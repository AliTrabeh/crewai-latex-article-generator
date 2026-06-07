---
id: "032"
title: "CLI Argument Parser"
group: "10 — CLI Entry Point"
priority: high
---

# Task 032 — CLI Argument Parser

## Goal

Implement the `argparse`-based CLI argument parser that translates command-line flags into parameters for the SDK.

## Files to Create or Modify

- `src/latex_article_generator/cli/parser.py` — `build_parser()` factory and `CliArgs` dataclass
- `src/latex_article_generator/cli/__init__.py` — empty package marker

## Exact Expected Behavior

```python
import argparse
from dataclasses import dataclass

@dataclass
class CliArgs:
    topic: str
    sections: list[str]
    output: str
    format: str          # "latex" | "pdf"
    verbose: bool

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="article-generator",
        description="Generate a LaTeX academic article using CrewAI agents.",
    )
    parser.add_argument("--topic", required=True, help="Article topic")
    parser.add_argument(
        "--sections",
        nargs="+",
        default=["introduction", "methodology", "results", "conclusion"],
        help="Sections to generate",
    )
    parser.add_argument(
        "--output",
        default="results/article.pdf",
        help="Output file path",
    )
    parser.add_argument(
        "--format",
        choices=["latex", "pdf"],
        default="pdf",
        help="Output format",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser

def parse_args(argv: list[str] | None = None) -> CliArgs:
    parser = build_parser()
    ns = parser.parse_args(argv)
    return CliArgs(
        topic=ns.topic,
        sections=ns.sections,
        output=ns.output,
        format=ns.format,
        verbose=ns.verbose,
    )
```

## Acceptance Criteria

- [ ] `parse_args(["--topic", "AI"])` returns `CliArgs(topic="AI", ...)`.
- [ ] Default sections are `["introduction", "methodology", "results", "conclusion"]`.
- [ ] `--format xyz` raises `SystemExit` (invalid choice).
- [ ] `--verbose` sets `verbose=True`.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- `--topic` is the only required argument.
- `parse_args(argv)` accepts an optional `argv` list for testability — do not use `sys.argv` directly inside the function.
- No business logic in the parser — only argument parsing and `CliArgs` construction.
