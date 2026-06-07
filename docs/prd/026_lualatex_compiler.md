---
id: "026"
title: "LuaLaTeX Single-Pass Runner"
group: "8 — PDF Compilation"
priority: critical
status: NOT_STARTED
---

# Task 026 — LuaLaTeX Single-Pass Runner

## Goal

Implement a low-level runner that executes a single `lualatex` pass on a `.tex` file, captures stdout/stderr, and raises a clear exception if compilation fails.

## Files to Create or Modify

- `src/latex_article_generator/services/compiler.py` — `LuaLatexRunner` class (and later `MultiPassCompiler`)

## Exact Expected Behavior

```python
import subprocess
from pathlib import Path

class LuaLatexRunner:
    def __init__(self, miktex_bin: str = "lualatex") -> None:
        self._bin = miktex_bin

    def run(self, tex_path: str, output_dir: str) -> subprocess.CompletedProcess:
        """Run a single lualatex pass; raise CompilationError on non-zero exit."""
        result = subprocess.run(
            [
                self._bin,
                "--interaction=nonstopmode",
                "--output-directory", output_dir,
                tex_path,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise CompilationError(
                f"lualatex failed (exit {result.returncode}):\n{result.stderr}"
            )
        return result

class CompilationError(RuntimeError):
    pass
```

## Acceptance Criteria

- [ ] `runner.run("valid.tex", "/tmp")` returns `CompletedProcess` on success.
- [ ] `runner.run("broken.tex", "/tmp")` raises `CompilationError` with stderr content.
- [ ] Timeout of 120 seconds is enforced.
- [ ] `--interaction=nonstopmode` is always passed (prevents interactive prompts).
- [ ] Unit tests mock `subprocess.run` to avoid requiring a real LaTeX installation.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- `lualatex` must be on the system PATH (MiKTeX or TeX Live). Document this requirement in README.
- `--output-directory` is required to keep build artifacts out of the source directory.
- `capture_output=True` is equivalent to `stdout=PIPE, stderr=PIPE` — do not use both forms.
