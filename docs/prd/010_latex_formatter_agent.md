---
id: "010"
title: "LaTeXFormatterAgent"
group: "3 — CrewAI Agents Design"
priority: high
status: NOT_STARTED
---

# Task 010 — LaTeXFormatterAgent

## Goal

Implement a CrewAI `Agent` that converts the reviewed article content into valid LaTeX markup, applying the correct document structure, packages, and formatting conventions.

## Files to Create or Modify

- `src/latex_article_generator/services/latex_formatter_agent.py` — agent factory function

## Exact Expected Behavior

```python
from crewai import Agent

def build_latex_formatter_agent(config: dict) -> Agent:
    """Return a configured LaTeXFormatterAgent."""
    return Agent(
        role="LaTeX Formatter",
        goal=(
            "Convert the reviewed article content into syntactically correct LaTeX markup. "
            "Apply proper document structure, section commands, citation commands, "
            "and BiDi directives for Hebrew text."
        ),
        backstory=(
            "You are an expert LaTeX typesetter with deep knowledge of academic paper "
            "formatting, BibTeX/biber citation management, and bidirectional text handling "
            "with polyglossia and bidi packages."
        ),
        tools=[],
        verbose=config.get("verbose", False),
        allow_delegation=False,
        max_iter=config.get("max_iter", 5),
    )
```

## Acceptance Criteria

- [ ] `build_latex_formatter_agent({})` returns a `crewai.Agent` without error.
- [ ] Agent `role` is exactly `"LaTeX Formatter"`.
- [ ] `allow_delegation` is `False`.
- [ ] Unit test confirms fields without LLM call.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- The formatter's output must be valid LaTeX — it will be piped directly to the compiler (task 027).
- The agent must be aware of LuaLaTeX-specific features (e.g., `fontspec`, `polyglossia`) — mention these in the backstory or goal prompt.
- BiDi (Hebrew/RTL) support is a hard requirement from the homework spec — the formatter must handle `\begin{RTL}...\end{RTL}` or equivalent.
