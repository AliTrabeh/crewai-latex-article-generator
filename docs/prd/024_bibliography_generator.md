---
id: "024"
title: "Bibliography Generator"
group: "7 — LaTeX Document Generation"
priority: high
---

# Task 024 — Bibliography Generator

## Goal

Parse citation information from the article content and generate a `.bib` file that `biber` will process during compilation.

## Files to Create or Modify

- `src/latex_article_generator/services/bibliography_generator.py` — `BibliographyGenerator` class

## Exact Expected Behavior

```python
from dataclasses import dataclass

@dataclass
class Reference:
    key: str           # BibTeX key, e.g. "Smith2023"
    author: str
    title: str
    year: str
    journal: str = ""
    booktitle: str = ""
    volume: str = ""
    pages: str = ""
    doi: str = ""

class BibliographyGenerator:
    def generate_bib_file(self, references: list[Reference]) -> str:
        """Return the full content of a .bib file."""
        entries = [self._format_entry(ref) for ref in references]
        return "\n\n".join(entries)

    def write_bib_file(self, references: list[Reference], path: str) -> str:
        """Write .bib content to disk; return the path."""
        content = self.generate_bib_file(references)
        Path(path).write_text(content, encoding="utf-8")
        return path

    def _format_entry(self, ref: Reference) -> str:
        entry_type = "article" if ref.journal else "inproceedings"
        venue_field = (
            f"  journal = {{{ref.journal}}},"
            if ref.journal
            else f"  booktitle = {{{ref.booktitle}}},"
        )
        return (
            f"@{entry_type}{{{ref.key},\n"
            f"  author = {{{ref.author}}},\n"
            f"  title = {{{ref.title}}},\n"
            f"  year = {{{ref.year}}},\n"
            f"{venue_field}\n"
            f"}}"
        )
```

## Acceptance Criteria

- [ ] `generator.generate_bib_file([Reference("K1","Author","Title","2023","Journal")])` contains `@article{K1,`.
- [ ] `write_bib_file(refs, "/tmp/refs.bib")` creates the file and returns the path.
- [ ] Missing optional fields do not cause errors.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- BibTeX keys must be unique — add a deduplication check in `generate_bib_file`.
- The `.bib` file is written to the same directory as the `.tex` file before compilation begins.
- `biber` (not `bibtex`) is used — ensure `biblatex` backend in the preamble is `biber`.
