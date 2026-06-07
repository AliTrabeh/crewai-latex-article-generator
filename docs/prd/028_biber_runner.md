---
id: "028"
title: "Biber Runner"
group: "8 — PDF Compilation"
priority: high
status: DONE
---

# Task 028 — Biber Runner

## Goal

Implement `BiberRunner` that executes `biber` between compilation passes to process the bibliography database and resolve `\cite{}` commands.

## Files to Create or Modify

- `src/latex_article_generator/services/compiler.py` — add `BiberRunner` class

## Exact Expected Behavior

```python
class BiberRunner:
    def __init__(self, biber_bin: str = "biber") -> None:
        self._bin = biber_bin

    def run(self, aux_basename: str, output_dir: str) -> subprocess.CompletedProcess:
        """
        Run biber on the aux_basename (path without extension).
        Raises CompilationError if biber exits non-zero.
        """
        result = subprocess.run(
            [self._bin, "--output-directory", output_dir, aux_basename],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            raise CompilationError(
                f"biber failed (exit {result.returncode}):\n{result.stderr}"
            )
        return result
```

## Acceptance Criteria

- [ ] `biber_runner.run("/tmp/article", "/tmp")` calls `biber` with correct args.
- [ ] Non-zero exit from `biber` raises `CompilationError`.
- [ ] Timeout of 60 seconds is enforced.
- [ ] Unit tests mock `subprocess.run`.
- [ ] File ≤ 150 lines (shared with compiler.py from tasks 026, 027).

## Notes / Constraints

- `biber` requires the `.bcf` file from the first `lualatex` pass to be present in `output_dir`.
- `aux_basename` is the path without extension, e.g., `/tmp/build/article` (not `article.aux`).
- `biber` must be on the system PATH — document this in README alongside `lualatex` requirement.
- If `biber` is not installed, `CompilationError` is raised with a hint message to install it.
