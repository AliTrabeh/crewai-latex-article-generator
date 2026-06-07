---
id: "001"
title: "Project Directory Structure"
group: "1 — Project Setup and Structure"
priority: critical
---

# Task 001 — Project Directory Structure

## Goal

Establish the complete directory skeleton that all subsequent tasks will populate. Every path referenced in later PRDs must exist before code is written.

## Files to Create or Modify

```
crewai-latex-article-generator/
├── src/
│   └── latex_article_generator/
│       ├── __init__.py
│       ├── constants.py
│       ├── services/
│       │   └── __init__.py
│       ├── shared/
│       │   └── __init__.py
│       └── sdk/
│           └── __init__.py
├── config/
│   ├── setup.json
│   ├── rate_limits.json
│   └── logging_config.json
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       └── __init__.py
├── docs/
│   ├── PLAN.md
│   ├── PRD.md
│   ├── TODO.md
│   └── prd/
├── data/
│   └── .gitkeep
├── results/
│   └── .gitkeep
├── assets/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── src/main.py
├── pyproject.toml
├── .env-example
├── .gitignore
└── README.md
```

## Exact Expected Behavior

- `uv run python src/main.py` executes without `ModuleNotFoundError`.
- All `__init__.py` files exist so that Python treats directories as packages.
- `data/`, `results/`, `assets/`, `notebooks/` are git-tracked via `.gitkeep` but their contents are ignored.

## Acceptance Criteria

- [ ] `git status` shows no unexpected untracked directories.
- [ ] `python -c "import latex_article_generator"` succeeds inside the `uv` env.
- [ ] `.gitignore` excludes `results/*`, `data/*`, `.env`, `__pycache__`, `.venv`.

## Notes / Constraints

- Do not place any business logic in `src/main.py` at this stage — entry point only.
- `services/`, `shared/`, `sdk/` subdirectories each need their own `__init__.py`.
- Empty `.gitkeep` files must be exactly 0 bytes (no content).
