"""CLI argument parser — task 032."""

import argparse
from dataclasses import dataclass


@dataclass
class CliArgs:
    topic: str
    sections: list[str]
    output: str
    format: str
    verbose: bool


def build_parser() -> argparse.ArgumentParser:
    """Return a configured ArgumentParser for the article generator CLI."""
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
    """Parse argv (or sys.argv if None) and return a CliArgs instance."""
    ns = build_parser().parse_args(argv)
    return CliArgs(
        topic=ns.topic,
        sections=ns.sections,
        output=ns.output,
        format=ns.format,
        verbose=ns.verbose,
    )
