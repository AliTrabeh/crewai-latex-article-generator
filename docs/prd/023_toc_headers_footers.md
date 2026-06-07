---
id: "023"
title: "TOC, Headers, and Footers"
group: "7 — LaTeX Document Generation"
priority: medium
status: NOT_STARTED
---

# Task 023 — Table of Contents, Headers, and Footers

## Goal

Generate LaTeX markup for the table of contents, configure headers/footers with the `fancyhdr` package, and set page numbering conventions.

## Files to Create or Modify

- `src/latex_article_generator/services/toc_formatter.py` — `TocFormatter` class

## Exact Expected Behavior

```python
class TocFormatter:
    def generate_toc_block(self) -> str:
        """Return LaTeX commands to insert the TOC on a new page."""
        return (
            "\\tableofcontents\n"
            "\\newpage\n"
        )

    def configure_headers_footers(self, title: str, author: str) -> str:
        """Return fancyhdr configuration commands."""
        return (
            "\\pagestyle{fancy}\n"
            "\\fancyhf{}\n"
            f"\\fancyhead[L]{{\\small {author}}}\n"
            f"\\fancyhead[R]{{\\small {title}}}\n"
            "\\fancyfoot[C]{\\thepage}\n"
            "\\renewcommand{\\headrulewidth}{0.4pt}\n"
        )

    def set_page_numbering(self, style: str = "arabic") -> str:
        """Return command to set page number style ('arabic', 'roman', 'Roman')."""
        return f"\\pagenumbering{{{style}}}\n"
```

## Acceptance Criteria

- [ ] `generate_toc_block()` returns a string containing `\tableofcontents`.
- [ ] `configure_headers_footers("Title", "Author")` contains `\fancyhead` and `\fancyfoot`.
- [ ] `set_page_numbering("roman")` returns `\pagenumbering{roman}`.
- [ ] No hardcoded author or title values.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- `fancyhdr` must be loaded in the preamble (task 021) — this class only emits commands, not `\usepackage`.
- The cover page (task 022) uses `\thispagestyle{empty}` to suppress headers/footers on page 1 — insert this command inside `\begin{titlepage}`.
- `\pagenumbering{roman}` is used for TOC pages; `\pagenumbering{arabic}` restarts at 1 for main content.
