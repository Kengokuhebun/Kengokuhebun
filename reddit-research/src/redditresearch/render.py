"""Compact, token-budgeted text views of threads for Claude to read."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from .store import Store
from .util import clip, strip_prefix

DEAD = ("[deleted]", "[removed]")


def date(ts) -> str:
    return datetime.fromtimestamp(ts or 0, tz=timezone.utc).strftime("%Y-%m-%d")


def header(p) -> str:
    cov = f" · {round((p['coverage'] or 0) * 100)}% of comments captured" if not p["meta_only"] else " · not fetched yet"
    return (f"# [p:{p['id']}] {p['title']}\n"
            f"r/{p['subreddit']} · {p['num_comments']} comments · score {p['score']} · {date(p['created_utc'])}"
            f"{cov}\n{p['permalink']}")


def ordered_comments(store: Store, post_id: str) -> list:
    """Depth-first order with siblings sorted by score (the way you'd read the best of a thread)."""
    rows = store.comments_for(post_id)
    kids = defaultdict(list)
    ids = {r["id"] for r in rows}
    for r in rows:
        parent = strip_prefix(r["parent_id"]) if (r["parent_id"] or "").startswith("t1_") else None
        kids[parent if parent in ids else None].append(r)
    for v in kids.values():
        v.sort(key=lambda r: -(r["score"] or 0))
    out = []

    def walk(parent):
        for r in kids.get(parent, []):
            out.append(r)
            walk(r["id"])

    walk(None)
    return out


def line(r, body_chars: int | None = None) -> str:
    body = r["body"] if body_chars is None else clip(r["body"], body_chars)
    body = body.replace("\n\n", "\n").replace("\n", "\n" + "  " * r["depth"] + "  ")
    op = "|OP" if r["is_submitter"] else ""
    return f"{'  ' * r['depth']}[c:{r['id']}|{r['score']:+d}|L{r['depth']}{op}] {body}"


def thread_text(store: Store, post_id: str, mode: str = "top", max_chars: int = 12000, offset: int = 0,
                min_score: int | None = None) -> str:
    p = store.post(post_id)
    if p is None:
        return f"Thread {post_id} isn't stored yet. Fetch it first (fetch_thread)."
    parts = [header(p)]
    if offset == 0 and p["selftext"]:
        parts.append(clip(p["selftext"], 3000) if mode != "all" else p["selftext"])
    parts.append("---")
    rows = [r for r in ordered_comments(store, post_id) if r["body"] not in DEAD]
    if min_score is not None:
        rows = [r for r in rows if (r["score"] or 0) >= min_score]
    if mode == "outline":
        rows = [r for r in rows if r["depth"] == 0]
        render = lambda r: line(r, 220)  # noqa: E731
    elif mode == "top":
        rows = [r for r in rows if r["depth"] <= 2]
        render = lambda r: line(r, 1200)  # noqa: E731
    else:
        render = line
    used = sum(len(x) for x in parts)
    shown = 0
    for r in rows[offset:]:
        text = render(r)
        if used + len(text) > max_chars and shown:
            break
        parts.append(text)
        used += len(text) + 1
        shown += 1
    end = offset + shown
    if end < len(rows):
        parts.append(f"--- showing comments {offset + 1}-{end} of {len(rows)} ({mode} view). "
                     f"Next page: offset={end}")
    else:
        parts.append(f"--- end of thread ({len(rows)} comments in {mode} view)")
    return "\n".join(parts)
