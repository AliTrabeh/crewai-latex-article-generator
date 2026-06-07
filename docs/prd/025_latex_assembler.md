---
id: "025"
title: "LaTeX Document Assembler"
group: "7 — LaTeX Document Generation"
priority: critical
status: NOT_STARTED
---

# Task 025 — LaTeX Document Assembler

## Goal

Combine preamble, cover page, TOC, section content, figures, tables, TikZ diagrams, and bibliography into a single valid `.tex` file ready for compilation.

## Files to Create or Modify

- `src/latex_article_generator/services/latex_assembler.py` — `LaTeXAssembler` class

## Exact Expected Behavior

```python
from pathlib import Path

class LaTeXAssembler:
    def assemble(
        self,
        preamble: str,
        cover_page: str,
        toc_block: str,
        header_footer: str,
        sections: dict[str, str],  # section_name -> latex content
        bibliography_path: str,
        output_path: str,
    ) -> str:
        """Assemble complete .tex document; write to output_path; return the path."""
        parts = [
            preamble,
            "\\begin{document}",
            "\\maketitle",
            cover_page,
            header_footer,
            toc_block,
            "\\newpage",
        ]
        for section_name, content in sections.items():
            parts.append(f"\\section{{{section_name}}}")
            parts.append(content)
        parts += [
            "\\newpage",
            "\\printbibliography",
            "\\end{document}",
        ]
        tex_content = "\n\n".join(parts)
        Path(output_path).write_text(tex_content, encoding="utf-8")
        return output_path
```

## Acceptance Criteria

- [ ] `assembler.assemble(...)` writes a `.tex` file and returns the path.
- [ ] Output contains `\begin{document}` and `\end{document}`.
- [ ] `\section{SectionName}` appears for each key in `sections`.
- [ ] `\printbibliography` appears before `\end{document}`.
- [ ] The assembled `.tex` compiles without LaTeX errors on a simple test input.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Section order follows the insertion order of the `sections` dict (Python 3.7+ dicts are ordered).
- The `output_path` directory must already exist before calling `assemble()` — the assembler does not create directories.
- All content strings passed in must already be LaTeX-encoded (special chars escaped, Hebrew wrapped in RTL directives).
