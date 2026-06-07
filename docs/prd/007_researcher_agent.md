---
id: "007"
title: "ResearcherAgent"
group: "3 — CrewAI Agents Design"
priority: high
status: DONE
---

# Task 007 — ResearcherAgent

## Goal

Implement a CrewAI `Agent` that investigates the requested topic, gathers credible sources, and produces a structured research brief used by the WriterAgent.

## Files to Create or Modify

- `src/latex_article_generator/services/researcher_agent.py` — agent factory function

## Exact Expected Behavior

```python
from crewai import Agent
from crewai_tools import SerperDevTool

def build_researcher_agent(config: dict) -> Agent:
    """Return a configured ResearcherAgent."""
    return Agent(
        role="Academic Researcher",
        goal=(
            "Thoroughly investigate the given topic and gather credible, "
            "up-to-date academic and technical sources."
        ),
        backstory=(
            "You are a meticulous academic researcher with expertise in "
            "literature review, source verification, and structured knowledge synthesis."
        ),
        tools=[SerperDevTool()],
        verbose=config.get("verbose", False),
        allow_delegation=False,
        max_iter=config.get("max_iter", 5),
    )
```

The function accepts a `config` dict so settings (verbosity, iteration limits) come from `ConfigManager`, not hardcoded values.

## Acceptance Criteria

- [x] `build_researcher_agent({})` returns a `crewai.Agent` instance without error.
- [x] Agent `role` is exactly `"Academic Researcher"`.
- [x] `SerperDevTool` is in `agent.tools`.
- [x] `allow_delegation` is `False`.
- [x] Unit test mocks `SerperDevTool` to avoid network calls.
- [x] File ≤ 150 lines.

## Notes / Constraints

- `SerperDevTool` requires `SERPER_API_KEY` in the environment — the test must mock or skip if the key is absent.
- Do not instantiate the agent at module import time — always use the factory function.
- If `crewai_tools` is not yet a dependency, add it with `uv add crewai-tools`.
