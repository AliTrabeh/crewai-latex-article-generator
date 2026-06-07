# CrewAI LaTeX Article Generator

A multi-agent system built with [CrewAI](https://crewai.com) that automatically generates well-structured academic articles in LaTeX format.

---

## Installation Instructions

### System Requirements
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager (mandatory)
- LaTeX distribution (e.g., TeX Live, MiKTeX) for PDF compilation

### Step-by-step setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd crewai-latex-article-generator

# 2. Install dependencies with uv (do NOT use pip)
uv sync

# 3. Copy the environment template and fill in your API keys
cp .env-example .env
# Edit .env with your actual keys

# 4. Verify the installation
uv run python src/main.py
```

### Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key for LLM calls |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional alternative) |
| `SERPER_API_KEY` | Serper API key for web search |

---

## Usage Instructions

```bash
# Run the article generator (CLI)
uv run python src/main.py --topic "Transformer architectures" --sections intro methods results

# Run tests
uv run pytest tests/

# Lint
uv run ruff check src/
```

---

## Examples and Demos

*(To be populated once the implementation is complete.)*

---

## Configuration Guide

All configuration lives in `config/`:

| File | Purpose |
|---|---|
| `config/setup.json` | Main application settings (versioned) |
| `config/rate_limits.json` | API rate limits per service (versioned) |
| `config/logging_config.json` | Logging format and levels |

No configuration values are hardcoded in source files.

---

## Contribution Guidelines

- Follow PEP 8 / Ruff rules (line length 100, `ruff check` must pass with 0 errors)
- All public methods require docstrings explaining *why*, not just *what*
- Write tests before or alongside code (TDD: Red → Green → Refactor)
- Minimum 85% test coverage required
- Use `uv add <pkg>` to add dependencies — never `pip install`
- No API keys or secrets in source code

---

## License & Credits

MIT License — Ali Trabeh  
Built with [CrewAI](https://crewai.com), [uv](https://docs.astral.sh/uv/), and [Ruff](https://docs.astral.sh/ruff/).
