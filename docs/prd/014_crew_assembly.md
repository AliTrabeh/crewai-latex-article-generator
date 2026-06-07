---
id: "014"
title: "Crew Assembly"
group: "4 — CrewAI Tasks and Workflow"
priority: high
status: NOT_STARTED
---

# Task 014 — Crew Assembly

## Goal

Wire all four agents and four tasks into a single `Crew` with a Sequential process. Expose a `build_crew()` factory function used by the SDK pipeline.

## Files to Create or Modify

- `src/latex_article_generator/services/crew.py` — `build_crew()` factory

## Exact Expected Behavior

```python
from crewai import Crew, Process
from latex_article_generator.services.researcher_agent import build_researcher_agent
from latex_article_generator.services.writer_agent import build_writer_agent
from latex_article_generator.services.reviewer_agent import build_reviewer_agent
from latex_article_generator.services.latex_formatter_agent import build_latex_formatter_agent
from latex_article_generator.services.tasks import (
    build_research_task,
    build_writing_task,
    build_review_task,
    build_formatting_task,
)

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
```

## Acceptance Criteria

- [ ] `build_crew("AI", ["intro"], {})` returns a `crewai.Crew` without error (agents mocked).
- [ ] `crew.process` is `Process.sequential`.
- [ ] `len(crew.agents) == 4` and `len(crew.tasks) == 4`.
- [ ] `crew.kickoff()` is called in the SDK pipeline (task 015), not here.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- `build_formatting_task` must be added to `tasks.py` (task 011–013 file) — it converts the reviewed text to LaTeX.
- The `config` dict is passed down to all agent factories to allow runtime tuning.
- Do not call `crew.kickoff()` inside `build_crew()` — separation of construction and execution is required.
