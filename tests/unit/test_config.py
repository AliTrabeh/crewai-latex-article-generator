"""Tests for ConfigManager (task 004)."""

import json
from pathlib import Path

import pytest

from latex_article_generator.shared.config import ConfigManager
from latex_article_generator.shared.version import __version__


def _write_valid_configs(tmp_path: Path, setup_overrides: dict | None = None) -> None:
    """Write a minimal set of valid config files into tmp_path."""
    setup = {"version": __version__, "app_name": "test-app", **(setup_overrides or {})}
    rate = {
        "version": __version__,
        "rate_limits": {
            "default": {
                "requests_per_minute": 10,
                "requests_per_hour": 100,
                "concurrent_max": 2,
                "retry_after_seconds": 5,
                "max_retries": 1,
            }
        },
    }
    logging_cfg = {
        "version": __version__,
        "logging": {"version": 1, "disable_existing_loggers": False, "handlers": {}, "root": {"level": "INFO", "handlers": []}},
    }
    (tmp_path / "setup.json").write_text(json.dumps(setup), encoding="utf-8")
    (tmp_path / "rate_limits.json").write_text(json.dumps(rate), encoding="utf-8")
    (tmp_path / "logging_config.json").write_text(json.dumps(logging_cfg), encoding="utf-8")


def test_default_config_dir_resolves():
    cm = ConfigManager()
    assert cm._config_dir.exists()
    assert cm._config_dir.is_dir()


def test_custom_config_dir(tmp_path):
    _write_valid_configs(tmp_path)
    cm = ConfigManager(config_dir=str(tmp_path))
    assert cm.get("app_name") == "test-app"


def test_get_app_name():
    cm = ConfigManager()
    assert cm.get("app_name") == "crewai-latex-article-generator"


def test_get_missing_key(cm=None):
    cm = ConfigManager()
    assert cm.get("no_such_key", "fallback") == "fallback"
    assert cm.get("no_such_key") is None


def test_get_rate_limit_default_has_required_keys():
    cm = ConfigManager()
    limits = cm.get_rate_limit("default")
    for key in ("requests_per_minute", "requests_per_hour", "concurrent_max"):
        assert key in limits, f"Missing key: {key}"


def test_get_rate_limit_unknown_service_falls_back_to_default():
    cm = ConfigManager()
    limits = cm.get_rate_limit("nonexistent_service")
    assert isinstance(limits, dict)
    assert "requests_per_minute" in limits


def test_get_logging_returns_dictconfig_compatible_dict():
    cm = ConfigManager()
    log_cfg = cm.get_logging()
    assert isinstance(log_cfg, dict)
    assert log_cfg.get("version") == 1  # dictConfig protocol requires integer 1


def test_missing_config_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        ConfigManager(config_dir=str(tmp_path))


def test_corrupted_json_raises_decode_error(tmp_path):
    (tmp_path / "setup.json").write_text("not { valid json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        ConfigManager(config_dir=str(tmp_path))


def test_version_mismatch_in_setup_raises_runtime_error(tmp_path):
    _write_valid_configs(tmp_path, setup_overrides={"version": "9.99"})
    with pytest.raises(RuntimeError, match="setup.json"):
        ConfigManager(config_dir=str(tmp_path))


def test_version_mismatch_message_names_file(tmp_path):
    _write_valid_configs(tmp_path)
    rate = {"version": "9.99", "rate_limits": {"default": {}}}
    (tmp_path / "rate_limits.json").write_text(json.dumps(rate), encoding="utf-8")
    with pytest.raises(RuntimeError, match="rate_limits.json"):
        ConfigManager(config_dir=str(tmp_path))


def test_config_without_version_field_is_accepted(tmp_path):
    """A config file that omits 'version' entirely should not raise."""
    setup = {"app_name": "no-version-app"}
    rate = {"version": __version__, "rate_limits": {"default": {}}}
    logging_cfg = {"version": __version__, "logging": {"version": 1}}
    (tmp_path / "setup.json").write_text(json.dumps(setup), encoding="utf-8")
    (tmp_path / "rate_limits.json").write_text(json.dumps(rate), encoding="utf-8")
    (tmp_path / "logging_config.json").write_text(json.dumps(logging_cfg), encoding="utf-8")
    cm = ConfigManager(config_dir=str(tmp_path))
    assert cm.get("app_name") == "no-version-app"
