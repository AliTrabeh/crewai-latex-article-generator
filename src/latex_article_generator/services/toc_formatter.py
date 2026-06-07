"""TOC, headers, and footers formatter — task 023."""


class TocFormatter:
    def generate_toc_block(self) -> str:
        """Return LaTeX commands to insert the TOC on a new page."""
        return "\\tableofcontents\n" "\\newpage\n"

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
