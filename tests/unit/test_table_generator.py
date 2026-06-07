"""Tests for TableGenerator (task 019)."""

import pytest

from latex_article_generator.services.table_generator import TableGenerator


@pytest.fixture
def gen():
    return TableGenerator()


@pytest.fixture
def simple_table(gen):
    return gen.generate(["A", "B"], [["1", "2"], ["3", "4"]])


def test_generate_contains_tabular(simple_table):
    assert "\\begin{tabular}" in simple_table


def test_generate_contains_hline(simple_table):
    assert "\\hline" in simple_table


def test_generate_headers_bold(simple_table):
    assert "\\textbf{A}" in simple_table
    assert "\\textbf{B}" in simple_table


def test_generate_rows_included(simple_table):
    assert "1 & 2 \\\\" in simple_table
    assert "3 & 4 \\\\" in simple_table


def test_generate_default_alignment(simple_table):
    assert "|l|l|" in simple_table


def test_generate_custom_alignment(gen):
    result = gen.generate(["X"], [["v"]], alignment="|c|")
    assert "|c|" in result


def test_generate_caption_present(gen):
    result = gen.generate(["A"], [["1"]], caption="My Caption")
    assert "\\caption{My Caption}" in result


def test_generate_no_caption_when_empty(simple_table):
    assert "\\caption" not in simple_table


def test_generate_label_present(gen):
    result = gen.generate(["A"], [["1"]], label="mytable")
    assert "\\label{tab:mytable}" in result


def test_generate_no_label_when_empty(simple_table):
    assert "\\label" not in simple_table


def test_generate_ends_with_end_table(simple_table):
    assert simple_table.strip().endswith("\\end{table}")


def test_escape_ampersand(gen):
    assert gen.escape("a & b") == r"a \& b"


def test_escape_percent(gen):
    assert gen.escape("50% done") == r"50\% done"


def test_escape_underscore(gen):
    assert gen.escape("my_var") == r"my\_var"


def test_escape_combined(gen):
    result = gen.escape("a & b_c 50%")
    assert r"\&" in result
    assert r"\_" in result
    assert r"\%" in result
