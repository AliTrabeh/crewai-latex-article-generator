"""Immutable project-wide constants."""

from enum import Enum


class ArticleSection(Enum):
    INTRODUCTION = "introduction"
    RELATED_WORK = "related_work"
    METHODOLOGY = "methodology"
    RESULTS = "results"
    CONCLUSION = "conclusion"


class OutputFormat(Enum):
    LATEX = "latex"
    PDF = "pdf"
    MARKDOWN = "markdown"


DEFAULT_LATEX_TEMPLATE = "article"
MAX_SECTION_LENGTH = 2000
MIN_SECTION_LENGTH = 100
