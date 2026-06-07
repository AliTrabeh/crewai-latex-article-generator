---
id: "040"
title: "Integration Tests — End-to-End Pipeline"
group: "12 — Testing and Final Submission Cleanup"
priority: high
status: DONE
---

# Task 040 — Integration Tests

## Goal

Write integration tests that exercise the full pipeline from topic input to LaTeX output (mocking the LLM layer) and optionally to PDF output (mocking the compiler layer).

## Files to Create or Modify

- `tests/integration/test_pipeline.py` — end-to-end integration tests

## Exact Expected Behavior

```python
from unittest.mock import patch, MagicMock
import pytest
from latex_article_generator.sdk.sdk import ArticleGeneratorSDK

MOCK_LATEX = r"""
\documentclass{article}
\begin{document}
\maketitle
\section{Introduction}
This is the introduction.
\section{Conclusion}
This is the conclusion.
\printbibliography
\end{document}
"""

@patch("latex_article_generator.services.crew.build_crew")
def test_generate_article_returns_string(mock_build_crew, tmp_path):
    mock_crew = MagicMock()
    mock_crew.kickoff.return_value = MOCK_LATEX
    mock_build_crew.return_value = mock_crew

    sdk = ArticleGeneratorSDK(config_dir=str(tmp_path / "config"))
    # use a real config dir for this test
    result = sdk.generate_article("AI", ["introduction", "conclusion"])
    assert isinstance(result, str)
    assert len(result) > 0

@patch("latex_article_generator.services.crew.build_crew")
@patch("latex_article_generator.services.compiler.MultiPassCompiler.compile")
def test_compile_pdf_returns_path(mock_compile, mock_build_crew, tmp_path):
    mock_compile.return_value = str(tmp_path / "article.pdf")
    (tmp_path / "article.pdf").write_bytes(b"%PDF-1.4 fake")

    sdk = ArticleGeneratorSDK()
    pdf_path = sdk.compile_pdf(MOCK_LATEX, str(tmp_path / "article.pdf"))
    assert pdf_path.endswith(".pdf")
```

## Acceptance Criteria

- [ ] `test_generate_article_returns_string` passes with mocked crew.
- [ ] `test_compile_pdf_returns_path` passes with mocked compiler.
- [ ] All integration tests pass without real API keys or LaTeX installation.
- [ ] Integration tests are located in `tests/integration/`.
- [ ] `uv run pytest tests/integration/` exits 0.

## Notes / Constraints

- Integration tests must not make real network calls — all LLM and API calls must be mocked.
- If a real LaTeX installation is available (CI environment), add a `@pytest.mark.slow` marker and skip by default.
- Config files needed for `ArticleGeneratorSDK` init must be available — use the real `config/` dir or a fixture-created copy.
