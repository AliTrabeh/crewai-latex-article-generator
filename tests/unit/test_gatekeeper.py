"""Tests for ApiGatekeeper (task 016)."""

import threading
import time
from unittest.mock import patch

import pytest

from latex_article_generator.shared.gatekeeper import ApiGatekeeper, QueueStatus, RateLimitConfig

_SLEEP = "latex_article_generator.shared.gatekeeper.time.sleep"


@pytest.fixture
def cfg():
    return RateLimitConfig(
        requests_per_minute=10,
        requests_per_hour=100,
        concurrent_max=2,
        retry_after_seconds=1,
        max_retries=3,
    )


@pytest.fixture
def gk(cfg):
    return ApiGatekeeper(cfg)


def test_execute_simple_callable(gk):
    assert gk.execute(lambda: 42) == 42


def test_execute_passes_positional_args(gk):
    assert gk.execute(lambda a, b: a + b, 3, 4) == 7


def test_execute_passes_keyword_args(gk):
    assert gk.execute(lambda x=0: x * 2, x=5) == 10


def test_queue_status_initial(gk):
    s = gk.get_queue_status()
    assert isinstance(s, QueueStatus)
    assert s.requests_this_minute == 0
    assert s.requests_this_hour == 0


def test_queue_status_increments_after_execute(gk):
    gk.execute(lambda: None)
    gk.execute(lambda: None)
    s = gk.get_queue_status()
    assert s.requests_this_minute == 2
    assert s.requests_this_hour == 2


def test_retry_succeeds_on_second_attempt(cfg):
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise ValueError("transient")
        return "ok"

    with patch(_SLEEP):
        result = ApiGatekeeper(cfg).execute(flaky)
    assert result == "ok"
    assert len(calls) == 2


def test_max_retries_raises_original_exception(cfg):
    def always_fails():
        raise RuntimeError("permanent failure")

    with patch(_SLEEP), pytest.raises(RuntimeError, match="permanent failure"):
        ApiGatekeeper(cfg).execute(always_fails)


def test_wait_for_capacity_sleeps_when_limit_reached(cfg):
    gk = ApiGatekeeper(cfg)
    t = time.monotonic()
    # pre-fill the window to its per-minute limit
    gk._minute_window.extend([t] * cfg.requests_per_minute)

    sleep_calls = []

    def fake_sleep(n):
        sleep_calls.append(n)
        gk._minute_window.clear()  # simulate window expiry

    with patch(_SLEEP, side_effect=fake_sleep):
        gk.execute(lambda: None)

    assert sleep_calls == [1]


def test_thread_safety(gk):
    results, errors = [], []

    def call():
        try:
            results.append(gk.execute(lambda: 1))
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=call) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(results) == 5
    assert gk.get_queue_status().requests_this_minute == 5
