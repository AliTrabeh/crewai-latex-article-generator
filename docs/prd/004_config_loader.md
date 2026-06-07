---
id: "004"
title: "ConfigManager — JSON Config Loader"
group: "2 — Configuration and Environment Handling"
priority: critical
status: NOT_STARTED
---

# Task 004 — ConfigManager

## Goal

Implement `ConfigManager` so that all application settings are read from versioned JSON files at startup. No hardcoded values may appear anywhere in source code.

## Files to Create or Modify

- `src/latex_article_generator/shared/config.py` — `ConfigManager` class
- `config/setup.json` — general app settings
- `config/rate_limits.json` — rate limit settings (see task 006)
- `config/logging_config.json` — Python logging dict config

## Exact Expected Behavior

```python
class ConfigManager:
    def __init__(self, config_dir: str | None = None) -> None:
        """Load all config files; raise RuntimeError on version mismatch."""

    def get(self, key: str, default=None) -> Any:
        """Return value from setup.json by key."""

    def get_rate_limit(self, service: str = "default") -> dict:
        """Return rate limit dict for the named service."""

    def get_logging(self) -> dict:
        """Return the full logging config dict."""

    def _load(self, filename: str) -> dict:
        """Read and parse a JSON file from config_dir; raise FileNotFoundError if missing."""

    def _validate_versions(self) -> None:
        """Compare version field in each config against __version__; raise RuntimeError if mismatch."""

    def _default_config_dir(self) -> str:
        """Return absolute path to project-root/config/."""
```

`_default_config_dir` resolves relative to the location of `config.py` so it works regardless of the working directory at runtime.

## Acceptance Criteria

- [ ] `ConfigManager()` (no args) finds `config/` using the default path.
- [ ] `ConfigManager(config_dir="/custom/path")` uses the supplied path.
- [ ] `config_manager.get("app_name")` returns `"crewai-latex-article-generator"`.
- [ ] Corrupted or missing JSON file raises `FileNotFoundError` or `json.JSONDecodeError`.
- [ ] Version mismatch raises `RuntimeError` with a descriptive message naming the mismatched file.
- [ ] Unit test coverage ≥ 85% for this module.

## Notes / Constraints

- File must stay ≤ 150 lines; split helpers into private methods if needed.
- Do not use `importlib.resources` — file-system path resolution via `pathlib.Path` is preferred.
- `config_dir` is a `str` parameter (not `Path`) for SDK compatibility; convert internally.
- No caching between calls — configs are read once at `__init__` and stored as instance attributes.
