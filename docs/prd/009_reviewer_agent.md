---
id: "009"
title: "ReviewerAgent"
group: "3 — CrewAI Agents Design"
priority: high
status: NOT_STARTED
---

# Task 009 — ReviewerAgent

## Goal

Implement a CrewAI `Agent` that critically reviews the drafted article for academic quality, logical consistency, and completeness, then produces actionable feedback.

## Files to Create or Modify

- `src/latex_article_generator/services/reviewer_agent.py` — agent factory function

## Exact Expected Behavior

```python
from crewai import Agent

def build_reviewer_agent(config: dict) -> Agent:
    """Return a configured ReviewerAgent."""
    return Agent(
        role="Academic Reviewer",
        goal=(
            "Review the drafted article sections for academic quality, "
            "logical consistency, completeness, and citation accuracy. "
            "Provide specific, actionable feedback."
        ),
        backstory=(
            "You are a rigorous peer reviewer for top-tier academic conferences, "
            "known for thorough and constructive critique."
        ),
        tools=[],
        verbose=config.get("verbose", False),
        allow_delegation=False,
        max_iter=config.get("max_iter", 3),
    )
```

## Acceptance Criteria

- [ ] `build_reviewer_agent({})` returns a `crewai.Agent` without error.
- [ ] Agent `role` is exactly `"Academic Reviewer"`.
- [ ] `allow_delegation` is `False`.
- [ ] `max_iter` defaults to `3` (fewer iterations needed — review is a single pass).
- [ ] Unit test confirms fields without LLM call.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- The review task (task 013) will pass writer output via `context` — the reviewer does not call any tools.
- In the sequential crew process, the reviewer runs after the writer, so it naturally receives the writer's output as context.
- Do not implement a feedback loop (multiple review passes) in v1.00 — single review pass only.
