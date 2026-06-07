# CrewAI LaTeX Article Generator

A multi-agent system built with [CrewAI](https://crewai.com) that automatically generates well-structured, fully compiled academic articles in LaTeX format. Four specialized AI agents — Researcher, Writer, Reviewer, and LaTeX Formatter — collaborate in a sequential pipeline to produce publication-ready PDF documents with proper citations, BiDi (Hebrew/English) support, TikZ diagrams, and a complete bibliography.

**Key features:**
- Multi-agent CrewAI pipeline with 4-pass LuaLaTeX compilation
- Hebrew (RTL) / English (LTR) BiDi mixing via `polyglossia`
- Automatic `.bib` generation and `biber` bibliography processing
- Matplotlib graphs, LaTeX tables, and TikZ diagrams
- Rate-limited OpenAI API access with retry logic
- Full validation: LaTeX source, PDF output, content completeness

---

## Requirements

| Requirement | Version |
|---|---|
| Python | ≥ 3.10 |
| [uv](https://docs.astral.sh/uv/) | ≥ 0.4.0 |
| MiKTeX or TeX Live | any recent (LuaLaTeX + biber required) |
| OpenAI API key | GPT-4o recommended |
| Serper API key | for ResearcherAgent web search |

`lualatex` and `biber` must be on your system `PATH`. Verify with:
```bash
lualatex --version
biber --version
```

---

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd crewai-latex-article-generator

# 2. Install all dependencies (do NOT use pip install)
uv sync --all-extras

# 3. Copy the environment template and add your API keys
cp .env-example .env
# Edit .env — at minimum set OPENAI_API_KEY and SERPER_API_KEY

# 4. Verify the installation
uv run pytest tests/ --no-cov -q
```

---

## Usage

**Generate a PDF article:**
```bash
uv run python src/main.py --topic "Transformer architectures in NLP" --format pdf
```

**Generate LaTeX source only (no compilation):**
```bash
uv run python src/main.py --topic "Federated Learning" --format latex --output results/fl.pdf
```

**Specify custom sections:**
```bash
uv run python src/main.py \
  --topic "Quantum Computing" \
  --sections introduction background methodology results conclusion \
  --format pdf \
  --output results/quantum.pdf
```

**Enable verbose agent output:**
```bash
uv run python src/main.py --topic "AI Ethics" --verbose --format pdf
```

**Full CLI reference:**
```
usage: article-generator [--topic TOPIC] [--sections S [S ...]]
                         [--output PATH] [--format {latex,pdf}] [--verbose]

  --topic       Article topic (required)
  --sections    Section names (default: introduction methodology results conclusion)
  --output      Output file path (default: results/article.pdf)
  --format      Output format: latex or pdf (default: pdf)
  --verbose     Print agent reasoning steps
```

---

## Configuration

All configuration lives in `config/` — no values are hardcoded in source.

### `config/setup.json`
Main application settings including version, institution name, default author, and log level.

```json
{
  "version": "1.00",
  "app_name": "LaTeX Article Generator",
  "institution": "Your Institution",
  "log_level": "INFO"
}
```

### `config/rate_limits.json`
API rate limits per service. Adjust `requests_per_minute` if you hit OpenAI throttling.

```json
{
  "version": "1.00",
  "rate_limits": {
    "default": { "requests_per_minute": 20, "requests_per_hour": 200 },
    "openai":  { "requests_per_minute": 60, "requests_per_hour": 500 }
  }
}
```

### `config/logging_config.json`
Standard Python `logging.config.dictConfig` format nested under the `"logging"` key.

---

## Project Structure

```
crewai-latex-article-generator/
├── src/
│   ├── main.py                          # CLI entry point
│   └── latex_article_generator/
│       ├── cli/
│       │   └── parser.py                # argparse CLI argument parser
│       ├── sdk/
│       │   └── sdk.py                   # ArticleGeneratorSDK (public API)
│       ├── services/
│       │   ├── researcher_agent.py      # CrewAI ResearcherAgent factory
│       │   ├── writer_agent.py          # CrewAI WriterAgent factory
│       │   ├── reviewer_agent.py        # CrewAI ReviewerAgent factory
│       │   ├── latex_formatter_agent.py # CrewAI LaTeXFormatterAgent factory
│       │   ├── tasks.py                 # CrewAI Task factories (all 4 tasks)
│       │   ├── crew.py                  # build_crew() assembles the Crew
│       │   ├── compiler.py              # LuaLatexRunner, BiberRunner, MultiPassCompiler
│       │   ├── bidi_handler.py          # Hebrew RTL wrapping
│       │   ├── graph_generator.py       # Matplotlib figure export
│       │   ├── table_generator.py       # LaTeX tabular generator
│       │   ├── tikz_generator.py        # TikZ block diagram / flowchart generator
│       │   ├── latex_template.py        # Base preamble template
│       │   ├── cover_page.py            # Title page generator
│       │   ├── toc_formatter.py         # TOC, headers, footers
│       │   ├── bibliography_generator.py# .bib file generator
│       │   ├── latex_assembler.py       # Assembles final .tex document
│       │   └── validators.py            # LaTeX, PDF, and content validators
│       └── shared/
│           ├── config.py                # ConfigManager (reads all 3 JSON configs)
│           ├── gatekeeper.py            # ApiGatekeeper with rate limiting + retry
│           └── version.py              # Version constant
├── tests/
│   └── unit/                           # One test file per service module
├── config/
│   ├── setup.json
│   ├── rate_limits.json
│   └── logging_config.json
├── docs/
│   ├── PLAN.md                         # Master task index with status tracking
│   ├── PROMPTS.md                      # Prompt templates used during development
│   ├── prompts_log.md                  # Prompt engineering iteration log
│   ├── cost_analysis.md                # Token usage and API cost report
│   └── prd/                           # 41 individual task PRD files
├── assets/                             # Generated graphs and figures
├── pyproject.toml
├── .env-example
└── README.md
```

---

## Running Tests

```bash
# Full test suite with coverage
uv run pytest tests/ --cov

# Quick run without coverage (faster)
uv run pytest tests/ --no-cov -q

# Single test file
uv run pytest tests/unit/test_agents.py -v --no-cov

# Linting (must pass with 0 errors before committing)
uv run ruff check src/ tests/
```

Coverage threshold is set to 85% in `pyproject.toml`. All modules must maintain this threshold at final submission.

---

## Contributing

- **Code style:** `uv run ruff check` must exit 0 — no exceptions
- **File length:** every source and test file must be ≤ 150 lines
- **Testing:** write tests alongside code (Red → Green → Refactor)
- **Dependencies:** use `uv add <package>` — never `pip install`
- **Secrets:** never commit `.env` or any file containing real API keys
- **Commits:** one logical change per commit with a descriptive message

---

## License

MIT License — Ali Trabeh  
Built with [CrewAI](https://crewai.com), [uv](https://docs.astral.sh/uv/), and [Ruff](https://docs.astral.sh/ruff/).
