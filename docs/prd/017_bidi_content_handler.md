---
id: "017"
title: "BiDi Content Handler"
group: "5 — Content Generation Pipeline"
priority: high
status: DONE
---

# Task 017 — BiDi Content Handler

## Goal

Implement a utility that detects Hebrew text segments in the article content and wraps them with the correct LuaLaTeX bidirectional directives, ensuring proper RTL rendering.

## Files to Create or Modify

- `src/latex_article_generator/services/bidi_handler.py` — `BiDiHandler` class

## Exact Expected Behavior

```python
import re

HEBREW_RANGE = re.compile(r'[א-תװ-״יִ-ﭏ]+')

class BiDiHandler:
    """Wraps Hebrew text segments in LuaLaTeX RTL directives."""

    def process(self, text: str) -> str:
        """Return text with Hebrew segments wrapped in \\begin{RTL}...\\end{RTL}."""
        return HEBREW_RANGE.sub(self._wrap_rtl, text)

    def contains_hebrew(self, text: str) -> bool:
        """Return True if text contains any Hebrew characters."""
        return bool(HEBREW_RANGE.search(text))

    def _wrap_rtl(self, match: re.Match) -> str:
        return f"\\begin{{RTL}}{match.group()}\\end{{RTL}}"
```

The processed text is then embedded into the LaTeX document. The LaTeX preamble must include `\usepackage{bidi}` (or `polyglossia` for LuaLaTeX).

## Acceptance Criteria

- [ ] `handler.process("Hello שלום World")` returns `"Hello \\begin{RTL}שלום\\end{RTL} World"`.
- [ ] `handler.contains_hebrew("English only")` returns `False`.
- [ ] `handler.contains_hebrew("עברית")` returns `True`.
- [ ] Consecutive Hebrew words in one run are wrapped in a single `\begin{RTL}...\end{RTL}` block.
- [ ] Pure ASCII/Latin input passes through unchanged.
- [ ] File ≤ 150 lines.

## Notes / Constraints

- Unicode range `א–ת` covers the Hebrew block; additional ranges cover extended Hebrew characters.
- The LaTeX preamble (task 021) must load `bidi` or `polyglossia` package for RTL support — `BiDiHandler` only wraps text, it does not modify the preamble.
- Do not attempt to handle Arabic or other RTL scripts in v1.00 — Hebrew only.
