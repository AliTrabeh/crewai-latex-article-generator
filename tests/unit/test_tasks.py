"""Tests for all four task factories (tasks 011–014)."""

import pytest
from crewai import Task


@pytest.fixture(autouse=True)
def fake_anthropic_key(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-fake-key")


@pytest.fixture
def researcher():
    from latex_article_generator.services.researcher_agent import build_researcher_agent
    return build_researcher_agent({})


@pytest.fixture
def writer():
    from latex_article_generator.services.writer_agent import build_writer_agent
    return build_writer_agent({})


@pytest.fixture
def reviewer():
    from latex_article_generator.services.reviewer_agent import build_reviewer_agent
    return build_reviewer_agent({})


@pytest.fixture
def formatter():
    from latex_article_generator.services.latex_formatter_agent import build_latex_formatter_agent
    return build_latex_formatter_agent({})


@pytest.fixture
def research_task(researcher):
    from latex_article_generator.services.tasks import build_research_task
    return build_research_task("AI", ["intro", "methods"], researcher)


@pytest.fixture
def writing_task(writer, research_task):
    from latex_article_generator.services.tasks import build_writing_task
    return build_writing_task("AI", ["intro"], writer, research_task)


@pytest.fixture
def review_task(reviewer, writing_task):
    from latex_article_generator.services.tasks import build_review_task
    return build_review_task(reviewer, writing_task)


@pytest.fixture
def formatting_task(formatter, review_task):
    from latex_article_generator.services.tasks import build_formatting_task
    return build_formatting_task(formatter, review_task)


def test_research_task_returns_task(research_task):
    assert isinstance(research_task, Task)


def test_research_task_description_has_topic(research_task):
    assert "AI" in research_task.description


def test_research_task_description_has_sections(research_task):
    assert "intro" in research_task.description


def test_research_task_output_has_citations(research_task):
    assert "cited academic sources" in research_task.expected_output


def test_writing_task_returns_task(writing_task):
    assert isinstance(writing_task, Task)


def test_writing_task_has_context(writing_task, research_task):
    assert research_task in writing_task.context


def test_writing_task_description_has_topic(writing_task):
    assert "AI" in writing_task.description


def test_writing_task_output_has_word_count(writing_task):
    assert "300 words" in writing_task.expected_output


def test_review_task_returns_task(review_task):
    assert isinstance(review_task, Task)


def test_review_task_has_context(review_task, writing_task):
    assert writing_task in review_task.context


def test_review_task_output_has_summary(review_task):
    assert "review summary" in review_task.expected_output


def test_formatting_task_returns_task(formatting_task):
    assert isinstance(formatting_task, Task)


def test_formatting_task_has_context(formatting_task, review_task):
    assert review_task in formatting_task.context


def test_formatting_task_output_has_latex(formatting_task):
    assert r"\documentclass" in formatting_task.expected_output
