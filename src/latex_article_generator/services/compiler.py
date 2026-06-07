"""Multi-pass LaTeX compiler — implemented in task 027."""


class MultiPassCompiler:
    """Compiles LaTeX source to PDF via a 4-pass pipeline. Stub — see task 027."""

    def __init__(self, config) -> None:
        self._config = config

    def compile(self, latex_source: str, output_path: str) -> str:
        """Run lualatex → biber → lualatex → lualatex; return PDF path."""
        raise NotImplementedError("MultiPassCompiler will be implemented in task 027.")
