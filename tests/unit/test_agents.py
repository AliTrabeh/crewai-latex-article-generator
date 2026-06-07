"""Unit tests for all four CrewAI agent factories (tasks 007–010)."""

from unittest.mock import patch

import pytest
from crewai import Agent
from crewai.tools import BaseTool

_SERPER_TARGET = "latex_article_generator.services.researcher_agent.SerperDevTool"


class _FakeSerperTool(BaseTool):
    """Minimal BaseTool stand-in — no network calls."""

    name: str = "Serper Search"
    description: str = "Mock search tool for testing."

    def _run(self, *args, **kwargs) -> str:  # noqa: ANN002
        return ""


@pytest.fixture(autouse=True)
def fake_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key")


@pytest.fixture
def researcher():
    with patch(_SERPER_TARGET, return_value=_FakeSerperTool()):
        from latex_article_generator.services.researcher_agent import build_researcher_agent
        return build_researcher_agent({})


def test_researcher_returns_agent(researcher):
    assert isinstance(researcher, Agent)


def test_researcher_role(researcher):
    assert researcher.role == "Academic Researcher"


def test_researcher_no_delegation(researcher):
    assert researcher.allow_delegation is False


def test_researcher_has_tool(researcher):
    assert len(researcher.tools) == 1
    assert isinstance(researcher.tools[0], BaseTool)


def test_researcher_max_iter_default(researcher):
    assert researcher.max_iter == 5


def test_researcher_verbose_override():
    with patch(_SERPER_TARGET, return_value=_FakeSerperTool()):
        from latex_article_generator.services.researcher_agent import build_researcher_agent
        assert build_researcher_agent({"verbose": True}).verbose is True


@pytest.fixture
def writer():
    from latex_article_generator.services.writer_agent import build_writer_agent
    return build_writer_agent({})


def test_writer_returns_agent(writer):
    assert isinstance(writer, Agent)


def test_writer_role(writer):
    assert writer.role == "Academic Writer"


def test_writer_no_tools_no_delegation(writer):
    assert writer.tools == []
    assert writer.allow_delegation is False


def test_writer_max_iter_default(writer):
    assert writer.max_iter == 5


def test_writer_max_iter_override():
    from latex_article_generator.services.writer_agent import build_writer_agent
    assert build_writer_agent({"max_iter": 10}).max_iter == 10


@pytest.fixture
def reviewer():
    from latex_article_generator.services.reviewer_agent import build_reviewer_agent
    return build_reviewer_agent({})


def test_reviewer_returns_agent(reviewer):
    assert isinstance(reviewer, Agent)


def test_reviewer_role(reviewer):
    assert reviewer.role == "Academic Reviewer"


def test_reviewer_no_tools_no_delegation(reviewer):
    assert reviewer.tools == []
    assert reviewer.allow_delegation is False


def test_reviewer_max_iter_default(reviewer):
    assert reviewer.max_iter == 3


@pytest.fixture
def formatter():
    from latex_article_generator.services.latex_formatter_agent import build_latex_formatter_agent
    return build_latex_formatter_agent({})


def test_formatter_returns_agent(formatter):
    assert isinstance(formatter, Agent)


def test_formatter_role(formatter):
    assert formatter.role == "LaTeX Formatter"


def test_formatter_no_tools_no_delegation(formatter):
    assert formatter.tools == []
    assert formatter.allow_delegation is False


def test_formatter_max_iter_default(formatter):
    assert formatter.max_iter == 5
