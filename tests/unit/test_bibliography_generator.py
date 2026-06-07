"""Tests for BibliographyGenerator (task 024)."""

import pytest

from latex_article_generator.services.bibliography_generator import (
    BibliographyGenerator,
    Reference,
)


@pytest.fixture
def gen():
    return BibliographyGenerator()


@pytest.fixture
def article_ref():
    return Reference(key="Smith2023", author="A. Smith", title="AI Study",
                     year="2023", journal="Nature")


@pytest.fixture
def proc_ref():
    return Reference(key="Jones2022", author="B. Jones", title="Deep Learning",
                     year="2022", booktitle="ICML 2022")


def test_article_entry_type(gen, article_ref):
    assert "@article{Smith2023," in gen.generate_bib_file([article_ref])


def test_inproceedings_entry_type(gen, proc_ref):
    assert "@inproceedings{Jones2022," in gen.generate_bib_file([proc_ref])


def test_entry_contains_author(gen, article_ref):
    assert "A. Smith" in gen.generate_bib_file([article_ref])


def test_entry_contains_title(gen, article_ref):
    assert "AI Study" in gen.generate_bib_file([article_ref])


def test_entry_contains_year(gen, article_ref):
    assert "2023" in gen.generate_bib_file([article_ref])


def test_entry_contains_journal(gen, article_ref):
    assert "Nature" in gen.generate_bib_file([article_ref])


def test_entry_contains_booktitle(gen, proc_ref):
    assert "ICML 2022" in gen.generate_bib_file([proc_ref])


def test_multiple_refs_joined(gen, article_ref, proc_ref):
    result = gen.generate_bib_file([article_ref, proc_ref])
    assert result.count("@") == 2


def test_duplicate_key_raises(gen, article_ref):
    dup = Reference(key="Smith2023", author="X", title="Y", year="2024", journal="J")
    with pytest.raises(ValueError, match="Duplicate"):
        gen.generate_bib_file([article_ref, dup])


def test_write_bib_creates_file(gen, article_ref, tmp_path):
    path = str(tmp_path / "refs.bib")
    gen.write_bib_file([article_ref], path)
    assert (tmp_path / "refs.bib").exists()


def test_write_bib_returns_path(gen, article_ref, tmp_path):
    path = str(tmp_path / "refs.bib")
    result = gen.write_bib_file([article_ref], path)
    assert result == path
