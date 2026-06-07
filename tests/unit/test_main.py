"""Tests for main() entry point (task 033)."""

from unittest.mock import MagicMock, patch

import main as main_module

_SDK = "main.ArticleGeneratorSDK"


def _mock_sdk(latex="\\documentclass{article}", pdf_path="/out.pdf"):
    sdk = MagicMock()
    sdk.return_value.generate_article.return_value = latex
    sdk.return_value.compile_pdf.return_value = pdf_path
    return sdk


def test_latex_format_returns_0(tmp_path):
    out = str(tmp_path / "out.pdf")
    with patch(_SDK, _mock_sdk()):
        assert main_module.main(["--topic", "AI", "--format", "latex", "--output", out]) == 0


def test_pdf_format_returns_0(tmp_path):
    out = str(tmp_path / "out.pdf")
    with patch(_SDK, _mock_sdk(pdf_path=out)):
        assert main_module.main(["--topic", "AI", "--format", "pdf", "--output", out]) == 0


def test_exception_returns_1():
    sdk = MagicMock()
    sdk.return_value.generate_article.side_effect = RuntimeError("API error")
    with patch(_SDK, sdk):
        assert main_module.main(["--topic", "AI"]) == 1


def test_exception_prints_to_stderr(capsys):
    sdk = MagicMock()
    sdk.return_value.generate_article.side_effect = RuntimeError("API error")
    with patch(_SDK, sdk):
        main_module.main(["--topic", "AI"])
    assert "Error" in capsys.readouterr().err


def test_latex_format_writes_tex_file(tmp_path):
    out = str(tmp_path / "out.pdf")
    with patch(_SDK, _mock_sdk(latex="\\documentclass{article}")):
        main_module.main(["--topic", "AI", "--format", "latex", "--output", out])
    assert (tmp_path / "out.tex").exists()


def test_pdf_format_calls_compile_pdf(tmp_path):
    out = str(tmp_path / "out.pdf")
    mock = _mock_sdk(pdf_path=out)
    with patch(_SDK, mock):
        main_module.main(["--topic", "AI", "--format", "pdf", "--output", out])
    mock.return_value.compile_pdf.assert_called_once()
