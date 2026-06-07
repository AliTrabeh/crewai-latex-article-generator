# Task Tracking — TODO

**Project:** CrewAI LaTeX Article Generator  
**Version:** 1.00

---

## Phase 1 — Documentation & Planning
- [x] Create `docs/PRD.md` — product requirements
- [x] Create `docs/PLAN.md` — architecture & planning
- [x] Create `docs/TODO.md` — this file
- [x] Create `README.md`
- [ ] Approval of all docs before development begins

## Phase 2 — Project Structure
- [x] Create recommended directory structure (sec. 2.4)
- [x] Create `pyproject.toml` with `uv`, `ruff`, `pytest` config
- [x] Create `.env-example` with placeholder keys
- [x] Create `.gitignore`
- [x] Create `config/setup.json`, `rate_limits.json`, `logging_config.json`
- [x] Create `src/latex_article_generator/__init__.py` with `__version__`
- [x] Create `shared/version.py`, `shared/config.py`, `shared/gatekeeper.py`
- [x] Create `sdk/sdk.py` — SDK skeleton
- [x] Create `src/main.py` — entry point
- [x] Create `tests/conftest.py`

## Phase 3 — Core Implementation (TDD)
- [ ] `PRD_crewai_orchestration.md` — per-mechanism PRD
- [ ] `services/research_service.py` — ResearchAgent service
- [ ] `services/writer_service.py` — WriterAgent service
- [ ] `services/reviewer_service.py` — ReviewerAgent service
- [ ] `services/formatter_service.py` — LaTeX formatting service
- [ ] `sdk/sdk.py` — implement `generate_article()` and `compile_pdf()`
- [ ] Unit tests for all services (≥ 85% coverage)
- [ ] Integration tests for full pipeline

## Phase 4 — Quality & Polish
- [ ] `uv run ruff check src/` — zero errors
- [ ] `uv run pytest tests/ --cov` — ≥ 85% coverage
- [ ] Update `README.md` with real usage examples and screenshots
- [ ] Prompt engineering log (`docs/prompts_log.md`)
- [ ] Cost analysis (token usage table)

---

## Definition of Done (per task)
1. Code written following TDD (Red → Green → Refactor)
2. File ≤ 150 lines of code
3. Docstrings on every public method/class
4. `ruff check` passes with 0 errors
5. Unit test(s) written and passing
6. Coverage ≥ 85% maintained
