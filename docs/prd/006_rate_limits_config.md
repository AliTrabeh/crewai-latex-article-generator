---
id: "006"
title: "Rate Limits Configuration"
group: "2 — Configuration and Environment Handling"
priority: high
status: NOT_STARTED
---

# Task 006 — Rate Limits Configuration

## Goal

Define the `RateLimitConfig` dataclass and populate `config/rate_limits.json` with per-service limits that `ApiGatekeeper` will enforce.

## Files to Create or Modify

- `config/rate_limits.json` — rate limit values per service
- `src/latex_article_generator/shared/gatekeeper.py` — `RateLimitConfig` dataclass

## Exact Expected Behavior

`config/rate_limits.json`:
```json
{
  "version": "1.00",
  "rate_limits": {
    "default": {
      "requests_per_minute": 20,
      "requests_per_hour": 200,
      "concurrent_max": 3,
      "retry_after_seconds": 5,
      "max_retries": 3
    },
    "openai": {
      "requests_per_minute": 60,
      "requests_per_hour": 500,
      "concurrent_max": 5,
      "retry_after_seconds": 10,
      "max_retries": 5
    }
  }
}
```

`RateLimitConfig` dataclass:
```python
from dataclasses import dataclass

@dataclass
class RateLimitConfig:
    requests_per_minute: int
    requests_per_hour: int
    concurrent_max: int
    retry_after_seconds: int
    max_retries: int
```

`ConfigManager.get_rate_limit("openai")` must return the `openai` sub-dict; `get_rate_limit()` (no arg) returns `default`.

## Acceptance Criteria

- [ ] `config_manager.get_rate_limit("default")["requests_per_minute"]` returns `20`.
- [ ] `config_manager.get_rate_limit("openai")["max_retries"]` returns `5`.
- [ ] `config_manager.get_rate_limit("unknown_service")` falls back to `"default"` rather than raising.
- [ ] `RateLimitConfig` can be instantiated from the dict via `RateLimitConfig(**limits_dict)`.

## Notes / Constraints

- Do not hardcode any numeric limit in Python source — all values must come from the JSON file.
- The fallback-to-default behavior for unknown services must be tested.
- `version` field sits at the root of `rate_limits.json`, not inside the `rate_limits` object.
