---
id: "039"
title: "Unit Tests — LaTeX Generation and Compilation"
group: "12 — Testing and Final Submission Cleanup"
priority: high
status: NOT_STARTED
---

# Task 039 — Unit Tests for LaTeX Generation and Compilation

## Goal

Write unit tests for `LatexTemplate`, `LaTeXAssembler`, `LuaLatexRunner`, `BiberRunner`, and `MultiPassCompiler`.

## Files to Create or Modify

- `tests/unit/test_latex_template.py` — LatexTemplate tests
- `tests/unit/test_latex_assembler.py` — LaTeXAssembler tests
- `tests/unit/test_compiler.py` — LuaLatexRunner, BiberRunner, MultiPassCompiler tests

## Exact Expected Behavior

**LatexTemplate:**
```python
def test_preamble_contains_documentclass():
    tmpl = LatexTemplate()
    result = tmpl.render_preamble("T", "A", "2026", "refs.bib")
    assert r"\documentclass" in result

def test_preamble_contains_polyglossia():
    tmpl = LatexTemplate()
    result = tmpl.render_preamble("T", "A", "2026", "refs.bib")
    assert "polyglossia" in result
```

**LaTeXAssembler:**
```python
def test_assembler_writes_file(tmp_path):
    assembler = LaTeXAssembler()
    out = tmp_path / "out.tex"
    assembler.assemble("preamble", "cover", "toc", "hf",
                       {"Intro": "content"}, "refs.bib", str(out))
    assert out.exists()
    assert r"\section{Intro}" in out.read_text()
```

**LuaLatexRunner:**
```python
@patch("subprocess.run")
def test_runner_raises_on_nonzero(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stderr="error")
    with pytest.raises(CompilationError):
        LuaLatexRunner().run("file.tex", "/tmp")
```

**MultiPassCompiler:**
```python
@patch.object(LuaLatexRunner, "run")
@patch.object(BiberRunner, "run")
def test_multi_pass_calls_four_passes(mock_biber, mock_lualatex, tmp_path):
    # mock PDF creation
    ...
    assert mock_lualatex.call_count == 3
    assert mock_biber.call_count == 1
```

## Acceptance Criteria

- [ ] `LuaLatexRunner` and `BiberRunner` tests mock `subprocess.run` — no real LaTeX calls.
- [ ] `MultiPassCompiler` test verifies exactly 3 lualatex + 1 biber calls.
- [ ] `LaTeXAssembler` tests use `tmp_path` pytest fixture.
- [ ] Coverage for compiler and template modules ≥ 85%.
- [ ] All tests pass in under 5 seconds total.

## Notes / Constraints

- `MultiPassCompiler` creates a temp directory internally — tests need to mock the PDF file creation or the runner calls.
- `CompilationError` must be importable from `latex_article_generator.services.compiler`.
- Test the `timeout=120` enforcement by mocking `subprocess.run` to raise `subprocess.TimeoutExpired`.
