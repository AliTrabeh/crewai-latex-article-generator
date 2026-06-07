# PLAN.md — Master Index

**Project:** CrewAI LaTeX Article Generator  
**Version:** 1.00  
**Last Updated:** 2026-06-07

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| `NOT_STARTED` | Task not yet begun |
| `IN_PROGRESS` | Task actively being worked on |
| `DONE` | Task fully implemented and tests passing |

---

## Implementation Order (Recommended)

Work through groups 1 → 12 in sequence. Within a group, tasks are numbered in dependency order.

---

## Group 1 — Project Setup and Structure

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 1 | [001_project_structure.md](prd/001_project_structure.md) | Directory layout, `.gitkeep` files, git hygiene | DONE |
| 2 | [002_python_package_setup.md](prd/002_python_package_setup.md) | `pyproject.toml`, `uv`, `hatchling`, `ruff`, `pytest` | NOT_STARTED |
| 3 | [003_version_tracking.md](prd/003_version_tracking.md) | `shared/version.py`, version consistency across code and config | NOT_STARTED |

---

## Group 2 — Configuration and Environment Handling

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 4 | [004_config_loader.md](prd/004_config_loader.md) | `ConfigManager` — reads JSON configs, validates version | NOT_STARTED |
| 5 | [005_environment_variables.md](prd/005_environment_variables.md) | `.env-example`, secrets via `os.environ`, no hardcoding | NOT_STARTED |
| 6 | [006_rate_limits_config.md](prd/006_rate_limits_config.md) | `rate_limits.json`, `RateLimitConfig` dataclass | NOT_STARTED |

---

## Group 3 — CrewAI Agents Design

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 7 | [007_researcher_agent.md](prd/007_researcher_agent.md) | ResearcherAgent — role, goal, backstory, tools | NOT_STARTED |
| 8 | [008_writer_agent.md](prd/008_writer_agent.md) | WriterAgent — drafts article sections | NOT_STARTED |
| 9 | [009_reviewer_agent.md](prd/009_reviewer_agent.md) | ReviewerAgent — reviews and critiques draft | NOT_STARTED |
| 10 | [010_latex_formatter_agent.md](prd/010_latex_formatter_agent.md) | LaTeXFormatterAgent — converts content to LaTeX | NOT_STARTED |

---

## Group 4 — CrewAI Tasks and Workflow

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 11 | [011_research_task.md](prd/011_research_task.md) | Research task — topic investigation, source gathering | NOT_STARTED |
| 12 | [012_writing_task.md](prd/012_writing_task.md) | Writing task — section drafting with context | NOT_STARTED |
| 13 | [013_review_task.md](prd/013_review_task.md) | Review task — quality check, feedback loop | NOT_STARTED |
| 14 | [014_crew_assembly.md](prd/014_crew_assembly.md) | Crew wiring — sequential process, agent+task linkage | NOT_STARTED |

---

## Group 5 — Content Generation Pipeline

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 15 | [015_sdk_pipeline.md](prd/015_sdk_pipeline.md) | `ArticleGeneratorSDK.generate_article()` — full pipeline | NOT_STARTED |
| 16 | [016_api_gatekeeper_impl.md](prd/016_api_gatekeeper_impl.md) | `ApiGatekeeper` — rate limiting, FIFO queue, retry | NOT_STARTED |
| 17 | [017_bidi_content_handler.md](prd/017_bidi_content_handler.md) | BiDi handler — Hebrew RTL + English LTR mixing | NOT_STARTED |

---

## Group 6 — Assets Generation

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 18 | [018_python_graph_generator.md](prd/018_python_graph_generator.md) | Matplotlib graphs — exported as `.pdf` or `.png` | NOT_STARTED |
| 19 | [019_table_generator.md](prd/019_table_generator.md) | LaTeX table generator from structured data | NOT_STARTED |
| 20 | [020_tikz_diagram_generator.md](prd/020_tikz_diagram_generator.md) | TikZ block diagrams and flowcharts | NOT_STARTED |

---

## Group 7 — LaTeX Document Generation

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 21 | [021_latex_template.md](prd/021_latex_template.md) | Base `.tex` template with preamble, packages | NOT_STARTED |
| 22 | [022_cover_page.md](prd/022_cover_page.md) | Cover page — title, author, date, affiliation | NOT_STARTED |
| 23 | [023_toc_headers_footers.md](prd/023_toc_headers_footers.md) | TOC, headers, footers, page numbering | NOT_STARTED |
| 24 | [024_bibliography_generator.md](prd/024_bibliography_generator.md) | `.bib` file generation, `\cite{}` insertion | NOT_STARTED |
| 25 | [025_latex_assembler.md](prd/025_latex_assembler.md) | Assembles all parts into final `.tex` document | NOT_STARTED |

