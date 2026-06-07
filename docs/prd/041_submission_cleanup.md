---
id: "041"
title: "Final Submission Cleanup"
group: "12 — Testing and Final Submission Cleanup"
priority: critical
status: DONE
---

# Task 041 — Final Submission Cleanup

## Goal

Perform all pre-submission quality checks, fix any remaining issues, and package the project for submission according to the software submission guidelines.

## Files to Create or Modify

- All source files — fix any ruff errors
- `docs/TODO.md` — mark all completed tasks
- `docs/cost_analysis.md` — fill with real run data
- `docs/prompts_log.md` — finalize all entries
- `README.md` — verify completeness
- Submission ZIP file (if required)

## Exact Expected Behavior

Run these checks in order and fix all failures before submitting:

**Step 1 — Linting (zero tolerance):**
```bash
uv run ruff check src/ tests/
```
Expected: no output (zero errors).

**Step 2 — Test coverage:**
```bash
uv run pytest tests/ --cov --cov-fail-under=85
```
Expected: all tests pass, coverage ≥ 85%.

**Step 3 — Import check:**
```bash
uv run python -c "from latex_article_generator.sdk.sdk import ArticleGeneratorSDK; print('OK')"
```
Expected: prints `OK`.

**Step 4 — Version consistency:**
```bash
uv run python -c "
from latex_article_generator import __version__
from latex_article_generator.shared.config import ConfigManager
cm = ConfigManager()
print(__version__, cm.get('version') or 'no version key')
"
```
Expected: both print `1.00`.

**Step 5 — Submission packaging (if ZIP required):**
```bash
zip -r submission.zip . \
  --exclude ".venv/*" \
  --exclude ".git/*" \
  --exclude "__pycache__/*" \
  --exclude "results/*" \
  --exclude "data/*" \
  --exclude ".env"
```

## Acceptance Criteria

- [ ] `uv run ruff check src/ tests/` exits 0 with no output.
- [ ] `uv run pytest --cov-fail-under=85` exits 0.
- [ ] No file in `src/` exceeds 150 lines.
- [ ] No hardcoded API keys in any committed file.
- [ ] `docs/prompts_log.md` has ≥ 2 versions per agent.
- [ ] `docs/cost_analysis.md` has a real token usage table.
- [ ] `README.md` is complete with real usage examples.
- [ ] Submission ZIP excludes `.env`, `.venv/`, `results/`, `data/`.

## Notes / Constraints

- Run all checks on a clean clone (`git clone` to a new directory) to catch missing files.
- The submission guidelines require a PDF of the generated article to be included — run a real article generation and include the output PDF.
- Version in all three JSON configs + `shared/version.py` + `pyproject.toml` must all read `"1.00"`.
- Check for any `print()` debug statements left in production code — remove them all.
