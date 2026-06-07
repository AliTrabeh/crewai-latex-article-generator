---
id: "037"
title: "Unit Tests — CrewAI Agents"
group: "12 — Testing and Final Submission Cleanup"
priority: high
---

# Task 037 — Unit Tests for CrewAI Agents

## Goal

Write unit tests for all four agent factory functions. Tests must verify agent configuration without making LLM API calls.

## Files to Create or Modify

- `tests/unit/test_agents.py` — unit tests for all four agents

## Exact Expected Behavior

```python
from unittest.mock import patch, MagicMock
import pytest
from latex_article_generator.services.researcher_agent import build_researcher_agent
from latex_article_generator.services.writer_agent import build_writer_agent
from latex_article_generator.services.reviewer_agent import build_reviewer_agent
from latex_article_generator.services.latex_formatter_agent import build_latex_formatter_agent

@patch("latex_article_generator.services.researcher_agent.SerperDevTool")
def test_researcher_agent_role(mock_tool):
    agent = build_researcher_agent({})
    assert agent.role == "Academic Researcher"

@patch("latex_article_generator.services.researcher_agent.SerperDevTool")
def test_researcher_agent_no_delegation(mock_tool):
    agent = build_researcher_agent({})
    assert agent.allow_delegation is False

def test_writer_agent_no_tools():
    agent = build_writer_agent({})
    assert agent.tools == []

def test_reviewer_agent_max_iter_default():
    agent = build_reviewer_agent({})
    assert agent.max_iter == 3

def test_latex_formatter_role():
    agent = build_latex_formatter_agent({})
    assert agent.role == "LaTeX Formatter"
```

## Acceptance Criteria

- [ ] All four agents have at least 2 unit tests each (8 tests minimum).
- [ ] No real API calls — `SerperDevTool` is mocked.
- [ ] All tests pass with `uv run pytest tests/unit/test_agents.py`.
- [ ] Coverage for agent modules ≥ 85%.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Use `unittest.mock.patch` at the module level where the tool is imported, not where it is defined.
- Test only configuration attributes — do not call `agent.execute()` or any LLM method.
- `conftest.py` fixtures (`test_rate_limit_config`, `gatekeeper`) are available for shared setup.
