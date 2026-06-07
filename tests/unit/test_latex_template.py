"""Tests for LatexTemplate (task 021)."""

import pytest

from latex_article_generator.services.latex_template import LatexTemplate


@pytest.fixture
def tmpl():
    return LatexTemplate()


@pytest.fixture
def rendered(tmpl):
    return tmpl.render_preamble("My Title", "Jane Doe", "2026-06", "refs.bib")


def test_render_returns_str(rendered):
    assert isinstance(rendered, str)


def test_render_contains_documentclass(rendered):
    assert r"\documentclass" in rendered


def test_render_contains_polyglossia(rendered):
    assert "polyglossia" in rendered


def test_render_contains_fontspec(rendered):
    assert "fontspec" in rendered


def test_render_contains_tikz(rendered):
    assert "tikz" in rendered


def test_render_contains_biblatex(rendered):
    assert "biblatex" in rendered


def test_render_contains_graphicx(rendered):
    assert "graphicx" in rendered


def test_render_bib_file_substituted(rendered):
    assert "refs.bib" in rendered


def test_render_title_substituted(rendered):
    assert "My Title" in rendered


def test_render_author_substituted(rendered):
    assert "Jane Doe" in rendered


def test_render_date_substituted(rendered):
    assert "2026-06" in rendered


def test_render_no_unresolved_placeholders(rendered):
    assert "{bib_file}" not in rendered
    assert "{title}" not in rendered
    assert "{author}" not in rendered
    assert "{date}" not in rendered
