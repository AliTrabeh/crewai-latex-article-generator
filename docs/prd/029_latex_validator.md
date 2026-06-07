---
id: "029"
title: "LaTeX Source Validator"
group: "9 — Validation and Checking System"
priority: high
status: NOT_STARTED
---

# Task 029 — LaTeX Source Validator

## Goal

Implement a pre-compilation validator that checks the LaTeX source for common structural errors before invoking the compiler, saving time and producing clearer error messages.

## Files to Create or Modify

- `src/latex_article_generator/services/validators.py` — `LatexValidator` class

## Exact Expected Behavior

```python
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

class LatexValidator:
    REQUIRED_SECTIONS = [r"\begin{document}", r"\end{document}", r"\maketitle"]

    def validate(self, latex_source: str) -> ValidationResult:
        errors, warnings = [], []
        self._check_required_sections(latex_source, errors)
        self._check_balanced_braces(latex_source, errors)
        self._check_balanced_environments(latex_source, errors)
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def _check_required_sections(self, src: str, errors: list) -> None:
        for section in self.REQUIRED_SECTIONS:
            if section not in src:
                errors.append(f"Missing required command: {section}")

    def _check_balanced_braces(self, src: str, errors: list) -> None:
        depth = 0
        for ch in src:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            if depth < 0:
                errors.append("Unmatched closing brace '}'")
                return
        if depth != 0:
            errors.append(f"Unmatched opening brace(s): {depth} unclosed")

    def _check_balanced_environments(self, src: str, errors: list) -> None:
        import re
        begins = re.findall(r"\\begin\{(\w+)\}", src)
        ends = re.findall(r"\\end\{(\w+)\}", src)
        if begins != ends:
            errors.append(f"Unbalanced environments: begins={begins}, ends={ends}")
```

## Acceptance Criteria

- [ ] Valid LaTeX returns `ValidationResult(valid=True, errors=[])`.
- [ ] Missing `\begin{document}` → error in `errors` list.
- [ ] Unclosed brace → brace error in `errors` list.
- [ ] Mismatched `\begin{X}` / `\end{Y}` → environment error.
- [ ] File ≤ 150 lines (shared with tasks 030 and 031).

## Notes / Constraints

- This validator runs before compilation — do not invoke `subprocess` here.
- False positives are acceptable for edge cases (e.g., braces in comments). Speed over perfect accuracy.
- If validation fails, `MultiPassCompiler.compile()` must raise `ValidationError` before calling lualatex.
