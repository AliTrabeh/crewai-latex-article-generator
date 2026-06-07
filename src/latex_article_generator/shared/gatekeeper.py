"""Centralized API gatekeeper — all external API calls must pass through here."""

import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from threading import Lock
from typing import Any


@dataclass
class RateLimitConfig:
    """Rate-limit settings loaded from config, never hardcoded."""

    requests_per_minute: int
    requests_per_hour: int
    concurrent_max: int
    retry_after_seconds: int
    max_retries: int


@dataclass
class QueueStatus:
    """Snapshot of sliding-window counters."""

    depth: int
    requests_this_minute: int
    requests_this_hour: int


class ApiGatekeeper:
    """Serialises API calls, enforces rate limits, and retries on failure."""

    def __init__(self, config: RateLimitConfig) -> None:
        """Initialise with rate-limit config loaded from a config file."""
        self._config = config
        self._minute_window: deque[float] = deque()
        self._hour_window: deque[float] = deque()
        self._lock = Lock()

    def execute(self, api_call: Callable, *args: Any, **kwargs: Any) -> Any:
        """Enforce rate limits then execute *api_call* with retry logic."""
        with self._lock:
            self._wait_for_capacity()
            return self._execute_with_retry(api_call, *args, **kwargs)

    def get_queue_status(self) -> QueueStatus:
        """Return current sliding-window counters."""
        self._prune_windows()
        return QueueStatus(
            depth=0,
            requests_this_minute=len(self._minute_window),
            requests_this_hour=len(self._hour_window),
        )

    def _prune_windows(self) -> None:
        now = time.monotonic()
        while self._minute_window and now - self._minute_window[0] > 60:
            self._minute_window.popleft()
        while self._hour_window and now - self._hour_window[0] > 3600:
            self._hour_window.popleft()

    def _wait_for_capacity(self) -> None:
        while True:
            self._prune_windows()
            if (
                len(self._minute_window) < self._config.requests_per_minute
                and len(self._hour_window) < self._config.requests_per_hour
            ):
                break
            time.sleep(1)

    def _execute_with_retry(self, api_call: Callable, *args: Any, **kwargs: Any) -> Any:
        for attempt in range(self._config.max_retries):
            try:
                now = time.monotonic()
                self._minute_window.append(now)
                self._hour_window.append(now)
                return api_call(*args, **kwargs)
            except Exception:
                if attempt == self._config.max_retries - 1:
                    raise
                time.sleep(self._config.retry_after_seconds)
        return None  # unreachable; satisfies type checkers
