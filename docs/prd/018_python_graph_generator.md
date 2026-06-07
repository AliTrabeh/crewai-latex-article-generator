---
id: "018"
title: "Python Graph Generator"
group: "6 — Assets Generation"
priority: medium
---

# Task 018 — Python Graph Generator

## Goal

Implement a service that generates figures (line charts, bar charts) using `matplotlib` and exports them as PDF or PNG files that can be `\includegraphics`-referenced from the LaTeX document.

## Files to Create or Modify

- `src/latex_article_generator/services/graph_generator.py` — `GraphGenerator` class
- `assets/` — output directory for generated graph files

## Exact Expected Behavior

```python
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt

class GraphGenerator:
    def __init__(self, output_dir: str = "assets") -> None:
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def line_chart(self, data: dict, title: str, filename: str) -> str:
        """Generate a line chart; return absolute path to saved file."""
        fig, ax = plt.subplots()
        for label, values in data.items():
            ax.plot(values, label=label)
        ax.set_title(title)
        ax.legend()
        path = self._output_dir / filename
        fig.savefig(str(path), bbox_inches="tight")
        plt.close(fig)
        return str(path)

    def bar_chart(self, categories: list[str], values: list[float],
                  title: str, filename: str) -> str:
        """Generate a bar chart; return absolute path to saved file."""
        fig, ax = plt.subplots()
        ax.bar(categories, values)
        ax.set_title(title)
        path = self._output_dir / filename
        fig.savefig(str(path), bbox_inches="tight")
        plt.close(fig)
        return str(path)
```

## Acceptance Criteria

- [ ] `generator.line_chart({"A": [1, 2, 3]}, "Test", "test.pdf")` creates `assets/test.pdf`.
- [ ] `generator.bar_chart(["X", "Y"], [1.0, 2.0], "Bar", "bar.png")` creates `assets/bar.png`.
- [ ] `plt.close(fig)` is called after every save to prevent memory leaks.
- [ ] Output files are valid image/PDF files (non-zero bytes).
- [ ] `matplotlib` backend is set to `"Agg"` to avoid display errors in headless environments.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Add `matplotlib` as a dependency: `uv add matplotlib`.
- Output filenames should use `.pdf` for LaTeX inclusion (vector) or `.png` for raster.
- The generated file paths are injected into the LaTeX template via `\includegraphics{assets/filename}`.
