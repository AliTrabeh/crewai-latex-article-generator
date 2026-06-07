"""Tests for GraphGenerator (task 018)."""

import pytest

from latex_article_generator.services.graph_generator import GraphGenerator


@pytest.fixture
def gen(tmp_path):
    return GraphGenerator(output_dir=str(tmp_path))


def test_line_chart_creates_file(gen, tmp_path):
    gen.line_chart({"A": [1, 2, 3]}, "Test", "test.png")
    assert (tmp_path / "test.png").exists()


def test_line_chart_returns_str(gen, tmp_path):
    result = gen.line_chart({"A": [1, 2, 3]}, "Test", "out.png")
    assert isinstance(result, str)
    assert result == str(tmp_path / "out.png")


def test_line_chart_file_nonempty(gen, tmp_path):
    gen.line_chart({"A": [1, 2, 3]}, "Test", "nonempty.png")
    assert (tmp_path / "nonempty.png").stat().st_size > 0


def test_line_chart_multiple_series(gen, tmp_path):
    gen.line_chart({"A": [1, 2], "B": [3, 4]}, "Multi", "multi.png")
    assert (tmp_path / "multi.png").exists()


def test_bar_chart_creates_file(gen, tmp_path):
    gen.bar_chart(["X", "Y"], [1.0, 2.0], "Bar", "bar.png")
    assert (tmp_path / "bar.png").exists()


def test_bar_chart_returns_str(gen, tmp_path):
    result = gen.bar_chart(["X", "Y"], [1.0, 2.0], "Bar", "bar2.png")
    assert isinstance(result, str)
    assert result == str(tmp_path / "bar2.png")


def test_bar_chart_file_nonempty(gen, tmp_path):
    gen.bar_chart(["X", "Y"], [1.0, 2.0], "Bar", "bar3.png")
    assert (tmp_path / "bar3.png").stat().st_size > 0


def test_output_dir_created_on_init(tmp_path):
    subdir = tmp_path / "nested" / "assets"
    GraphGenerator(output_dir=str(subdir))
    assert subdir.is_dir()


def test_different_filename_extension(gen, tmp_path):
    gen.bar_chart(["A"], [1.0], "Ext Test", "chart2.png")
    assert (tmp_path / "chart2.png").exists()
