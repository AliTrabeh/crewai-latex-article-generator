---
id: "030"
title: "PDF Output Validator"
group: "9 — Validation and Checking System"
priority: medium
status: NOT_STARTED
---

# Task 030 — PDF Output Validator

## Goal

Implement a post-compilation validator that verifies the generated PDF is a valid, non-empty PDF file meeting minimum quality requirements.

## Files to Create or Modify

- `src/latex_article_generator/services/validators.py` — add `PdfValidator` class

## Exact Expected Behavior

```python
from pathlib import Path

class PdfValidator:
    MIN_FILE_SIZE_BYTES = 1024       # 1 KB minimum
    MIN_PAGE_COUNT = 3               # homework requires substantial document

    def validate(self, pdf_path: str) -> ValidationResult:
        errors, warnings = [], []
        path = Path(pdf_path)
        self._check_exists(path, errors)
        if not errors:
            self._check_file_size(path, errors)
            self._check_pdf_header(path, errors)
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def _check_exists(self, path: Path, errors: list) -> None:
        if not path.exists():
            errors.append(f"PDF not found: {path}")

    def _check_file_size(self, path: Path, errors: list) -> None:
        size = path.stat().st_size
        if size < self.MIN_FILE_SIZE_BYTES:
            errors.append(f"PDF too small: {size} bytes (min {self.MIN_FILE_SIZE_BYTES})")

    def _check_pdf_header(self, path: Path, errors: list) -> None:
        with open(path, "rb") as f:
            header = f.read(5)
        if header != b"%PDF-":
            errors.append("File does not start with PDF magic bytes %PDF-")
```

## Acceptance Criteria

- [ ] Valid PDF → `ValidationResult(valid=True)`.
- [ ] Missing file → error "PDF not found".
- [ ] File < 1 KB → size error.
- [ ] File with wrong header → header error.
- [ ] File ≤ 150 lines (shared with validators.py from tasks 029 and 031).

## Notes / Constraints

- Do not install `pypdf` or any PDF library — byte-level header check is sufficient for v1.00.
- Page count validation via subprocess calling `pdfinfo` (from MiKTeX/TeX Live) is optional in v1.00.
- This validator is called by `ArticleGeneratorSDK.compile_pdf()` after `MultiPassCompiler.compile()` returns.