---

## Group 8 — PDF Compilation

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 26 | [026_lualatex_compiler.md](prd/026_lualatex_compiler.md) | LuaLaTeX runner — single pass, error capture | NOT_STARTED |
| 27 | [027_multi_pass_compiler.md](prd/027_multi_pass_compiler.md) | 4-pass orchestration: lualatex→biber→lualatex→lualatex | NOT_STARTED |
| 28 | [028_biber_runner.md](prd/028_biber_runner.md) | Biber runner — bibliography processing between passes | NOT_STARTED |

---

## Group 9 — Validation and Checking System

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 29 | [029_latex_validator.md](prd/029_latex_validator.md) | LaTeX source validation — balanced braces, required sections | NOT_STARTED |
| 30 | [030_pdf_validator.md](prd/030_pdf_validator.md) | PDF output validation — page count, file size, readability | NOT_STARTED |
| 31 | [031_content_completeness_checker.md](prd/031_content_completeness_checker.md) | Content checker — all required sections present, min lengths | NOT_STARTED |

---

## Group 10 — CLI Entry Point

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 32 | [032_cli_argument_parser.md](prd/032_cli_argument_parser.md) | `argparse` CLI — `--topic`, `--output`, `--format` flags | NOT_STARTED |
| 33 | [033_cli_main_entrypoint.md](prd/033_cli_main_entrypoint.md) | `src/main.py` — wires CLI args to SDK, handles exit codes | NOT_STARTED |

---

## Group 11 — Documentation

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 34 | [034_readme_final.md](prd/034_readme_final.md) | Final `README.md` — install, usage, examples, config guide | NOT_STARTED |
| 35 | [035_prompts_engineering_log.md](prd/035_prompts_engineering_log.md) | `docs/prompts_log.md` — prompt iteration history | NOT_STARTED |
| 36 | [036_cost_analysis.md](prd/036_cost_analysis.md) | `docs/cost_analysis.md` — token usage table, cost estimates | NOT_STARTED |

---

## Group 12 — Testing and Final Submission Cleanup

| # | PRD File | Description | Status |
|---|----------|-------------|--------|
| 37 | [037_unit_tests_agents.md](prd/037_unit_tests_agents.md) | Unit tests for all CrewAI agent classes | NOT_STARTED |
| 38 | [038_unit_tests_services.md](prd/038_unit_tests_services.md) | Unit tests for services (config, gatekeeper, bidi) | NOT_STARTED |
| 39 | [039_unit_tests_latex.md](prd/039_unit_tests_latex.md) | Unit tests for LaTeX generation and compilation | NOT_STARTED |
| 40 | [040_integration_tests.md](prd/040_integration_tests.md) | End-to-end integration test — topic → PDF | NOT_STARTED |
| 41 | [041_submission_cleanup.md](prd/041_submission_cleanup.md) | Final cleanup — ruff zero errors, ≥85% coverage, zip | NOT_STARTED |

---

## Status Summary

| Status | Count |
|--------|-------|
| DONE | 1 |
| IN_PROGRESS | 0 |
| NOT_STARTED | 40 |

---

## Dependency Graph

```
Group 1 (structure) → Group 2 (config) → Group 3 (agents) → Group 4 (tasks)
                                        ↘                   ↗
                                         Group 5 (pipeline)
                                                ↓
                           Group 6 (assets) → Group 7 (LaTeX) → Group 8 (PDF)
                                                                       ↓
                                                     Group 9 (validation) → Group 10 (CLI)
                                                                                   ↓
                                                                 Group 11 (docs) + Group 12 (tests)
```

**Start with:** [`001_project_structure.md`](prd/001_project_structure.md)

---

## Architecture Reference (preserved)

### C4 Context

```
[User / CLI]
     |
     v
[ArticleGeneratorSDK]   <-- single entry point for all logic
     |
     v
[CrewAI Orchestrator]   <-- coordinates multiple AI agents
  ├── ResearchAgent
  ├── WriterAgent
  ├── ReviewerAgent
  └── FormatterAgent
     |
     v
[External APIs]         <-- OpenAI / Anthropic (via ApiGatekeeper)
```

### ADR-001: SDK Architecture
All business logic is accessible only through `ArticleGeneratorSDK`. CLI, REST, GUI consume SDK only.

### ADR-002: uv as Package Manager
`uv` exclusively; `pip install` is forbidden per submission guidelines.

### ADR-003: Config-driven Rate Limits
All rate limits live in `config/rate_limits.json`; no hardcoded values in source.
