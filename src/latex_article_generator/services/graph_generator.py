"""Matplotlib graph generator — task 018."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


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

    def bar_chart(
        self, categories: list[str], values: list[float], title: str, filename: str
    ) -> str:
        """Generate a bar chart; return absolute path to saved file."""
        fig, ax = plt.subplots()
        ax.bar(categories, values)
        ax.set_title(title)
        path = self._output_dir / filename
        fig.savefig(str(path), bbox_inches="tight")
        plt.close(fig)
        return str(path)
