"""Validators for LaTeX source, PDF output, and content completeness — tasks 029–031."""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class LatexValidator:
    REQUIRED_SECTIONS = [r"\begin{document}", r"\end{document}", r"\maketitle"]

    def validate(self, latex_source: str) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
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
        begins = re.findall(r"\\begin\{(\w+)\}", src)
        ends = re.findall(r"\\end\{(\w+)\}", src)
        if begins != ends:
            errors.append(f"Unbalanced environments: begins={begins}, ends={ends}")


class PdfValidator:
    MIN_FILE_SIZE_BYTES = 1024
    MIN_PAGE_COUNT = 3

    def validate(self, pdf_path: str) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
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


class ContentCompletenessChecker:
    MIN_WORDS_PER_SECTION = 300
    REQUIRED_SECTIONS = ["introduction", "methodology", "conclusion"]

    def check(self, sections: dict[str, str], has_hebrew: bool = False) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
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
