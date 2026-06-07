"""LuaLaTeX runner, Biber runner, and multi-pass compiler — tasks 026–028."""

import shutil
import subprocess
import tempfile
from pathlib import Path


class CompilationError(RuntimeError):
    pass


class LuaLatexRunner:
    def __init__(self, miktex_bin: str = "lualatex") -> None:
        self._bin = miktex_bin

    def run(self, tex_path: str, output_dir: str) -> subprocess.CompletedProcess:
        """Run a single lualatex pass; raise CompilationError on non-zero exit."""
        result = subprocess.run(
            [self._bin, "--interaction=nonstopmode", "--output-directory", output_dir, tex_path],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise CompilationError(
                f"lualatex failed (exit {result.returncode}):\n{result.stderr}"
            )
        return result


class BiberRunner:
    def __init__(self, biber_bin: str = "biber") -> None:
        self._bin = biber_bin

    def run(self, aux_basename: str, output_dir: str) -> subprocess.CompletedProcess:
        """Run biber on aux_basename; raise CompilationError on non-zero exit."""
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


class MultiPassCompiler:
    def __init__(self, config) -> None:
        self._runner = LuaLatexRunner()
        self._biber = BiberRunner()

    def compile(self, latex_source: str, output_path: str) -> str:
        """Write source to temp dir, run 4-pass compilation, copy PDF to output_path."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tex_file = str(Path(tmp_dir) / "article.tex")
            Path(tex_file).write_text(latex_source, encoding="utf-8")

            self._runner.run(tex_file, tmp_dir)
            self._biber.run(str(Path(tmp_dir) / "article"), tmp_dir)
            self._runner.run(tex_file, tmp_dir)
            self._runner.run(tex_file, tmp_dir)

            pdf_src = str(Path(tmp_dir) / "article.pdf")
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdf_src, output_path)

        return output_path
