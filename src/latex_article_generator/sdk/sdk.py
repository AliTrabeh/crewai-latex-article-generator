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

    def generate_article(self, topic: str, sections: list[str]) -> str:
        """Run the full CrewAI pipeline; return LaTeX source string."""
        from latex_article_generator.services.crew import build_crew

        crew = build_crew(topic, sections, self._agent_config())
        result = crew.kickoff()
        return str(result)

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
