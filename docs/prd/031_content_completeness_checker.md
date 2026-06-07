---
id: "031"
title: "Content Completeness Checker"
group: "9 — Validation and Checking System"
priority: medium
status: NOT_STARTED
---

# Task 031 — Content Completeness Checker

## Goal

Implement a checker that verifies the generated article content contains all required sections, meets minimum word counts, and includes at least one Hebrew section.

## Files to Create or Modify

- `src/latex_article_generator/services/validators.py` — add `ContentCompletenessChecker` class

## Exact Expected Behavior

```python
class ContentCompletenessChecker:
    MIN_WORDS_PER_SECTION = 300
    REQUIRED_SECTIONS = ["introduction", "methodology", "conclusion"]

    def check(self, sections: dict[str, str], has_hebrew: bool = False) -> ValidationResult:
        errors, warnings = [], []
        self._check_required_sections(sections, errors)
        self._check_word_counts(sections, errors)
        if not has_hebrew:
            warnings.append(
                "No Hebrew content detected. At least one section should demonstrate BiDi."
            )
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def _check_required_sections(self, sections: dict[str, str], errors: list) -> None:
        for req in self.REQUIRED_SECTIONS:
            if not any(req.lower() in k.lower() for k in sections):
                errors.append(f"Missing required section: '{req}'")

    def _check_word_counts(self, sections: dict[str, str], errors: list) -> None:
        for name, content in sections.items():
            word_count = len(content.split())
            if word_count < self.MIN_WORDS_PER_SECTION:
                errors.append(
                    f"Section '{name}' too short: {word_count} words "
                    f"(min {self.MIN_WORDS_PER_SECTION})"
                )
```

## Acceptance Criteria

- [ ] All required sections present and ≥ 300 words → `valid=True`.
- [ ] Missing "introduction" → error in `errors`.
- [ ] Section with 50 words → word count error.
- [ ] No Hebrew → warning (not error) in `warnings`.
- [ ] File ≤ 150 lines (shared with validators.py).

## Notes / Constraints

- Word count is computed on the raw text before LaTeX encoding — count words in the content strings, not in the `.tex` output.
- "introduction" match is case-insensitive and substring-based.
- `has_hebrew` is provided by `BiDiHandler.contains_hebrew()` (task 017).
