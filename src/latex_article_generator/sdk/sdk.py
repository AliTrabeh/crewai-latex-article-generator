"""SDK — the sole public interface for all article-generation logic."""

from dotenv import load_dotenv

from latex_article_generator.shared.config import ConfigManager
from latex_article_generator.shared.gatekeeper import ApiGatekeeper, RateLimitConfig


class ArticleGeneratorSDK:
    """Single entry point for all LaTeX article generation operations."""

    def __init__(self, config_dir: str | None = None) -> None:
        """Load env, config, and rate limiter."""
        load_dotenv()
        self._config = ConfigManager(config_dir)
        self._gatekeeper = self._build_gatekeeper()

    def generate_article(
        self, topic: str, sections: list[str], *, graph_path: str = "", bib_path: str = ""
    ) -> str:
        """Run the full CrewAI pipeline; return LaTeX source string."""
        from latex_article_generator.services.crew import build_crew

        crew = build_crew(
            topic, sections, self._agent_config(), graph_path=graph_path, bib_path=bib_path
        )
        result = str(crew.kickoff())
        text = self._strip_markdown_fences(result)
        text = self._patch_preamble(text)
        return self._ensure_complete_document(text)

    @staticmethod
    def _strip_markdown_fences(text: str) -> str:
        """Remove ```latex ... ``` or ``` ... ``` wrappers that LLMs add."""
        import re
        text = text.strip()
        text = re.sub(r"^```(?:latex)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
        return text.strip()

    @staticmethod
    def _patch_preamble(text: str) -> str:
        """Fix known preamble issues that break XeLaTeX compilation."""
        import re
        # Suppress URL/DOI in biblatex to avoid nullfont errors with hyperref
        text = re.sub(
            r"\\usepackage\[([^\]]*backend=biber[^\]]*)\]\{biblatex\}",
            lambda m: (
                r"\usepackage[" + m.group(1) + "]{biblatex}"
                if "url=false" in m.group(1)
                else r"\usepackage[" + m.group(1) + ",url=false,doi=false]{biblatex}"
            ),
            text,
        )
        # Ensure headheight is set (fancyhdr warning that becomes an error at high page counts)
        if r"\setlength{\headheight}" not in text:
            text = text.replace(
                r"\usepackage{fancyhdr}",
                r"\usepackage{fancyhdr}" + "\n" + r"\setlength{\headheight}{14.5pt}",
            )
        # Remove LuaTeX-only primitive that XeLaTeX doesn't understand
        text = text.replace(r"\textdir TRT", "")
        return text

    @staticmethod
    def _ensure_complete_document(text: str) -> str:
        """Append missing \\printbibliography / \\end{document} if the LLM truncated output."""
        if r"\end{document}" not in text:
            suffix = ""
            if r"\printbibliography" not in text:
                suffix = "\n\n\\printbibliography"
            text = text.rstrip() + suffix + "\n\\end{document}\n"
        return text

    def compile_pdf(self, latex_source: str, output_path: str) -> str:
        """Compile LaTeX source to PDF; return path to the PDF file."""
        from latex_article_generator.services.compiler import MultiPassCompiler

        compiler = MultiPassCompiler(self._config)
        return compiler.compile(latex_source, output_path)

    def _build_gatekeeper(self) -> ApiGatekeeper:
        limits = self._config.get_rate_limit()
        return ApiGatekeeper(RateLimitConfig(**limits))

    def _agent_config(self) -> dict:
        return {
            "verbose": self._config.get("log_level") == "DEBUG",
            "max_iter": 5,
        }
