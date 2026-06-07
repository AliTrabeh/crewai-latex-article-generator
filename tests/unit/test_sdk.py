"""Tests for ArticleGeneratorSDK pipeline (task 015)."""

from unittest.mock import MagicMock, patch

import pytest

from latex_article_generator.sdk.sdk import ArticleGeneratorSDK

_CREW = "latex_article_generator.services.crew.build_crew"
_COMPILER = "latex_article_generator.services.compiler.MultiPassCompiler"


@pytest.fixture
def sdk(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake")
    return ArticleGeneratorSDK()


def test_generate_article_calls_kickoff_once(sdk):
    mock_crew = MagicMock()
    mock_crew.kickoff.return_value = r"\documentclass{article}"
    with patch(_CREW, return_value=mock_crew):
        sdk.generate_article("AI", ["intro"])
    mock_crew.kickoff.assert_called_once()


def test_generate_article_returns_nonempty_string(sdk):
    mock_crew = MagicMock()
    mock_crew.kickoff.return_value = "some latex source"
    with patch(_CREW, return_value=mock_crew):
        result = sdk.generate_article("topic", ["intro", "conclusion"])
    assert isinstance(result, str) and len(result) > 0


def test_generate_article_returns_kickoff_value(sdk):
    mock_crew = MagicMock()
    mock_crew.kickoff.return_value = r"\begin{document}\end{document}"
    with patch(_CREW, return_value=mock_crew):
        result = sdk.generate_article("topic", ["body"])
    assert result == r"\begin{document}\end{document}"


def test_compile_pdf_delegates_to_compiler(sdk):
    mock_instance = MagicMock()
    mock_instance.compile.return_value = "/tmp/out.pdf"
    with patch(_COMPILER, return_value=mock_instance):
        result = sdk.compile_pdf(r"\documentclass{article}", "/tmp/out")
    mock_instance.compile.assert_called_once_with(r"\documentclass{article}", "/tmp/out")
    assert result == "/tmp/out.pdf"


def test_agent_config_defaults(sdk):
    cfg = sdk._agent_config()
    assert cfg["verbose"] is False
    assert cfg["max_iter"] == 5
