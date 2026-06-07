"""Cover page generator — task 022."""


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

    @staticmethod
    def escape_latex(text: str) -> str:
        """Escape special LaTeX characters."""
        return (
            text.replace("&", r"\&")
            .replace("%", r"\%")
            .replace("_", r"\_")
            .replace("#", r"\#")
        )
