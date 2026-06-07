"""SDK — the sole public interface for all article-generation logic.

External consumers (CLI, GUI, REST, third-party) must use only this class.
No business logic lives in GUI or CLI layers.
"""

from latex_article_generator.shared.config import ConfigManager
from latex_article_generator.shared.gatekeeper import ApiGatekeeper, RateLimitConfig


class ArticleGeneratorSDK:
    """Single entry point for all LaTeX article generation operations."""

    def __init__(self, config_dir: str | None = None):
        """Initialize SDK with configuration loaded from config files."""
        self._config = ConfigManager(config_dir)
        self._gatekeeper = self._build_gatekeeper()

    # ------------------------------------------------------------------
    # Public interface (to be implemented in future tasks)
    # ------------------------------------------------------------------

    def generate_article(self, topic: str, sections: list[str]) -> str:
        """Generate a complete LaTeX article for *topic* with *sections*.

        Returns the LaTeX source as a string.
        """
        raise NotImplementedError

    def compile_pdf(self, latex_source: str, output_path: str) -> str:
        """Compile *latex_source* to PDF and write it to *output_path*.

        Returns the absolute path to the generated PDF.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_gatekeeper(self) -> ApiGatekeeper:
        limits = self._config.get_rate_limit()
        cfg = RateLimitConfig(
            requests_per_minute=limits.get("requests_per_minute", 30),
            requests_per_hour=limits.get("requests_per_hour", 500),
            concurrent_max=limits.get("concurrent_max", 5),
            retry_after_seconds=limits.get("retry_after_seconds", 30),
            max_retries=limits.get("max_retries", 3),
        )
        return ApiGatekeeper(cfg)
