"""BiDi content handler — wraps Hebrew segments in LuaLaTeX RTL directives."""

import re

# Matches one or more Hebrew characters (including extended ranges),
# then greedily absorbs any whitespace followed by more Hebrew so that
# consecutive Hebrew words form a single RTL block.
_HEBREW = re.compile(r"[א-תװ-״יִ-ﭏ]+(?:\s+[א-תװ-״יִ-ﭏ]+)*")


class BiDiHandler:
    """Wraps Hebrew text segments in LuaLaTeX RTL directives."""

    def process(self, text: str) -> str:
        """Return *text* with Hebrew segments wrapped in \\begin{RTL}...\\end{RTL}."""
        return _HEBREW.sub(self._wrap_rtl, text)

    def contains_hebrew(self, text: str) -> bool:
        """Return True if *text* contains any Hebrew characters."""
        return bool(_HEBREW.search(text))

    def _wrap_rtl(self, match: re.Match) -> str:  # type: ignore[type-arg]
        return rf"\begin{{RTL}}{match.group()}\end{{RTL}}"
