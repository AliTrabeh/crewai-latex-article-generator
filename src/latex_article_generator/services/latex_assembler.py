"""LaTeX document assembler — task 025."""

from pathlib import Path


class LaTeXAssembler:
    def assemble(
        self,
        preamble: str,
        cover_page: str,
        toc_block: str,
        header_footer: str,
        sections: dict[str, str],
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
