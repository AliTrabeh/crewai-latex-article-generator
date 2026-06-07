"""TikZ diagram generator — task 020."""


class TikZGenerator:
    def block_diagram(self, nodes: list[dict], edges: list[tuple[str, str]]) -> str:
        """
        Generate TikZ code for a block diagram.

        nodes: list of {"id": str, "label": str, "x": float, "y": float}
        edges: list of (from_id, to_id)
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
