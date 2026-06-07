---
id: "034"
title: "Final README"
group: "11 — Documentation"
priority: high
---

# Task 034 — Final README

## Goal

Update `README.md` to serve as a complete user manual: installation instructions, usage examples, configuration guide, and contribution guidelines. The README is evaluated as part of the submission.

## Files to Create or Modify

- `README.md` — full rewrite with real content

## Exact Expected Behavior

The README must contain all of the following sections:

1. **Project Description** — what the tool does, key features
2. **Requirements** — Python ≥ 3.10, MiKTeX/TeX Live with LuaLaTeX, biber, uv
3. **Installation**
   ```bash
   git clone <repo>
   cd crewai-latex-article-generator
   uv sync --all-extras
   cp .env-example .env
   # edit .env with your API keys
   ```
4. **Usage**
   ```bash
   uv run python src/main.py --topic "Transformer architectures" --format pdf
   uv run python src/main.py --topic "AI" --sections introduction methodology --format latex
   ```
5. **Configuration** — explain `config/setup.json`, `config/rate_limits.json`
6. **Project Structure** — directory tree with explanations
7. **Running Tests**
   ```bash
   uv run pytest tests/ --cov
   ```
8. **Contributing** — code style (ruff), TDD requirement, 150 LOC limit per file
9. **License** — MIT (or as required by instructor)

## Acceptance Criteria

- [ ] All 9 sections present.
- [ ] Installation instructions use `uv sync` (not `pip install`).
- [ ] At least two usage examples shown.
- [ ] `uv run pytest` command present in "Running Tests" section.
- [ ] No placeholder text remaining (no "TODO" or "lorem ipsum").

## Notes / Constraints

- README is part of the graded submission — treat it as formal documentation.
- Do not include real API keys anywhere in the README.
- Screenshots of the terminal output and the generated PDF are a bonus but not required for v1.00.
