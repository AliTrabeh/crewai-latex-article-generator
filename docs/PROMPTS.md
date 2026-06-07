# PROMPTS.md — Prompt Engineering Reference

**Project:** CrewAI LaTeX Article Generator  
**Version:** 1.00  
**Last Updated:** 2026-06-07

---

## 1. Main Project Planning Prompt

Used to generate the full PRD, architecture decisions, and implementation plan.

```
You are a senior software architect. I need a detailed implementation plan for a Python project called "CrewAI LaTeX Article Generator".

The system must:
- Accept a topic as CLI input
- Use CrewAI to orchestrate multiple AI agents (Researcher, Writer, Reviewer, LaTeXFormatter)
- Generate a full academic-style LaTeX article with cover page, TOC, bibliography, graphs, and TikZ diagrams
- Support Hebrew (RTL) and English (LTR) mixed content via LuaLaTeX
- Compile to a valid PDF using a 4-pass pipeline: lualatex → biber → lualatex → lualatex
- Expose all functionality through a single SDK class: ArticleGeneratorSDK
- Be fully testable with ≥85% coverage using pytest

Constraints:
- Python 3.11+
- Use uv as the package manager (no pip)
- Use ruff for linting (zero errors tolerance)
- All rate limits in config/rate_limits.json (no hardcoded values)
- No file in src/ should exceed 150 lines
- All secrets via environment variables (.env), never committed

Produce:
1. A complete PRD (docs/PRD.md)
2. A phased implementation plan (docs/PLAN.md) with 41 granular tasks organized in 12 groups
3. Individual PRD files for each task in docs/prd/001_*.md through docs/prd/041_*.md
4. A TODO tracking file (docs/TODO.md)
```

---

## 2. Project Structure Creation Prompt

Used to scaffold the initial directory and file skeleton.

```
You are a Python project scaffolding expert. Create the initial directory structure for the CrewAI LaTeX Article Generator project.

Project root: crewai-latex-article-generator/

Required structure:
- src/latex_article_generator/ with __init__.py, constants.py
  - services/__init__.py
  - shared/__init__.py
  - sdk/__init__.py
- config/ with setup.json, rate_limits.json, logging_config.json
- tests/ with __init__.py
  - unit/__init__.py
  - integration/__init__.py
- docs/ with PLAN.md, PRD.md, TODO.md, PROMPTS.md
  - prd/ (41 individual task files)
- data/.gitkeep, results/.gitkeep, assets/.gitkeep, notebooks/.gitkeep
- pyproject.toml (uv + hatchling + ruff + pytest)
- .env-example, .gitignore, README.md, src/main.py

Rules:
- All __init__.py files must exist so Python treats directories as packages
- .gitkeep files must be exactly 0 bytes
- pyproject.toml uses hatchling as build backend
- ruff configured with line-length=100, select=["E","F","I"]
- pytest configured with testpaths=["tests"], addopts="--tb=short"

Do not add any business logic yet — structure only.
```

---

## 3. Reusable Prompt Template — Implement One PRD Task

Use this template each time you start implementing a single PRD task. Replace `{NNN}` with the task number and fill in the specifics.

```
Implement PRD task {NNN}: {TASK_TITLE}

Context:
- PRD file: docs/prd/{NNN}_{task_slug}.md
- Group: {GROUP_NAME}
- Dependencies already done: {LIST_COMPLETED_DEPS}

Rules (non-negotiable):
1. Follow TDD: write the test first (Red), then implement (Green), then refactor.
2. The implementation file must be ≤150 lines.
3. All public classes and functions must have a one-line docstring.
4. No hardcoded config values — read from ConfigManager or environment variables.
5. Run `uv run ruff check src/ tests/` before reporting done — must exit 0.
6. Run `uv run pytest tests/ -x` before reporting done — all tests must pass.

Deliver:
- The implementation file at the path specified in the PRD
- The test file in tests/unit/ or tests/integration/ as appropriate
- Update docs/TODO.md: mark task {NNN} as [x] done
- Update docs/prd/{NNN}_*.md: change Status to DONE

Do not implement anything outside the scope of this single PRD task.
```

---

## 4. Reusable Prompt Template — Review and Fix One Completed Task

Use this template after implementing a task to verify correctness and fix any issues before moving on.

```
Review and fix the implementation of PRD task {NNN}: {TASK_TITLE}

Files to review:
- Implementation: {IMPLEMENTATION_FILE_PATH}
- Tests: {TEST_FILE_PATH}
- PRD spec: docs/prd/{NNN}_{task_slug}.md

Checklist to verify (fix anything that fails):
1. [ ] All acceptance criteria in the PRD are met — check each criterion explicitly.
2. [ ] File is ≤150 lines — if over, refactor without changing behavior.
3. [ ] `uv run ruff check {IMPLEMENTATION_FILE_PATH}` exits 0.
4. [ ] `uv run pytest {TEST_FILE_PATH} -v` — all tests pass.
5. [ ] No hardcoded secrets, API keys, or magic numbers.
6. [ ] Public interface matches exactly what later PRD tasks expect to import.
7. [ ] Edge cases are tested: empty input, None values, invalid config.

If issues found:
- Fix the implementation first, then adjust tests only if the spec changed.
- Do not add features beyond what the PRD specifies.
- Re-run ruff and pytest after every fix.

Report: list each criterion as PASS or FAIL with a one-line explanation.
If all pass, confirm: "Task {NNN} is complete and ready for the next task."
```
