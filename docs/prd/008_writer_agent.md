---
id: "008"
title: "WriterAgent"
group: "3 — CrewAI Agents Design"
priority: high
---

# Task 008 — WriterAgent

## Goal

Implement a CrewAI `Agent` that drafts full article sections from the research brief. The agent must produce prose that is structured for academic publication and compatible with LaTeX formatting downstream.

## Files to Create or Modify

- `src/latex_article_generator/services/writer_agent.py` — agent factory function

## Exact Expected Behavior

```python
from crewai import Agent

def build_writer_agent(config: dict) -> Agent:
    """Return a configured WriterAgent."""
    return Agent(
        role="Academic Writer",
        goal=(
            "Draft clear, well-structured academic article sections "
            "based on the provided research brief."
        ),
        backstory=(
            "You are an experienced academic writer skilled in producing "
            "publication-ready prose for computer science and engineering papers."
        ),
        tools=[],
        verbose=config.get("verbose", False),
        allow_delegation=False,
        max_iter=config.get("max_iter", 5),
    )
```

The writer agent has no tools — it relies entirely on the research context passed via task `context`.

## Acceptance Criteria

- [ ] `build_writer_agent({})` returns a `crewai.Agent` instance without error.
- [ ] Agent `role` is exactly `"Academic Writer"`.
- [ ] `agent.tools` is an empty list.
- [ ] `allow_delegation` is `False`.
- [ ] Unit test verifies the agent fields without any LLM call.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- The writer must receive the research task output via `Task(context=[research_task])` — not via a tool.
- Do not hardcode the article topic in the agent definition — topics are passed at task creation time.
- The agent must be capable of generating content with both English and Hebrew sections (BiDi) when requested.
