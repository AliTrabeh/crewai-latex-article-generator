"""Tests for CoverPageGenerator (task 022)."""

import pytest

from latex_article_generator.services.cover_page import CoverPageGenerator


@pytest.fixture
def gen():
    return CoverPageGenerator()


@pytest.fixture
def page(gen):
    return gen.generate("My Title", "Jane Doe", "MIT", "2026-06", "Short abstract.")


def test_starts_with_titlepage(page):
    assert page.startswith("\\begin{titlepage}")


def test_ends_with_end_titlepage(page):
    assert "\\end{titlepage}" in page


def test_contains_title(page):
    assert "My Title" in page


def test_contains_author(page):
    assert "Jane Doe" in page


def test_contains_institution(page):
    assert "MIT" in page


def test_contains_date(page):
    assert "2026-06" in page


def test_contains_abstract_env(page):
    assert "\\begin{abstract}" in page
    assert "\\end{abstract}" in page


def test_contains_abstract_text(page):
    assert "Short abstract." in page


def test_escape_latex_ampersand(gen):
    assert gen.escape_latex("a & b") == r"a \& b"


def test_escape_latex_percent(gen):
    assert gen.escape_latex("50%") == r"50\%"


def test_escape_latex_underscore(gen):
    assert gen.escape_latex("my_var") == r"my\_var"


def test_escape_latex_hash(gen):
    assert gen.escape_latex("#1") == r"\#1"


def test_escape_latex_combined(gen):
    result = gen.escape_latex("a & b_c 50% #tag")
    assert r"\&" in result
    assert r"\_" in result
    assert r"\%" in result
    assert r"\#" in result
