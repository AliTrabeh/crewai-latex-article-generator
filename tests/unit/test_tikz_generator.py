"""Tests for TikZGenerator (task 020)."""

import pytest

from latex_article_generator.services.tikz_generator import TikZGenerator


@pytest.fixture
def gen():
    return TikZGenerator()


_NODE = {"id": "a", "label": "Alpha", "x": 0, "y": 0}
_NODE_B = {"id": "b", "label": "Beta", "x": 2, "y": 0}


def test_block_diagram_contains_begin(gen):
    assert "\\begin{tikzpicture}" in gen.block_diagram([_NODE], [])


def test_block_diagram_contains_end(gen):
    assert "\\end{tikzpicture}" in gen.block_diagram([_NODE], [])


def test_block_diagram_has_node(gen):
    result = gen.block_diagram([_NODE], [])
    assert "(a)" in result
    assert "Alpha" in result


def test_block_diagram_has_edge(gen):
    result = gen.block_diagram([_NODE, _NODE_B], [("a", "b")])
    assert "\\draw[->] (a) -- (b);" in result


def test_block_diagram_empty_edges(gen):
    result = gen.block_diagram([_NODE], [])
    assert "\\draw" not in result


def test_block_diagram_multiple_nodes(gen):
    result = gen.block_diagram([_NODE, _NODE_B], [])
    assert "(a)" in result
    assert "(b)" in result


def test_flowchart_contains_begin(gen):
    assert "\\begin{tikzpicture}" in gen.flowchart(["Start"])


def test_flowchart_contains_end(gen):
    assert "\\end{tikzpicture}" in gen.flowchart(["Start"])


def test_flowchart_rectangle_for_normal(gen):
    result = gen.flowchart(["Start"])
    assert "rectangle" in result


def test_flowchart_diamond_for_question(gen):
    result = gen.flowchart(["?Decision"])
    assert "diamond" in result


def test_flowchart_strips_question_mark(gen):
    result = gen.flowchart(["?Decision"])
    assert "Decision" in result
    assert "?Decision" not in result


def test_flowchart_draws_arrows_between_steps(gen):
    result = gen.flowchart(["Start", "End"])
    assert "\\draw[->]" in result


def test_flowchart_single_step_no_arrow(gen):
    result = gen.flowchart(["Start"])
    assert "\\draw" not in result


def test_flowchart_three_steps_two_arrows(gen):
    result = gen.flowchart(["A", "B", "C"])
    assert result.count("\\draw[->]") == 2
