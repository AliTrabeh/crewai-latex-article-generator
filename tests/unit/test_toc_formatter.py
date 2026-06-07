"""Tests for TocFormatter (task 023)."""

import pytest

from latex_article_generator.services.toc_formatter import TocFormatter


@pytest.fixture
def fmt():
    return TocFormatter()


def test_toc_block_contains_tableofcontents(fmt):
    assert "\\tableofcontents" in fmt.generate_toc_block()


def test_toc_block_contains_newpage(fmt):
    assert "\\newpage" in fmt.generate_toc_block()


def test_headers_footers_contains_fancyhead(fmt):
    result = fmt.configure_headers_footers("Title", "Author")
    assert "\\fancyhead" in result


def test_headers_footers_contains_fancyfoot(fmt):
    result = fmt.configure_headers_footers("Title", "Author")
    assert "\\fancyfoot" in result


def test_headers_footers_contains_author(fmt):
    result = fmt.configure_headers_footers("Title", "Jane Doe")
    assert "Jane Doe" in result


def test_headers_footers_contains_title(fmt):
    result = fmt.configure_headers_footers("My Article", "Author")
    assert "My Article" in result


def test_headers_footers_contains_pagestyle(fmt):
    result = fmt.configure_headers_footers("T", "A")
    assert "\\pagestyle{fancy}" in result


def test_page_numbering_arabic(fmt):
    assert fmt.set_page_numbering("arabic") == "\\pagenumbering{arabic}\n"


def test_page_numbering_roman(fmt):
    assert fmt.set_page_numbering("roman") == "\\pagenumbering{roman}\n"


def test_page_numbering_default_arabic(fmt):
    assert "arabic" in fmt.set_page_numbering()
