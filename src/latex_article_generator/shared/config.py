"""Configuration manager — reads all settings from config files, never from hardcoded values."""

import json
from pathlib import Path
from typing import Any


class ConfigManager:
    """Loads and exposes configuration from versioned JSON files."""

    def __init__(self, config_dir: str | None = None):
        """Load all config files; raise RuntimeError on version mismatch."""
        self._config_dir = Path(config_dir or self._default_config_dir())
        self._setup = self._load("setup.json")
        self._rate_limits = self._load("rate_limits.json")
        self._logging = self._load("logging_config.json")
        self._validate_versions()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """Return value from setup.json by key."""
        return self._setup.get(key, default)

    def get_rate_limit(self, service: str = "default") -> dict:
        """Return rate limit dict for the named service."""
        limits = self._rate_limits.get("rate_limits", {})
        return limits.get(service, limits.get("default", {}))

    def get_logging(self) -> dict:
        """Return the logging config dict (suitable for logging.config.dictConfig)."""
        return self._logging.get("logging", self._logging)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self, filename: str) -> dict:
        """Read and parse a JSON file from config_dir; raise FileNotFoundError if missing."""
        path = self._config_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Required config file not found: {path}")
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    def _validate_versions(self) -> None:
        """Compare version field in each config against __version__; raise RuntimeError if mismatch."""
        from latex_article_generator.shared.version import __version__

        checks = [
            ("setup.json", self._setup),
            ("rate_limits.json", self._rate_limits),
            ("logging_config.json", self._logging),
        ]
        for filename, cfg in checks:
            cfg_version = cfg.get("version")
            if cfg_version is not None and cfg_version != __version__:
                raise RuntimeError(
                    f"Version mismatch in {filename}: "
                    f"code={__version__!r}, config={cfg_version!r}"
                )

    @staticmethod
    def _default_config_dir() -> str:
        """Return absolute path to project-root/config/."""
        return str(Path(__file__).resolve().parents[3] / "config")
