---
id: "016"
title: "ApiGatekeeper Implementation"
group: "5 — Content Generation Pipeline"
priority: critical
---

# Task 016 — ApiGatekeeper Implementation

## Goal

Fully implement `ApiGatekeeper` in `shared/gatekeeper.py`. All external API calls must pass through this class — no direct API call may bypass it.

## Files to Create or Modify

- `src/latex_article_generator/shared/gatekeeper.py` — full implementation

## Exact Expected Behavior

```python
import time
from collections import deque
from dataclasses import dataclass
from threading import Lock
from typing import Any, Callable

@dataclass
class RateLimitConfig:
    requests_per_minute: int
    requests_per_hour: int
    concurrent_max: int
    retry_after_seconds: int
    max_retries: int

@dataclass
class QueueStatus:
    depth: int
    requests_this_minute: int
    requests_this_hour: int

class ApiGatekeeper:
    def __init__(self, config: RateLimitConfig) -> None:
        self._config = config
        self._minute_window: deque[float] = deque()
        self._hour_window: deque[float] = deque()
        self._lock = Lock()

    def execute(self, api_call: Callable, *args: Any, **kwargs: Any) -> Any:
        """Enforce rate limits, then execute the callable with retry logic."""
        with self._lock:
            self._wait_for_capacity()
            return self._execute_with_retry(api_call, *args, **kwargs)

    def get_queue_status(self) -> QueueStatus:
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
            if (len(self._minute_window) < self._config.requests_per_minute and
                    len(self._hour_window) < self._config.requests_per_hour):
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
```

## Acceptance Criteria

- [ ] `gatekeeper.execute(lambda: 42)` returns `42`.
- [ ] Exceeding `requests_per_minute` causes `_wait_for_capacity` to block (test with time mock).
- [ ] After `max_retries` failures, the original exception propagates.
- [ ] `get_queue_status()` returns correct counts.
- [ ] Thread-safety: concurrent calls do not corrupt window counts.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Use `time.monotonic()` (not `time.time()`) to avoid wall-clock skew issues.
- The `Lock` ensures thread safety when multiple CrewAI tasks call APIs concurrently.
- In tests, patch `time.sleep` and `time.monotonic` to avoid slow tests.
