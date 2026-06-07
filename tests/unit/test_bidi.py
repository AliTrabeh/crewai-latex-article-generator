"""Tests for BiDiHandler (task 017)."""

import pytest

from latex_article_generator.services.bidi_handler import BiDiHandler


@pytest.fixture
def h():
    return BiDiHandler()


def test_process_wraps_single_hebrew_word(h):
    assert h.process("Hello שלום World") == r"Hello \begin{RTL}שלום\end{RTL} World"


def test_process_pure_ascii_unchanged(h):
    text = "Hello World 123"
    assert h.process(text) == text


def test_process_only_hebrew(h):
    assert h.process("שלום") == r"\begin{RTL}שלום\end{RTL}"


def test_process_consecutive_hebrew_words_single_block(h):
    assert h.process("שלום עולם") == r"\begin{RTL}שלום עולם\end{RTL}"


def test_process_multiple_separated_hebrew_segments(h):
    result = h.process("Hello שלום and עולם end")
    assert result.count(r"\begin{RTL}") == 2
    assert result.count(r"\end{RTL}") == 2


def test_process_empty_string(h):
    assert h.process("") == ""


def test_contains_hebrew_true(h):
    assert h.contains_hebrew("שלום") is True


def test_contains_hebrew_false_ascii(h):
    assert h.contains_hebrew("Hello World") is False


def test_contains_hebrew_mixed(h):
    assert h.contains_hebrew("Hello שלום") is True


def test_contains_hebrew_empty(h):
    assert h.contains_hebrew("") is False
