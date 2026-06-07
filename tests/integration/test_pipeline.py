"""Integration tests — full SDK pipeline with mocked LLM and compiler (task 040)."""

from unittest.mock import MagicMock, patch

import pytest

from latex_article_generator.sdk.sdk import ArticleGeneratorSDK

_CREW = "latex_article_generator.services.crew.build_crew"
_COMPILER = "latex_article_generator.services.compiler.MultiPassCompiler"

MOCK_LATEX = r"""
\documentclass{article}
\begin{document}
\maketitle
\section{Introduction}
This is the introduction.
\section{Conclusion}
This is the conclusion.
\printbibliography
\end{document}
"""


@pytest.fixture(autouse=True)
def fake_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-integration")


@pytest.fixture
def sdk():
    return ArticleGeneratorSDK()


def test_generate_article_returns_string(sdk):
    mock_crew = MagicMock()
    mock_crew.kickoff.return_value = MOCK_LATEX
    with patch(_CREW, return_value=mock_crew):
        result = sdk.generate_article("AI", ["introduction", "conclusion"])
    assert isinstance(result, str)
    assert len(result) > 0


def test_generate_article_calls_kickoff(sdk):
    mock_crew = MagicMock()
    mock_crew.kickoff.return_value = MOCK_LATEX
    with patch(_CREW, return_value=mock_crew):
        sdk.generate_article("Quantum Computing", ["intro"])
    mock_crew.kickoff.assert_called_once()


def test_generate_article_returns_kickoff_value(sdk):
    mock_crew = MagicMock()
    mock_crew.kickoff.return_value = MOCK_LATEX
    with patch(_CREW, return_value=mock_crew):
        result = sdk.generate_article("AI", ["intro"])
    assert result == MOCK_LATEX


def test_compile_pdf_returns_path(sdk, tmp_path):
    out = str(tmp_path / "article.pdf")
    mock_instance = MagicMock()
    mock_instance.compile.return_value = out
    with patch(_COMPILER, return_value=mock_instance):
        result = sdk.compile_pdf(MOCK_LATEX, out)
    assert result == out
    assert result.endswith(".pdf")


def test_compile_pdf_delegates_to_compiler(sdk, tmp_path):
    out = str(tmp_path / "article.pdf")
    mock_instance = MagicMock()
    mock_instance.compile.return_value = out
    with patch(_COMPILER, return_value=mock_instance):
        sdk.compile_pdf(MOCK_LATEX, out)
    mock_instance.compile.assert_called_once_with(MOCK_LATEX, out)


def test_sdk_agent_config_defaults(sdk):
    cfg = sdk._agent_config()
    assert cfg["verbose"] is False
    assert cfg["max_iter"] == 5


def test_full_pipeline_latex_to_string(sdk):
    mock_crew = MagicMock()
    mock_crew.kickoff.return_value = MOCK_LATEX
    with patch(_CREW, return_value=mock_crew):
        latex = sdk.generate_article("Federated Learning", ["intro", "conclusion"])
    assert r"\documentclass" in latex
