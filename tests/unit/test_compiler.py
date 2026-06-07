"""Tests for LuaLatexRunner, BiberRunner, MultiPassCompiler (tasks 026–028)."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from latex_article_generator.services.compiler import (
    BiberRunner,
    CompilationError,
    LuaLatexRunner,
    MultiPassCompiler,
)

_TARGET = "latex_article_generator.services.compiler"
_SUBPROCESS = f"{_TARGET}.subprocess.run"


@pytest.fixture
def ok_proc():
    proc = MagicMock(spec=subprocess.CompletedProcess)
    proc.returncode = 0
    return proc


# --- LuaLatexRunner ---

def test_runner_returns_completed_process(ok_proc):
    with patch(_SUBPROCESS, return_value=ok_proc):
        result = LuaLatexRunner().run("doc.tex", "/tmp")
    assert result is ok_proc


def test_runner_raises_compilation_error_on_nonzero():
    proc = MagicMock(returncode=1, stderr="fatal error")
    with patch(_SUBPROCESS, return_value=proc), pytest.raises(CompilationError, match="lualatex failed"):
        LuaLatexRunner().run("bad.tex", "/tmp")


def test_runner_passes_nonstopmode(ok_proc):
    with patch(_SUBPROCESS, return_value=ok_proc) as m:
        LuaLatexRunner().run("doc.tex", "/tmp")
    assert "--interaction=nonstopmode" in m.call_args[0][0]


def test_runner_passes_output_directory(ok_proc):
    with patch(_SUBPROCESS, return_value=ok_proc) as m:
        LuaLatexRunner().run("doc.tex", "/out")
    cmd = m.call_args[0][0]
    assert "--output-directory" in cmd
    assert "/out" in cmd


def test_runner_timeout_is_120(ok_proc):
    with patch(_SUBPROCESS, return_value=ok_proc) as m:
        LuaLatexRunner().run("doc.tex", "/tmp")
    assert m.call_args[1]["timeout"] == 120


# --- BiberRunner ---

def test_biber_returns_completed_process(ok_proc):
    with patch(_SUBPROCESS, return_value=ok_proc):
        result = BiberRunner().run("/tmp/article", "/tmp")
    assert result is ok_proc


def test_biber_raises_compilation_error_on_nonzero():
    proc = MagicMock(returncode=1, stderr="biber error")
    with patch(_SUBPROCESS, return_value=proc), pytest.raises(CompilationError, match="biber failed"):
        BiberRunner().run("/tmp/article", "/tmp")


def test_biber_passes_output_directory(ok_proc):
    with patch(_SUBPROCESS, return_value=ok_proc) as m:
        BiberRunner().run("/tmp/article", "/out")
    cmd = m.call_args[0][0]
    assert "--output-directory" in cmd
    assert "/out" in cmd


def test_biber_timeout_is_60(ok_proc):
    with patch(_SUBPROCESS, return_value=ok_proc) as m:
        BiberRunner().run("/tmp/article", "/tmp")
    assert m.call_args[1]["timeout"] == 60


# --- MultiPassCompiler ---

@pytest.fixture
def compiler_mocks():
    with (
        patch(f"{_TARGET}.LuaLatexRunner") as mock_lua_cls,
        patch(f"{_TARGET}.BiberRunner") as mock_biber_cls,
        patch(f"{_TARGET}.shutil.copy2") as mock_copy,
    ):
        yield mock_lua_cls.return_value, mock_biber_cls.return_value, mock_copy


def test_compile_returns_output_path(compiler_mocks, tmp_path):
    out = str(tmp_path / "out.pdf")
    assert MultiPassCompiler({}).compile("\\documentclass{article}", out) == out


def test_compile_three_lualatex_passes(compiler_mocks):
    mock_runner, _, _ = compiler_mocks
    MultiPassCompiler({}).compile("src", "/any/out.pdf")
    assert mock_runner.run.call_count == 3


def test_compile_one_biber_pass(compiler_mocks):
    _, mock_biber, _ = compiler_mocks
    MultiPassCompiler({}).compile("src", "/any/out.pdf")
    assert mock_biber.run.call_count == 1


def test_compile_copies_pdf_to_output(compiler_mocks, tmp_path):
    _, _, mock_copy = compiler_mocks
    out = str(tmp_path / "result.pdf")
    MultiPassCompiler({}).compile("src", out)
    assert mock_copy.call_args[0][1] == out


def test_compile_propagates_compilation_error(compiler_mocks):
    mock_runner, _, _ = compiler_mocks
    mock_runner.run.side_effect = CompilationError("lualatex failed")
    with pytest.raises(CompilationError):
        MultiPassCompiler({}).compile("src", "/any/out.pdf")


def test_compile_pass_order(compiler_mocks):
    mock_runner, mock_biber, _ = compiler_mocks
    log = []
    mock_runner.run.side_effect = lambda *a, **kw: log.append("lua")
    mock_biber.run.side_effect = lambda *a, **kw: log.append("biber")
    MultiPassCompiler({}).compile("src", "/any/out.pdf")
    assert log == ["lua", "biber", "lua", "lua"]
