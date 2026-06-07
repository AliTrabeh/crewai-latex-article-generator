"""Tests for CLI argument parser (task 032)."""

import pytest

from latex_article_generator.cli.parser import CliArgs, build_parser, parse_args


def test_parse_topic():
    args = parse_args(["--topic", "Artificial Intelligence"])
    assert args.topic == "Artificial Intelligence"


def test_returns_cli_args():
    assert isinstance(parse_args(["--topic", "AI"]), CliArgs)


def test_default_sections():
    args = parse_args(["--topic", "AI"])
    assert args.sections == ["introduction", "methodology", "results", "conclusion"]


def test_custom_sections():
    args = parse_args(["--topic", "AI", "--sections", "intro", "methods"])
    assert args.sections == ["intro", "methods"]


def test_default_output():
    args = parse_args(["--topic", "AI"])
    assert args.output == "results/article.pdf"


def test_custom_output():
    args = parse_args(["--topic", "AI", "--output", "/tmp/out.pdf"])
    assert args.output == "/tmp/out.pdf"


def test_default_format_is_pdf():
    args = parse_args(["--topic", "AI"])
    assert args.format == "pdf"


def test_format_latex():
    args = parse_args(["--topic", "AI", "--format", "latex"])
    assert args.format == "latex"


def test_invalid_format_raises_system_exit():
    with pytest.raises(SystemExit):
        parse_args(["--topic", "AI", "--format", "docx"])


def test_verbose_default_false():
    args = parse_args(["--topic", "AI"])
    assert args.verbose is False


def test_verbose_flag_sets_true():
    args = parse_args(["--topic", "AI", "--verbose"])
    assert args.verbose is True


def test_missing_topic_raises_system_exit():
    with pytest.raises(SystemExit):
        parse_args([])


def test_build_parser_returns_argument_parser():
    import argparse
    assert isinstance(build_parser(), argparse.ArgumentParser)
