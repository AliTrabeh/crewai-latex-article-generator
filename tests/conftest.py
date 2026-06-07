"""Shared pytest fixtures."""

import pytest

from latex_article_generator.shared.config import ConfigManager
from latex_article_generator.shared.gatekeeper import ApiGatekeeper, RateLimitConfig


@pytest.fixture
def test_rate_limit_config() -> RateLimitConfig:
    """Minimal rate-limit config suitable for unit tests."""
    return RateLimitConfig(
        requests_per_minute=60,
        requests_per_hour=1000,
        concurrent_max=10,
        retry_after_seconds=1,
        max_retries=2,
    )


@pytest.fixture
def gatekeeper(test_rate_limit_config: RateLimitConfig) -> ApiGatekeeper:
    """Pre-configured ApiGatekeeper for unit tests."""
    return ApiGatekeeper(test_rate_limit_config)
