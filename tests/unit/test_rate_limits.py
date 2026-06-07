"""Tests for rate limits configuration (task 006)."""

import pytest

from latex_article_generator.shared.config import ConfigManager
from latex_article_generator.shared.gatekeeper import RateLimitConfig


@pytest.fixture(scope="module")
def cm() -> ConfigManager:
    return ConfigManager()


# ---------------------------------------------------------------------------
# JSON values match PRD spec
# ---------------------------------------------------------------------------


def test_default_requests_per_minute(cm):
    assert cm.get_rate_limit("default")["requests_per_minute"] == 20


def test_default_requests_per_hour(cm):
    assert cm.get_rate_limit("default")["requests_per_hour"] == 200


def test_default_concurrent_max(cm):
    assert cm.get_rate_limit("default")["concurrent_max"] == 3


def test_default_retry_after_seconds(cm):
    assert cm.get_rate_limit("default")["retry_after_seconds"] == 5


def test_default_max_retries(cm):
    assert cm.get_rate_limit("default")["max_retries"] == 3


def test_openai_requests_per_minute(cm):
    assert cm.get_rate_limit("openai")["requests_per_minute"] == 60


def test_openai_requests_per_hour(cm):
    assert cm.get_rate_limit("openai")["requests_per_hour"] == 500


def test_openai_concurrent_max(cm):
    assert cm.get_rate_limit("openai")["concurrent_max"] == 5


def test_openai_retry_after_seconds(cm):
    assert cm.get_rate_limit("openai")["retry_after_seconds"] == 10


def test_openai_max_retries(cm):
    assert cm.get_rate_limit("openai")["max_retries"] == 5


# ---------------------------------------------------------------------------
# Fallback behaviour
# ---------------------------------------------------------------------------


def test_unknown_service_falls_back_to_default(cm):
    limits = cm.get_rate_limit("unknown_service")
    assert limits == cm.get_rate_limit("default")


def test_no_arg_returns_default(cm):
    assert cm.get_rate_limit() == cm.get_rate_limit("default")


# ---------------------------------------------------------------------------
# RateLimitConfig dataclass
# ---------------------------------------------------------------------------


def test_rate_limit_config_instantiated_from_dict(cm):
    limits = cm.get_rate_limit("default")
    cfg = RateLimitConfig(**limits)
    assert cfg.requests_per_minute == 20
    assert cfg.max_retries == 3


def test_rate_limit_config_openai(cm):
    limits = cm.get_rate_limit("openai")
    cfg = RateLimitConfig(**limits)
    assert cfg.requests_per_minute == 60
    assert cfg.max_retries == 5


def test_rate_limit_config_is_dataclass():
    from dataclasses import fields
    field_names = {f.name for f in fields(RateLimitConfig)}
    expected = {
        "requests_per_minute",
        "requests_per_hour",
        "concurrent_max",
        "retry_after_seconds",
        "max_retries",
    }
    assert field_names == expected
