"""Tests for build_crew() assembly (task 014)."""

from unittest.mock import patch

import pytest
from crewai import Crew, Process
from crewai.tools import BaseTool

_SERPER_TARGET = "latex_article_generator.services.researcher_agent.SerperDevTool"


class _FakeSerperTool(BaseTool):
    name: str = "Serper Search"
    description: str = "Mock search tool for testing."

    def _run(self, *args, **kwargs) -> str:  # noqa: ANN002
        return ""


@pytest.fixture(autouse=True)
def fake_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key")


@pytest.fixture
def crew():
    with patch(_SERPER_TARGET, return_value=_FakeSerperTool()):
        from latex_article_generator.services.crew import build_crew
        return build_crew("AI", ["intro", "methods"], {})


def test_build_crew_returns_crew(crew):
    assert isinstance(crew, Crew)


def test_crew_sequential_process(crew):
    assert crew.process == Process.sequential


def test_crew_has_four_agents(crew):
    assert len(crew.agents) == 4


def test_crew_has_four_tasks(crew):
    assert len(crew.tasks) == 4


def test_crew_verbose_default(crew):
    assert crew.verbose is False


def test_crew_verbose_override():
    with patch(_SERPER_TARGET, return_value=_FakeSerperTool()):
        from latex_article_generator.services.crew import build_crew
        c = build_crew("AI", ["intro"], {"verbose": True})
    assert c.verbose is True
