"""Tests for LatexValidator, PdfValidator, ContentCompletenessChecker (tasks 029–031)."""

import pytest

from latex_article_generator.services.validators import (
    ContentCompletenessChecker,
    LatexValidator,
    PdfValidator,
    ValidationResult,
)

_VALID_LATEX = r"\begin{document}" + "\n" + r"\maketitle" + "\n" + r"\end{document}"
_LONG = " ".join(["word"] * 300)


# --- LatexValidator ---

@pytest.fixture
def lv():
    return LatexValidator()


def test_valid_latex_returns_true(lv):
    assert lv.validate(_VALID_LATEX).valid is True


def test_valid_latex_no_errors(lv):
    assert lv.validate(_VALID_LATEX).errors == []


def test_missing_begin_document_is_error(lv):
    result = lv.validate(r"\maketitle" + "\n" + r"\end{document}")
    assert any("begin{document}" in e for e in result.errors)


def test_missing_maketitle_is_error(lv):
    result = lv.validate(r"\begin{document}" + "\n" + r"\end{document}")
    assert any("maketitle" in e for e in result.errors)


def test_unclosed_brace_is_error(lv):
    result = lv.validate(_VALID_LATEX + "{unclosed")
    assert any("brace" in e for e in result.errors)


def test_extra_close_brace_is_error(lv):
    result = lv.validate(_VALID_LATEX + "}")
    assert any("brace" in e for e in result.errors)


def test_mismatched_environments_is_error(lv):
    src = r"\begin{document}" + "\n" + r"\maketitle" + "\n" + r"\begin{figure}" + "\n" + r"\end{document}"
    result = lv.validate(src)
    assert any("environment" in e for e in result.errors)


def test_valid_returns_validation_result(lv):
    assert isinstance(lv.validate(_VALID_LATEX), ValidationResult)


# --- PdfValidator ---

@pytest.fixture
def pv():
    return PdfValidator()


@pytest.fixture
def valid_pdf(tmp_path):
    path = tmp_path / "valid.pdf"
    path.write_bytes(b"%PDF-" + b"x" * 1024)
    return str(path)


def test_valid_pdf_returns_true(pv, valid_pdf):
    assert pv.validate(valid_pdf).valid is True


def test_missing_file_is_error(pv, tmp_path):
    result = pv.validate(str(tmp_path / "missing.pdf"))
    assert any("not found" in e for e in result.errors)


def test_small_file_is_error(pv, tmp_path):
    path = tmp_path / "small.pdf"
    path.write_bytes(b"%PDF-" + b"x" * 10)
    result = pv.validate(str(path))
    assert any("too small" in e for e in result.errors)


def test_wrong_header_is_error(pv, tmp_path):
    path = tmp_path / "fake.pdf"
    path.write_bytes(b"NOTPDF" + b"x" * 1024)
    result = pv.validate(str(path))
    assert any("magic bytes" in e for e in result.errors)


# --- ContentCompletenessChecker ---

@pytest.fixture
def cc():
    return ContentCompletenessChecker()


@pytest.fixture
def full_sections():
    return {"Introduction": _LONG, "Methodology": _LONG, "Conclusion": _LONG}


def test_full_sections_valid(cc, full_sections):
    assert cc.check(full_sections, has_hebrew=True).valid is True


def test_missing_introduction_is_error(cc):
    result = cc.check({"Methodology": _LONG, "Conclusion": _LONG})
    assert any("introduction" in e for e in result.errors)


def test_short_section_is_error(cc):
    result = cc.check({"Introduction": "too short", "Methodology": _LONG, "Conclusion": _LONG})
    assert any("too short" in e for e in result.errors)


def test_no_hebrew_adds_warning(cc, full_sections):
    result = cc.check(full_sections, has_hebrew=False)
    assert result.warnings != []
    assert result.valid is True


def test_has_hebrew_no_warning(cc, full_sections):
    result = cc.check(full_sections, has_hebrew=True)
    assert result.warnings == []
