---
id: "005"
title: "Environment Variables and Secrets Management"
group: "2 — Configuration and Environment Handling"
priority: critical
status: DONE
---

# Task 005 — Environment Variables and Secrets Management

## Goal

Ensure all API keys and secrets are loaded exclusively from environment variables at runtime. No secret may appear in source code or committed files.

## Files to Create or Modify

- `.env-example` — placeholder keys, committed to git
- `.env` — real keys, git-ignored (user creates from `.env-example`)
- `.gitignore` — must exclude `.env`, `*.key`, `*.pem`, `credentials.json`
- `src/latex_article_generator/shared/config.py` — already loads `python-dotenv` at startup

## Exact Expected Behavior

`.env-example` content:
```
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
SERPER_API_KEY=your-serper-key-here
```

In any source file that needs an API key:
```python
import os
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set")
```

`python-dotenv` must be loaded once, early (e.g., in `sdk.py` `__init__` or `main.py`):
```python
from dotenv import load_dotenv
load_dotenv()  # reads .env if present, does not override already-set vars
```

## Acceptance Criteria

- [x] `git grep -r "sk-"` returns no matches (no real keys committed).
- [x] `.env` is listed in `.gitignore`.
- [x] Running the app without `.env` and without env vars raises a clear `EnvironmentError`, not a cryptic AttributeError.
- [x] `.env-example` is committed and contains all three placeholder keys.

## Notes / Constraints

- `load_dotenv()` must be called before any `os.environ.get()` — place it at the very top of the entry point.
- Never use `os.environ["KEY"]` (raises `KeyError`); prefer `os.environ.get("KEY")` and handle `None` explicitly.
- The `.env` file must never be committed — add a pre-commit check or document the risk in README.
