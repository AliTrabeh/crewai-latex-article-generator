"""Crew assembly — task 014."""

from crewai import Crew, Process

from latex_article_generator.services.latex_formatter_agent import build_latex_formatter_agent
from latex_article_generator.services.researcher_agent import build_researcher_agent
from latex_article_generator.services.reviewer_agent import build_reviewer_agent
from latex_article_generator.services.tasks import (
    build_formatting_task,
    build_research_task,
    build_review_task,
    build_writing_task,
)
from latex_article_generator.services.writer_agent import build_writer_agent


def build_crew(topic: str, sections: list[str], config: dict) -> Crew:
    """Assemble and return the full article-generation Crew."""
    researcher = build_researcher_agent(config)
    writer = build_writer_agent(config)
    reviewer = build_reviewer_agent(config)
    formatter = build_latex_formatter_agent(config)

    research_task = build_research_task(topic, sections, researcher)
    writing_task = build_writing_task(topic, sections, writer, research_task)
    review_task = build_review_task(reviewer, writing_task)
    formatting_task = build_formatting_task(formatter, review_task)

    return Crew(
        agents=[researcher, writer, reviewer, formatter],
        tasks=[research_task, writing_task, review_task, formatting_task],
        process=Process.sequential,
        verbose=config.get("verbose", False),
    )
