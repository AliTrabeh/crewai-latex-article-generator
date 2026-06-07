"""Tests for LaTeXAssembler (task 025)."""

import pytest

from latex_article_generator.services.latex_assembler import LaTeXAssembler


@pytest.fixture
def asm():
    return LaTeXAssembler()


@pytest.fixture
def assembled(asm, tmp_path):
    out = str(tmp_path / "article.tex")
    asm.assemble(
        preamble="\\documentclass{article}",
        cover_page="\\begin{titlepage}\\end{titlepage}",
        toc_block="\\tableofcontents",
        header_footer="\\pagestyle{fancy}",
        sections={"Introduction": "Intro text.", "Conclusion": "Conc text."},
        bibliography_path="refs.bib",
        output_path=out,
    )
    return out


def test_assemble_returns_path(asm, tmp_path):
    out = str(tmp_path / "out.tex")
    result = asm.assemble("", "", "", "", {}, "", out)
    assert result == out


def test_assemble_writes_file(assembled):
    from pathlib import Path
    assert Path(assembled).exists()


def test_assemble_contains_begin_document(assembled):
    from pathlib import Path
    content = Path(assembled).read_text(encoding="utf-8")
    assert "\\begin{document}" in content


def test_assemble_contains_end_document(assembled):
    from pathlib import Path
    content = Path(assembled).read_text(encoding="utf-8")
    assert "\\end{document}" in content


def test_assemble_contains_section(assembled):
    from pathlib import Path
    content = Path(assembled).read_text(encoding="utf-8")
    assert "\\section{Introduction}" in content
    assert "\\section{Conclusion}" in content


def test_assemble_contains_printbibliography(assembled):
    from pathlib import Path
    content = Path(assembled).read_text(encoding="utf-8")
    assert "\\printbibliography" in content


def test_assemble_section_order(assembled):
    from pathlib import Path
    content = Path(assembled).read_text(encoding="utf-8")
    assert content.index("Introduction") < content.index("Conclusion")
