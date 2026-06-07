---
id: "020"
title: "TikZ Diagram Generator"
group: "6 — Assets Generation"
priority: medium
status: NOT_STARTED
---

# Task 020 — TikZ Diagram Generator

## Goal

Implement a utility that generates TikZ LaTeX code for block diagrams, flowcharts, and system architecture diagrams that are embedded directly in the LaTeX document.

## Files to Create or Modify

- `src/latex_article_generator/services/tikz_generator.py` — `TikZGenerator` class

## Exact Expected Behavior

```python
class TikZGenerator:
    def block_diagram(self, nodes: list[dict], edges: list[tuple[str, str]]) -> str:
        """
        Generate TikZ code for a block diagram.

        nodes: list of {"id": str, "label": str, "x": float, "y": float}
        edges: list of (from_id, to_id)
        Returns a complete tikzpicture environment string.
        """
        lines = ["\\begin{tikzpicture}[node distance=2cm]"]
        for node in nodes:
            lines.append(
                f"  \\node[draw, rectangle] ({node['id']}) "
                f"at ({node['x']},{node['y']}) {{{node['label']}}};"
            )
        for src, dst in edges:
            lines.append(f"  \\draw[->] ({src}) -- ({dst});")
        lines.append("\\end{tikzpicture}")
        return "\n".join(lines)

    def flowchart(self, steps: list[str]) -> str:
        """Generate a simple vertical flowchart from a list of step labels."""
        lines = ["\\begin{tikzpicture}[node distance=1.5cm]"]
        prev = None
        for i, step in enumerate(steps):
            node_id = f"step{i}"
            shape = "diamond" if step.startswith("?") else "rectangle"
            lines.append(
                f"  \\node[draw, {shape}] ({node_id}) {{{step.lstrip('?')}}};"
            )
            if prev:
                lines.append(f"  \\draw[->] ({prev}) -- ({node_id});")
            prev = node_id
        lines.append("\\end{tikzpicture}")
        return "\n".join(lines)
```

## Acceptance Criteria

- [ ] `generator.block_diagram([{"id":"a","label":"A","x":0,"y":0}], [])` contains `\begin{tikzpicture}`.
- [ ] Edge `("a","b")` produces `\draw[->] (a) -- (b);`.
- [ ] `generator.flowchart(["Start", "?Decision", "End"])` produces a diamond for "Decision".
- [ ] Output is a valid string (no exception raised with valid inputs).
- [ ] File ≤ 150 lines.

## Notes / Constraints

- The LaTeX preamble (task 021) must include `\usepackage{tikz}` — this generator only produces the picture environment content.
- TikZ is part of MiKTeX/TeX Live — no additional installation needed on a standard LaTeX distribution.
- The generated TikZ code is inserted into the `.tex` file by the LaTeX assembler (task 025).
