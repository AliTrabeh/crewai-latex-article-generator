# PLAN.md — Master Index

**Project:** CrewAI LaTeX Article Generator  
**Version:** 1.00  
**Last Updated:** 2026-06-07

---

## Implementation Order (Recommended)

Work through groups 1 → 12 in sequence. Within a group, tasks are numbered in dependency order.

---

## Group 1 — Project Setup and Structure

| # | PRD File | Description |
|---|----------|-------------|
| 1 | [001_project_structure.md](prd/001_project_structure.md) | Directory layout, `.gitkeep` files, git hygiene |
| 2 | [002_python_package_setup.md](prd/002_python_package_setup.md) | `pyproject.toml`, `uv`, `hatchling`, `ruff`, `pytest` |
| 3 | [003_version_tracking.md](prd/003_version_tracking.md) | `shared/version.py`, version consistency across code and config |

---

## Group 2 — Configuration and Environment Handling

| # | PRD File | Description |
|---|----------|-------------|
| 4 | [004_config_loader.md](prd/004_config_loader.md) | `ConfigManager` — reads JSON configs, validates version |
| 5 | [005_environment_variables.md](prd/005_environment_variables.md) | `.env-example`, secrets via `os.environ`, no hardcoding |
| 6 | [006_rate_limits_config.md](prd/006_rate_limits_config.md) | `rate_limits.json`, `RateLimitConfig` dataclass |

---

## Group 3 — CrewAI Agents Design

| # | PRD File | Description |
|---|----------|-------------|
| 7 | [007_researcher_agent.md](prd/007_researcher_agent.md) | ResearcherAgent — role, goal, backstory, tools |
| 8 | [008_writer_agent.md](prd/008_writer_agent.md) | WriterAgent — drafts article sections |
| 9 | [009_reviewer_agent.md](prd/009_reviewer_agent.md) | ReviewerAgent — reviews and critiques draft |
| 10 | [010_latex_formatter_agent.md](prd/010_latex_formatter_agent.md) | LaTeXFormatterAgent — converts content to LaTeX |

---

## Group 4 — CrewAI Tasks and Workflow

| # | PRD File | Description |
|---|----------|-------------|
| 11 | [011_research_task.md](prd/011_research_task.md) | Research task — topic investigation, source gathering |
| 12 | [012_writing_task.md](prd/012_writing_task.md) | Writing task — section drafting with context |
| 13 | [013_review_task.md](prd/013_review_task.md) | Review task — quality check, feedback loop |
| 14 | [014_crew_assembly.md](prd/014_crew_assembly.md) | Crew wiring — sequential process, agent+task linkage |

---

## Group 5 — Content Generation Pipeline

| # | PRD File | Description |
|---|----------|-------------|
| 15 | [015_sdk_pipeline.md](prd/015_sdk_pipeline.md) | `ArticleGeneratorSDK.generate_article()` — full pipeline |
| 16 | [016_api_gatekeeper_impl.md](prd/016_api_gatekeeper_impl.md) | `ApiGatekeeper` — rate limiting, FIFO queue, retry |
| 17 | [017_bidi_content_handler.md](prd/017_bidi_content_handler.md) | BiDi handler — Hebrew RTL + English LTR mixing |

---

## Group 6 — Assets Generation

| # | PRD File | Description |
|---|----------|-------------|
| 18 | [018_python_graph_generator.md](prd/018_python_graph_generator.md) | Matplotlib graphs — exported as `.pdf` or `.png` |
| 19 | [019_table_generator.md](prd/019_table_generator.md) | LaTeX table generator from structured data |
| 20 | [020_tikz_diagram_generator.md](prd/020_tikz_diagram_generator.md) | TikZ block diagrams and flowcharts |

---

## Group 7 — LaTeX Document Generation

| # | PRD File | Description |
|---|----------|-------------|
| 21 | [021_latex_template.md](prd/021_latex_template.md) | Base `.tex` template with preamble, packages |
| 22 | [022_cover_page.md](prd/022_cover_page.md) | Cover page — title, author, date, affiliation |
| 23 | [023_toc_headers_footers.md](prd/023_toc_headers_footers.md) | TOC, headers, footers, page numbering |
| 24 | [024_bibliography_generator.md](prd/024_bibliography_generator.md) | `.bib` file generation, `\cite{}` insertion |
| 25 | [025_latex_assembler.md](prd/025_latex_assembler.md) | Assembles all parts into final `.tex` document |

---

## Group 8 — PDF Compilation

| # | PRD File | Description |
|---|----------|-------------|
| 26 | [026_lualatex_compiler.md](prd/026_lualatex_compiler.md) | LuaLaTeX runner — single pass, error capture |
| 27 | [027_multi_pass_compiler.md](prd/027_multi_pass_compiler.md) | 4-pass orchestration: lualatex→biber→lualatex→lualatex |
| 28 | [028_biber_runner.md](prd/028_biber_runner.md) | Biber runner — bibliography processing between passes |

---

## Group 9 — Validation and Checking System

| # | PRD File | Description |
|---|----------|-------------|
| 29 | [029_latex_validator.md](prd/029_latex_validator.md) | LaTeX source validation — balanced braces, required sections |
| 30 | [030_pdf_validator.md](prd/030_pdf_validator.md) | PDF output validation — page count, file size, readability |
| 31 | [031_content_completeness_checker.md](prd/031_content_completeness_checker.md) | Content checker — all required sections present, min lengths |

---

## Group 10 — CLI Entry Point

| # | PRD File | Description |
|---|----------|-------------|
| 32 | [032_cli_argument_parser.md](prd/032_cli_argument_parser.md) | `argparse` CLI — `--topic`, `--output`, `--format` flags |
| 33 | [033_cli_main_entrypoint.md](prd/033_cli_main_entrypoint.md) | `src/main.py` — wires CLI args to SDK, handles exit codes |

---

## Group 11 — Documentation

| # | PRD File | Description |
|---|----------|-------------|
| 34 | [034_readme_final.md](prd/034_readme_final.md) | Final `README.md` — install, usage, examples, config guide |
| 35 | [035_prompts_engineering_log.md](prd/035_prompts_engineering_log.md) | `docs/prompts_log.md` — prompt iteration history |
| 36 | [036_cost_analysis.md](prd/036_cost_analysis.md) | `docs/cost_analysis.md` — token usage table, cost estimates |

---

## Group 12 — Testing and Final Submission Cleanup

| # | PRD File | Description |
|---|----------|-------------|
| 37 | [037_unit_tests_agents.md](prd/037_unit_tests_agents.md) | Unit tests for all CrewAI agent classes |
| 38 | [038_unit_tests_services.md](prd/038_unit_tests_services.md) | Unit tests for services (config, gatekeeper, bidi) |
| 39 | [039_unit_tests_latex.md](prd/039_unit_tests_latex.md) | Unit tests for LaTeX generation and compilation |
| 40 | [040_integration_tests.md](prd/040_integration_tests.md) | End-to-end integration test — topic → PDF |
| 41 | [041_submission_cleanup.md](prd/041_submission_cleanup.md) | Final cleanup — ruff zero errors, ≥85% coverage, zip |

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
