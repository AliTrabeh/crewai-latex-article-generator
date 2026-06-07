"""LaTeX table generator — task 019."""


class TableGenerator:
    def generate(
        self,
        headers: list[str],
        rows: list[list[str]],
        caption: str = "",
        label: str = "",
        alignment: str | None = None,
    ) -> str:
        """Return a LaTeX table string wrapped in a table environment."""
        col_spec = alignment or "|" + "l|" * len(headers)
        lines = [
            "\\begin{table}[h]",
            "\\centering",
            f"\\begin{{tabular}}{{{col_spec}}}",
            "\\hline",
            " & ".join(f"\\textbf{{{h}}}" for h in headers) + " \\\\",
            "\\hline",
        ]
        for row in rows:
            lines.append(" & ".join(str(cell) for cell in row) + " \\\\")
        lines += [
            "\\hline",
            "\\end{tabular}",
        ]
        if caption:
            lines.append(f"\\caption{{{caption}}}")
        if label:
            lines.append(f"\\label{{tab:{label}}}")
        lines.append("\\end{table}")
        return "\n".join(lines)

    @staticmethod
    def escape(text: str) -> str:
        """Escape special LaTeX characters in cell values."""
        return text.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
