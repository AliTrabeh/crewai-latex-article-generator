"""Tests for version tracking (task 003)."""

import json
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


def test_package_version_is_string():
    from latex_article_generator import __version__

    assert isinstance(__version__, str)
    assert __version__ == "1.00"


def test_version_module_directly():
    from latex_article_generator.shared.version import __version__

    assert __version__ == "1.00"


def test_package_exports_version():
    import latex_article_generator

    assert hasattr(latex_article_generator, "__version__")
    assert latex_article_generator.__version__ == "1.00"


def test_setup_json_version():
    cfg = json.loads((CONFIG_DIR / "setup.json").read_text(encoding="utf-8"))
    assert cfg.get("version") == "1.00"


def test_rate_limits_json_version():
    cfg = json.loads((CONFIG_DIR / "rate_limits.json").read_text(encoding="utf-8"))
    assert cfg.get("version") == "1.00"


def test_logging_config_json_version():
    cfg = json.loads((CONFIG_DIR / "logging_config.json").read_text(encoding="utf-8"))
    assert cfg.get("version") == "1.00"
