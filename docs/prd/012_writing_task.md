---
id: "012"
title: "Writing Task"
group: "4 — CrewAI Tasks and Workflow"
priority: high
status: DONE
---

# Task 012 — Writing Task

## Goal

Define the CrewAI `Task` that directs `WriterAgent` to draft all requested article sections using the research brief as context.

## Files to Create or Modify

- `src/latex_article_generator/services/tasks.py` — add `build_writing_task()`

## Exact Expected Behavior

```python
def build_writing_task(topic: str, sections: list[str], agent, research_task: Task) -> Task:
    """Return the writing Task; depends on research_task for context."""
    sections_str = ", ".join(sections)
    return Task(
        description=(
            f"Write the following sections of an academic article about '{topic}':\n"
            f"{sections_str}\n\n"
            "Use the research brief from the previous task as your source. "
            "Write in clear academic English. Include in-text citations. "
            "If a section requires Hebrew content, write it in Hebrew with proper RTL formatting."
        ),
        expected_output=(
            "Complete prose for each requested section, clearly delimited by section name. "
            "Each section must be at least 300 words. "
            "Citations must be in the format [Author, Year]."
        ),
        agent=agent,
        context=[research_task],
    )
```

## Acceptance Criteria

- [ ] `build_writing_task("AI", ["intro"], agent_mock, research_task_mock)` returns a `crewai.Task`.
- [ ] `task.context` contains `research_task`.
- [ ] Task `expected_output` specifies minimum word count.
- [ ] File ≤ 150 lines (shared with other task factories).

## Notes / Constraints

- The `context=[research_task]` wiring is essential — without it, CrewAI does not pass the research output to the writer.
- Minimum 300 words per section is a homework requirement.
- Hebrew section requirement: at least one section demonstrating BiDi must be included in the final article.
