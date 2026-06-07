---
id: "003"
title: "Version Tracking"
group: "1 — Project Setup and Structure"
priority: high
status: NOT_STARTED
---

# Task 003 — Version Tracking

## Goal

Establish a single version constant (`"1.00"`) as the source of truth, referenced consistently across the package, all JSON config files, and `pyproject.toml`.

## Files to Create or Modify

- `src/latex_article_generator/shared/version.py` — defines `__version__`
- `src/latex_article_generator/__init__.py` — re-exports `__version__`
- `config/setup.json` — must contain `"version": "1.00"`
- `config/rate_limits.json` — must contain `"version": "1.00"` inside the root object
- `config/logging_config.json` — must contain `"version": "1.00"`

## Exact Expected Behavior

`shared/version.py`:
```python
__version__ = "1.00"
```

`__init__.py`:
```python
from latex_article_generator.shared.version import __version__

__all__ = ["__version__"]
```

`ConfigManager._validate_versions()` (see task 004) must compare config `"version"` fields against `__version__` and raise `RuntimeError` if any mismatch is detected.

```python
from latex_article_generator import __version__
assert __version__ == "1.00"
```

## Acceptance Criteria

- [ ] `from latex_article_generator import __version__` returns `"1.00"`.
- [ ] All three JSON config files contain `"version": "1.00"`.
- [ ] Changing `__version__` to `"1.01"` while leaving configs at `"1.00"` causes `ConfigManager` to raise `RuntimeError` on init.

## Notes / Constraints

- Version format is a string `"1.00"`, not a float or tuple.
- When bumping the version in the future, update `shared/version.py`, `pyproject.toml`, and all three JSON files atomically.
- Never import version from `pyproject.toml` at runtime — `shared/version.py` is the runtime source.
