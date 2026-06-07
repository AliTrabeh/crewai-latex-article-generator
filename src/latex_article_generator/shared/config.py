"""Configuration manager — reads all settings from config files, never from hardcoded values."""

import json
import os
from pathlib import Path


class ConfigManager:
    """Loads and exposes configuration from versioned JSON files."""

    def __init__(self, config_dir: str | None = None):
        """Initialize with the path to the config directory."""
        self._config_dir = Path(config_dir or self._default_config_dir())
        self._setup = self._load("setup.json")
        self._rate_limits = self._load("rate_limits.json")
        self._logging = self._load("logging_config.json")
        self._validate_versions()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get(self, key: str, default=None):
        """Return a value from the main setup config."""
        return self._setup.get(key, default)

    def get_rate_limit(self, service: str = "default") -> dict:
        """Return rate-limit settings for *service*."""
        services = self._rate_limits.get("rate_limits", {}).get("services", {})
        return services.get(service, services.get("default", {}))

    def get_logging(self) -> dict:
        """Return the logging configuration dict."""
        return self._logging

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self, filename: str) -> dict:
        path = self._config_dir / filename
        if not path.exists():
            return {}
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    def _validate_versions(self) -> None:
        """Verify that config-file versions match the code version."""
        from latex_article_generator.shared.version import __version__

        cfg_version = self._setup.get("version")
        if cfg_version and cfg_version != __version__:
            raise RuntimeError(
                f"Config version mismatch: code={__version__}, config={cfg_version}"
            )

    @staticmethod
    def _default_config_dir() -> str:
        return str(Path(__file__).resolve().parents[3] / "config")
