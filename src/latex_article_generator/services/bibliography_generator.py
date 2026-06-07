"""Bibliography generator — task 024."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Reference:
    key: str
    author: str
    title: str
    year: str
    journal: str = field(default="")
    booktitle: str = field(default="")
    volume: str = field(default="")
    pages: str = field(default="")
    doi: str = field(default="")


class BibliographyGenerator:
    def generate_bib_file(self, references: list[Reference]) -> str:
        """Return the full content of a .bib file."""
        seen: set[str] = set()
        for ref in references:
            if ref.key in seen:
                raise ValueError(f"Duplicate BibTeX key: {ref.key!r}")
            seen.add(ref.key)
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
