"""XeLaTeX runner, Biber runner, and multi-pass compiler — tasks 026–028."""

import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


class CompilationError(RuntimeError):
    """Raised when xelatex or biber exits with a non-zero return code."""


class LuaLatexRunner:
    """Thin wrapper around the xelatex binary for a single compilation pass."""

    def __init__(self, miktex_bin: str = "xelatex") -> None:
        self._bin = miktex_bin

    def run(self, tex_path: str, output_dir: str) -> subprocess.CompletedProcess:
        """Run a single xelatex pass; raise CompilationError on non-zero exit."""
        result = subprocess.run(
            [self._bin, "--interaction=nonstopmode", "--output-directory", output_dir, tex_path],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
        )
        if result.returncode != 0:
            output = result.stdout or result.stderr or "(no output)"
            raise CompilationError(
                f"xelatex failed (exit {result.returncode}):\n{output[-3000:]}"
            )
        return result


class BiberRunner:
    """Thin wrapper around the biber binary for bibliography processing."""

    def __init__(self, biber_bin: str = "biber") -> None:
        self._bin = biber_bin

    def run(self, aux_basename: str, output_dir: str) -> subprocess.CompletedProcess:
        """Run biber on aux_basename; raise CompilationError on non-zero exit."""
        result = subprocess.run(
            [self._bin, "--output-directory", output_dir, aux_basename],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
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
        tmp_dir = tempfile.mkdtemp(prefix="latex_build_")
        try:
            latex_source = self._localize_bib_files(latex_source, tmp_dir)

            tex_file = str(Path(tmp_dir) / "article.tex")
            pdf_tmp = Path(tmp_dir) / "article.pdf"
            Path(tex_file).write_text(latex_source, encoding="utf-8")

            # Pass 1: tolerate non-zero if a PDF was produced (biblatex errors before biber runs)
            self._run_tolerant(tex_file, tmp_dir, pdf_tmp)
            self._biber.run(str(Path(tmp_dir) / "article"), tmp_dir)
            self._runner.run(tex_file, tmp_dir)
            self._runner.run(tex_file, tmp_dir)

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            self._copy_with_retry(str(pdf_tmp), output_path)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        return output_path

    @staticmethod
    def _copy_with_retry(src: str, dst: str, retries: int = 8, delay: float = 2.0) -> None:
        """Copy PDF, working around Windows Defender's temporary lock on freshly-written files."""
        for attempt in range(retries):
            try:
                # read_bytes / write_bytes bypasses the CopyFile API that Defender intercepts
                data = Path(src).read_bytes()
                Path(dst).write_bytes(data)
                return
            except PermissionError:
                if attempt == retries - 1:
                    raise
                time.sleep(delay)

    def _run_tolerant(self, tex_file: str, output_dir: str, pdf_path: Path) -> None:
        """Run xelatex; only re-raise if no PDF was produced (pass-1 biblatex errors are expected)."""
        try:
            self._runner.run(tex_file, output_dir)
        except CompilationError:
            if not pdf_path.exists():
                raise

    @staticmethod
    def _localize_bib_files(source: str, tmp_dir: str) -> str:
        """Copy .bib files referenced via \\addbibresource into tmp_dir, rewrite to filename-only."""
        def _replace(m: re.Match) -> str:
            bib_path = Path(m.group(1))
            if bib_path.exists():
                dest = Path(tmp_dir) / bib_path.name
                shutil.copy2(str(bib_path), str(dest))
                return r"\addbibresource{" + bib_path.name + "}"
            return m.group(0)

        return re.sub(r"\\addbibresource\{([^}]+)\}", _replace, source)
