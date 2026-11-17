"""Small shared helpers: tokenizing, quote normalization, rate limiting."""

from __future__ import annotations

import asyncio
import re
import time
import unicodedata

STOPWORDS = frozenset(
    """a about above after again against all am an and any are as at be because been before being below
    between both but by can could did do does doing down during each few for from further had has have having
    he her here hers herself him himself his how i if in into is it its itself just me more most my myself no
    nor not now of off on once only or other our ours ourselves out over own same she should so some such than
    that the their theirs them themselves then there these they this those through to too under until up very
    was we were what when where which while who whom why will with would you your yours yourself yourselves
    im ive id dont didnt doesnt isnt wasnt cant wont also really like get got just one even still much would
    know think thing things lot way going make made anyone someone something anything every would could
    reddit post thread comment comments edit deleted removed http https www com amp""".split()
)

_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9'\-]*[a-z0-9]|[a-z0-9]")


def tokens(text: str | None) -> list[str]:
    """Lowercase content words (stopwords and 1-letter tokens dropped, possessives stripped)."""
    if not text:
        return []
    out = []
    for tok in _TOKEN_RE.findall(text.lower()):
        tok = tok.replace("'", "")
        if tok.endswith("s") and len(tok) > 4 and not tok.endswith("ss"):
            tok = tok[:-1]  # crude plural folding: "oils" ~ "oil"
        if len(tok) > 1 and tok not in STOPWORDS and not tok.replace("-", "").isdigit():
            out.append(tok)
    return out


_QUOTE_MAP = str.maketrans({
    "‘": "'", "’": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "‟": '"', "″": '"',
    "–": "-", "—": "-", "−": "-", " ": " ",
})


def normalize_for_match(text: str) -> str:
    """Normalize only what doesn't change the words: unicode form, curly quotes, dashes, whitespace,
    markdown emphasis characters and letter case."""
    text = unicodedata.normalize("NFKC", text or "").translate(_QUOTE_MAP)
    text = re.sub(r"[*_~`>]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def quote_in_text(quote: str, source: str) -> bool:
    """True when every part of `quote` (split on ... or …) appears in `source`, in order."""
    parts = [p.strip(" \"'") for p in re.split(r"\.\.\.|…|\[\.\.\.\]", quote or "")]
    parts = [normalize_for_match(p) for p in parts if p.strip(" \"'")]
    if not parts or sum(len(p) for p in parts) < 8:
        return False
    hay = normalize_for_match(source)
    pos = 0
    for part in parts:
        idx = hay.find(part, pos)
        if idx < 0:
            return False
        pos = idx + len(part)
    return True


class RateLimiter:
    """Enforces a minimum interval between calls (async). One per source."""

    def __init__(self, min_interval: float):
        self.min_interval = min_interval
        self._last = 0.0
        self._lock = asyncio.Lock()

    async def wait(self) -> None:
        async with self._lock:
            delay = self._last + self.min_interval - time.monotonic()
            if delay > 0:
                await asyncio.sleep(delay)
            self._last = time.monotonic()


def strip_prefix(fullname: str | None) -> str | None:
    if not fullname:
        return None
    return fullname.split("_", 1)[1] if re.match(r"^t\d_", fullname) else fullname


def clip(text: str | None, n: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"
