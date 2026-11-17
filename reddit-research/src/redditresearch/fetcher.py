"""Fetch a complete thread: every 'load more' and 'continue this thread' stub expanded.

Ported from how the redditcommentscraper.com extension works (found with REA), minus its caps:
it stops after 40 'continue this thread' fetches and its paid tiers cap comments at 1,000.
"""

from __future__ import annotations

import logging
import re

from .sources.base import Source, SourceError
from .tree import assign_paths, flatten

log = logging.getLogger(__name__)
POST_ID_RE = re.compile(r"(?:comments/|redd\.it/|^)([a-z0-9]{4,10})(?:[/?#]|$)", re.IGNORECASE)


def parse_post_id(url_or_id: str) -> str:
    s = (url_or_id or "").strip()
    m = POST_ID_RE.search(s)
    if not m:
        raise ValueError(f"Can't find a Reddit post id in {url_or_id!r}. Use a link containing /comments/<id>/.")
    return m.group(1).lower().removeprefix("t3_")


async def fetch_full_thread(source: Source, post_id: str, max_requests: int = 400) -> tuple[dict, list[dict], dict]:
    """Returns (raw post, comment rows, stats)."""
    post, children = await source.thread(post_id)
    seen: set[str] = set()
    parsed = flatten(children, post_id, seen)
    requests = 1
    pending_more = list(dict.fromkeys(parsed.more_ids))
    pending_cont = list(dict.fromkeys(parsed.continue_parents))
    done_cont: set[str] = set()
    errors: list[str] = []

    while (pending_more or pending_cont) and requests < max_requests:
        if pending_more:
            batch, pending_more = pending_more[:100], pending_more[100:]
            batch = [i for i in batch if i not in seen]
            if not batch:
                continue
            try:
                things = await source.more_children(post_id, batch)
            except SourceError as exc:
                errors.append(str(exc))
                continue
            requests += 1
            new = flatten(things, post_id, seen)
        else:
            cid = pending_cont.pop(0)
            if cid in done_cont:
                continue
            done_cont.add(cid)
            try:
                kids = await source.subtree(post_id, cid)
            except SourceError as exc:
                errors.append(str(exc))
                continue
            requests += 1
            new = flatten(kids, post_id, seen)
        parsed.comments += new.comments
        pending_more += [i for i in dict.fromkeys(new.more_ids) if i not in seen]
        pending_cont += [c for c in dict.fromkeys(new.continue_parents) if c not in done_cont]

    assign_paths(parsed.comments, post_id)
    stats = {
        "requests": requests,
        "unexpanded_stubs": len(pending_more) + len(pending_cont),
        "errors": errors[:5],
    }
    return post, parsed.comments, stats
