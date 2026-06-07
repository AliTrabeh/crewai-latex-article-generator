---
id: "011"
title: "Research Task"
group: "4 — CrewAI Tasks and Workflow"
priority: high
---

# Task 011 — Research Task

## Goal

Define the CrewAI `Task` that directs `ResearcherAgent` to gather structured information about the requested topic and produce a research brief consumed by the writer.

## Files to Create or Modify

- `src/latex_article_generator/services/tasks.py` — task factory functions (all four tasks in one file)

## Exact Expected Behavior

```python
from crewai import Task
from latex_article_generator.services.researcher_agent import build_researcher_agent

def build_research_task(topic: str, sections: list[str], agent) -> Task:
    """Return the research Task for the given topic."""
    sections_str = ", ".join(sections)
    return Task(
        description=(
            f"Research the topic: '{topic}'.\n"
            f"Focus on these sections: {sections_str}.\n"
            "Gather credible academic sources, key findings, and relevant data. "
            "Produce a structured research brief with source citations."
        ),
        expected_output=(
            "A structured research brief containing:\n"
            "1. Key concepts and definitions\n"
            "2. Current state of the art\n"
            "3. At least 5 cited academic sources (author, title, year, venue)\n"
            "4. Key findings relevant to each requested section"
        ),
        agent=agent,
    )
```

## Acceptance Criteria

- [ ] `build_research_task("AI", ["intro", "methods"], agent_mock)` returns a `crewai.Task`.
- [ ] Task `description` contains the topic string.
- [ ] Task `expected_output` mentions "cited academic sources".
- [ ] No hardcoded topic string in the task factory.
- [ ] File ≤ 150 lines (shared with tasks 012, 013, 014).

## Notes / Constraints

- All four task factory functions live in `services/tasks.py` to keep the file count manageable.
- The `agent` parameter is injected — do not instantiate agents inside task factories.
- `context` is not set here — context wiring happens in `build_crew()` (task 014).
