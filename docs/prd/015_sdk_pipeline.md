---
id: "015"
title: "SDK Pipeline — generate_article()"
group: "5 — Content Generation Pipeline"
priority: critical
---

# Task 015 — SDK Pipeline

## Goal

Implement `ArticleGeneratorSDK.generate_article()` — the single public method that orchestrates the full research → writing → review → formatting pipeline and returns the LaTeX source string.

## Files to Create or Modify

- `src/latex_article_generator/sdk/sdk.py` — implement `generate_article()` and `compile_pdf()`

## Exact Expected Behavior

```python
class ArticleGeneratorSDK:
    def __init__(self, config_dir: str | None = None) -> None:
        from dotenv import load_dotenv
        load_dotenv()
        self._config = ConfigManager(config_dir)
        self._gatekeeper = self._build_gatekeeper()

    def generate_article(self, topic: str, sections: list[str]) -> str:
        """Run the full CrewAI pipeline; return LaTeX source string."""
        crew = build_crew(topic, sections, self._agent_config())
        result = crew.kickoff()
        return str(result)

    def compile_pdf(self, latex_source: str, output_path: str) -> str:
        """Compile LaTeX source to PDF; return path to PDF file."""
        from latex_article_generator.services.compiler import MultiPassCompiler
        compiler = MultiPassCompiler(self._config)
        return compiler.compile(latex_source, output_path)

    def _build_gatekeeper(self) -> ApiGatekeeper:
        limits = self._config.get_rate_limit()
        cfg = RateLimitConfig(**limits)
        return ApiGatekeeper(cfg)

    def _agent_config(self) -> dict:
        return {
            "verbose": self._config.get("log_level") == "DEBUG",
            "max_iter": 5,
        }
```

## Acceptance Criteria

- [ ] `sdk.generate_article("topic", ["intro"])` calls `crew.kickoff()` exactly once.
- [ ] Return value is a non-empty string.
- [ ] `sdk.compile_pdf(latex_str, "/tmp/out")` delegates to `MultiPassCompiler`.
- [ ] All secrets loaded from env, not from config files.
- [ ] Unit tests mock `build_crew` and `crew.kickoff` to avoid LLM calls.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- The SDK is the **only** public interface — CLI, tests, and future REST layer must all call through `ArticleGeneratorSDK`.
- `_gatekeeper` instance is available for use by agent tools if needed in the future.
- Do not catch exceptions from `crew.kickoff()` here — let them propagate to the CLI layer.
