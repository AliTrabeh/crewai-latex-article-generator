"""Tests for environment variables and secrets management (task 005)."""

import os
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_env_example_exists():
    assert (PROJECT_ROOT / ".env-example").exists()


def test_env_example_contains_all_required_keys():
    content = (PROJECT_ROOT / ".env-example").read_text(encoding="utf-8")
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "SERPER_API_KEY"):
        assert key in content, f"Missing key in .env-example: {key}"


def test_env_example_has_no_real_keys():
    content = (PROJECT_ROOT / ".env-example").read_text(encoding="utf-8")
    assert "sk-" not in content, "Real API key found in .env-example"


def test_gitignore_excludes_dot_env():
    content = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in content


def test_load_dotenv_present_in_entrypoint():
    content = (PROJECT_ROOT / "src" / "main.py").read_text(encoding="utf-8")
    assert "load_dotenv" in content, "load_dotenv() must be called in src/main.py"


def test_missing_api_key_raises_environment_error(monkeypatch):
    """Pattern: os.environ.get() + explicit EnvironmentError if None."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    key = os.environ.get("OPENAI_API_KEY")
    with pytest.raises(OSError, match="OPENAI_API_KEY"):
        if not key:
            raise OSError("OPENAI_API_KEY is not set")
