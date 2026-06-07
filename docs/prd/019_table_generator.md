---
id: "019"
title: "LaTeX Table Generator"
group: "6 — Assets Generation"
priority: medium
status: DONE
---

# Task 019 — LaTeX Table Generator

## Goal

Implement a utility that takes structured tabular data and produces valid LaTeX `tabular` markup that can be inserted directly into the document.

## Files to Create or Modify

- `src/latex_article_generator/services/table_generator.py` — `TableGenerator` class

## Exact Expected Behavior

```python
class TableGenerator:
    def generate(
        self,
        headers: list[str],
        rows: list[list[str]],
        caption: str = "",
        label: str = "",
        alignment: str | None = None,
    ) -> str:
        """Return a LaTeX table string wrapped in a figure/table environment."""
        col_spec = alignment or "|" + "l|" * len(headers)
        lines = [
            "\\begin{table}[h]",
            "\\centering",
            f"\\begin{{tabular}}{{{col_spec}}}",
            "\\hline",
            " & ".join(f"\\textbf{{{h}}}" for h in headers) + " \\\\",
            "\\hline",
        ]
        for row in rows:
            lines.append(" & ".join(str(cell) for cell in row) + " \\\\")
        lines += [
            "\\hline",
            "\\end{tabular}",
        ]
        if caption:
            lines.append(f"\\caption{{{caption}}}")
        if label:
            lines.append(f"\\label{{tab:{label}}}")
        lines.append("\\end{table}")
        return "\n".join(lines)
```

## Acceptance Criteria

- [ ] `generator.generate(["A", "B"], [["1", "2"]])` returns a string containing `\begin{tabular}`.
- [ ] Output contains `\hline` between header and rows.
- [ ] Headers are wrapped in `\textbf{}`.
- [ ] `\caption{}` appears when `caption` is non-empty.
- [ ] `\label{tab:X}` appears when `label` is non-empty.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Do not use any external LaTeX table library — generate the markup directly.
- The caller is responsible for inserting the returned string at the correct position in the document.
- Long cell values should be escaped (replace `&` → `\&`, `%` → `\%`, `_` → `\_`) before being passed to `generate()` — add a static `escape()` helper method.
