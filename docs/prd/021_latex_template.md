---
id: "021"
title: "Base LaTeX Template"
group: "7 — LaTeX Document Generation"
priority: critical
status: NOT_STARTED
---

# Task 021 — Base LaTeX Template

## Goal

Define the base `.tex` preamble template that all generated articles will use. The preamble must include all packages required for academic formatting, BiDi text, TikZ, BibTeX, and LuaLaTeX.

## Files to Create or Modify

- `src/latex_article_generator/services/latex_template.py` — `LatexTemplate` class
- `assets/templates/base_article.tex` — template file (optional: can be embedded as string)

## Exact Expected Behavior

```python
PREAMBLE_TEMPLATE = r"""
\documentclass[12pt,a4paper]{{article}}

% Encoding and language
\usepackage{{fontspec}}
\usepackage{{polyglossia}}
\setmainlanguage{{english}}
\setotherlanguage{{hebrew}}
\newfontfamily\hebrewfont[Script=Hebrew]{{David CLM}}

% Layout
\usepackage{{geometry}}
\geometry{{margin=2.5cm}}
\usepackage{{setspace}}
\onehalfspacing

% Graphics and diagrams
\usepackage{{graphicx}}
\usepackage{{tikz}}
\usetikzlibrary{{shapes,arrows,positioning}}
\usepackage{{float}}

% Math
\usepackage{{amsmath,amssymb}}

% Bibliography
\usepackage[backend=biber,style=ieee]{{biblatex}}
\addbibresource{{{bib_file}}}

% Hyperlinks
\usepackage{{hyperref}}
\hypersetup{{colorlinks=true,linkcolor=blue,citecolor=blue}}

% Headers/Footers
\usepackage{{fancyhdr}}
\pagestyle{{fancy}}

\title{{{title}}}
\author{{{author}}}
\date{{{date}}}
"""

class LatexTemplate:
    def render_preamble(self, title: str, author: str, date: str, bib_file: str) -> str:
        return PREAMBLE_TEMPLATE.format(
            title=title, author=author, date=date, bib_file=bib_file
        )
```

## Acceptance Criteria

- [ ] `render_preamble("Title", "Author", "2026-06", "refs.bib")` returns a string containing `\documentclass`.
- [ ] Output contains `polyglossia`, `fontspec`, `tikz`, `biblatex`, `graphicx`.
- [ ] `{bib_file}` placeholder is replaced correctly.
- [ ] Compiled with LuaLaTeX on an empty `\begin{document}\end{document}` without errors.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Use `lualatex` (not `pdflatex`) — `fontspec` and `polyglossia` require LuaLaTeX or XeLaTeX.
- `David CLM` is a common Hebrew font in MiKTeX; fall back to `FreeSerif` if unavailable.
- The template uses `{{` / `}}` escaping because `str.format()` is used — not an f-string.
