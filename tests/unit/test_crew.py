"""Tests for build_crew() assembly (task 014)."""

import pytest
from crewai import Crew, Process


@pytest.fixture(autouse=True)
def fake_anthropic_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-fake-key")


@pytest.fixture
def crew():
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
    from latex_article_generator.services.crew import build_crew
    c = build_crew("AI", ["intro"], {"verbose": True})
    assert c.verbose is True
