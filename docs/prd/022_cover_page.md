---
id: "022"
title: "Cover Page Generator"
group: "7 — LaTeX Document Generation"
priority: high
status: NOT_STARTED
---

# Task 022 — Cover Page Generator

## Goal

Generate the LaTeX cover page markup (title, author, institution, date, abstract) that appears on the first page of the compiled PDF.

## Files to Create or Modify

- `src/latex_article_generator/services/cover_page.py` — `CoverPageGenerator` class

## Exact Expected Behavior

```python
class CoverPageGenerator:
    def generate(
        self,
        title: str,
        author: str,
        institution: str,
        date: str,
        abstract: str,
    ) -> str:
        """Return LaTeX markup for the cover page."""
        return (
            "\\begin{titlepage}\n"
            "\\centering\n"
            f"\\vspace*{{2cm}}\n"
            f"{{\\Huge\\bfseries {title}\\par}}\n"
            "\\vspace{1.5cm}\n"
            f"{{\\Large {author}\\par}}\n"
            "\\vspace{0.5cm}\n"
            f"{{\\large {institution}\\par}}\n"
            "\\vspace{0.5cm}\n"
            f"{{\\large {date}\\par}}\n"
            "\\vfill\n"
            "\\begin{abstract}\n"
            f"{abstract}\n"
            "\\end{abstract}\n"
            "\\end{titlepage}\n"
        )
```

## Acceptance Criteria

- [ ] `generator.generate("Title", "Author", "Institute", "2026", "Abstract text")` returns a string starting with `\begin{titlepage}`.
- [ ] All five fields appear in the output.
- [ ] `\end{titlepage}` is present.
- [ ] `\begin{abstract}...\end{abstract}` is included.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Special LaTeX characters in title/author (`&`, `%`, `_`, `#`) must be escaped before passing to this generator — add a static `escape_latex(text: str) -> str` helper.
- The cover page is inserted after `\begin{document}` and before the first `\section{}`.
- In v1.00, institution is hardcoded from `config/setup.json` → `"institution"` key; add that key to setup.json.
