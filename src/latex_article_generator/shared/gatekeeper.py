"""Centralized API gatekeeper — all external API calls must pass through here."""

import logging
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


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
    """Snapshot of the current queue state."""

    depth: int
    requests_this_minute: int
    requests_this_hour: int


class ApiGatekeeper:
    """Centralized API call manager.

    Enforces rate limits, queues excess requests, and logs every call.
    No external API call may bypass this class.
    """

    def __init__(self, config: RateLimitConfig):
        """Initialize with rate-limit config loaded from a config file."""
        self._cfg = config
        self._minute_window: deque[float] = deque()
        self._hour_window: deque[float] = deque()
        self._queue: deque[tuple[Callable, tuple, dict]] = deque()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def execute(self, api_call: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute *api_call* through the gatekeeper.

        - Checks rate limits before execution.
        - Queues the request if limits are reached (FIFO).
        - Retries on transient failures up to max_retries.
        - Logs every call attempt and outcome.
        """
        self._prune_windows()
        self._wait_for_capacity()
        return self._execute_with_retry(api_call, *args, **kwargs)

    def get_queue_status(self) -> QueueStatus:
        """Return current queue depth and sliding-window counters."""
        self._prune_windows()
        return QueueStatus(
            depth=len(self._queue),
            requests_this_minute=len(self._minute_window),
            requests_this_hour=len(self._hour_window),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _prune_windows(self) -> None:
        now = time.monotonic()
        while self._minute_window and now - self._minute_window[0] > 60:
            self._minute_window.popleft()
        while self._hour_window and now - self._hour_window[0] > 3600:
            self._hour_window.popleft()

    def _wait_for_capacity(self) -> None:
        while (
            len(self._minute_window) >= self._cfg.requests_per_minute
            or len(self._hour_window) >= self._cfg.requests_per_hour
        ):
            logger.debug("Rate limit reached — waiting %ss", self._cfg.retry_after_seconds)
            time.sleep(self._cfg.retry_after_seconds)
            self._prune_windows()

    def _execute_with_retry(self, api_call: Callable, *args: Any, **kwargs: Any) -> Any:
        last_exc: Exception | None = None
        for attempt in range(1, self._cfg.max_retries + 1):
            try:
                now = time.monotonic()
                result = api_call(*args, **kwargs)
                self._minute_window.append(now)
                self._hour_window.append(now)
                logger.info("API call succeeded on attempt %d", attempt)
                return result
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                logger.warning("API call failed (attempt %d/%d): %s", attempt, self._cfg.max_retries, exc)
                if attempt < self._cfg.max_retries:
                    time.sleep(self._cfg.retry_after_seconds)
        raise RuntimeError(f"API call failed after {self._cfg.max_retries} attempts") from last_exc
