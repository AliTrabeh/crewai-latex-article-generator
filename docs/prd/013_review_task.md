---
id: "013"
title: "Review Task"
group: "4 — CrewAI Tasks and Workflow"
priority: high
---

# Task 013 — Review Task

## Goal

Define the CrewAI `Task` that directs `ReviewerAgent` to review the drafted article and produce actionable feedback that is passed to the formatter.

## Files to Create or Modify

- `src/latex_article_generator/services/tasks.py` — add `build_review_task()`

## Exact Expected Behavior

```python
def build_review_task(agent, writing_task: Task) -> Task:
    """Return the review Task; depends on writing_task for context."""
    return Task(
        description=(
            "Review the drafted article sections for:\n"
            "1. Academic quality and clarity\n"
            "2. Logical flow between sections\n"
            "3. Citation accuracy and completeness\n"
            "4. Factual consistency with the research brief\n"
            "5. Correctness of Hebrew/RTL sections (if present)\n\n"
            "Produce an improved, final version of the article with all issues addressed."
        ),
        expected_output=(
            "The final, revised article text with all sections. "
            "Include a brief review summary (max 200 words) at the top noting what was changed."
        ),
        agent=agent,
        context=[writing_task],
    )
```

## Acceptance Criteria

- [ ] `build_review_task(agent_mock, writing_task_mock)` returns a `crewai.Task`.
- [ ] `task.context` contains `writing_task`.
- [ ] The `expected_output` specifies a review summary.
- [ ] File ≤ 150 lines (shared with other task factories).

## Notes / Constraints

- The reviewer produces the **final text** (improved draft), not just a list of comments. The formatter (task 014) receives this improved text.
- In v1.00, there is no iterative feedback loop — the reviewer improves the article in a single pass.
- The review summary at the top is stripped before LaTeX formatting.
