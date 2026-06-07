---
id: "038"
title: "Unit Tests — Services"
group: "12 — Testing and Final Submission Cleanup"
priority: high
status: DONE
---

# Task 038 — Unit Tests for Services

## Goal

Write unit tests for `ConfigManager`, `ApiGatekeeper`, `BiDiHandler`, `TableGenerator`, `TikZGenerator`, `GraphGenerator`, `CoverPageGenerator`, `TocFormatter`, `BibliographyGenerator`, and `ContentCompletenessChecker`.

## Files to Create or Modify

- `tests/unit/test_config.py` — ConfigManager tests
- `tests/unit/test_gatekeeper.py` — ApiGatekeeper tests
- `tests/unit/test_bidi.py` — BiDiHandler tests
- `tests/unit/test_generators.py` — table, tikz, graph, cover, toc, bibliography tests
- `tests/unit/test_validators.py` — LatexValidator, PdfValidator, ContentCompletenessChecker tests

## Exact Expected Behavior

Key test cases to implement:

**ConfigManager:**
- Valid config dir → loads without error
- Version mismatch → `RuntimeError`
- `get("app_name")` → correct string
- Missing JSON file → `FileNotFoundError`

**ApiGatekeeper:**
- `execute(lambda: 42)` → `42`
- Retry on exception → retries `max_retries` times
- `get_queue_status()` → `QueueStatus` with correct counts
- Exceeding rate limit → `_wait_for_capacity` is called

**BiDiHandler:**
- Hebrew text → wrapped in `\begin{RTL}...\end{RTL}`
- English-only → passes unchanged
- `contains_hebrew("עברית")` → `True`

**Validators:**
- Valid LaTeX → no errors
- Missing `\begin{document}` → error
- Unbalanced braces → error

## Acceptance Criteria

- [ ] Each service module has at least 4 unit tests.
- [ ] All tests use mocking where external I/O is involved.
- [ ] `uv run pytest tests/unit/ --cov` shows ≥ 85% coverage.
- [ ] No test takes longer than 1 second (mock all I/O and sleep calls).

## Notes / Constraints

- Mock `time.sleep` and `time.monotonic` in gatekeeper tests to avoid slow tests.
- For `ConfigManager`, create a temporary JSON config dir in `tmp_path` (pytest fixture).
- `GraphGenerator` tests should mock `matplotlib.pyplot.savefig` to avoid filesystem side effects.
