"""Quote-verified insights. Claude reads threads, then saves what it found here.

Nothing is stored unless its quote really appears (word for word) in the cited comment or post.
That enforces "verbatim-sourced language only" mechanically, not on trust.
"""

from __future__ import annotations

import time

from .store import Store
from .util import clip, quote_in_text

KINDS = {
    "pain": "a problem, frustration or fear in their own words",
    "desire": "an outcome they want (map to a sub-desire in the label)",
    "failed_solution": "something they tried that didn't work; label = the product/approach",
    "objection": "a reason they hesitate or don't buy",
    "belief": "something they believe (true or not) that shapes buying, e.g. 'it'll grow back'",
    "trigger": "the moment/situation that made them act or post (shower drain, 2AM, photo)",
    "brand": "a brand/product mention; put sentiment in the note (positive/negative/mixed)",
    "price": "price, value or willingness-to-pay statements",
    "buying_intent": "asking where to buy / what to buy / ready to purchase",
    "question": "a question they ask (FAQ and content ideas)",
    "identity": "how they describe themselves ('as a first-time mom...')",
    "language": "a vivid phrase worth using verbatim in copy",
    "angle": "a possible marketing angle this suggests (quote is the evidence)",
    "other": "anything else worth keeping",
}


def save(store: Store, study_id: int, items: list[dict], analyzed_thread_ids: list[str] | None = None) -> dict:
    accepted, rejected = 0, []
    for i, item in enumerate(items or []):
        kind = (item.get("kind") or "").strip().lower()
        label = (item.get("label") or "").strip()
        quote = (item.get("quote") or "").strip()
        sid = (item.get("source_id") or "").strip()
        if kind not in KINDS:
            rejected.append({"index": i, "reason": f"unknown kind {kind!r}; use one of {sorted(KINDS)}"})
            continue
        if not label or not quote or not sid:
            rejected.append({"index": i, "reason": "kind, label, quote and source_id are all required"})
            continue
        src = _resolve(store, sid)
        if src is None:
            rejected.append({"index": i, "reason": f"source {sid!r} not found (use the c:<id> / p:<id> tags shown)"})
            continue
        if not quote_in_text(quote, src["text"]):
            rejected.append({"index": i, "reason": "quote not found verbatim in that source; copy it exactly "
                                                   "(use ... to skip words)", "quote": clip(quote, 80)})
            continue
        cur = store.db.execute(
            "INSERT OR IGNORE INTO insights(study_id,kind,label,quote,source_id,post_id,author,score,permalink,note,"
            "created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (study_id, kind, label.lower(), quote, src["source_id"], src["post_id"], src["author"], src["score"],
             src["permalink"], item.get("note"), int(time.time())),
        )
        accepted += cur.rowcount
    for pid in analyzed_thread_ids or []:
        store.db.execute("UPDATE study_posts SET analyzed=1 WHERE study_id=? AND post_id=?",
                         (study_id, pid.removeprefix("p:")))
    store.db.commit()
    left = store.one("SELECT COUNT(*) FROM study_posts WHERE study_id=? AND status='fetched' AND analyzed=0",
                     (study_id,))[0]
    return {"saved": accepted, "rejected": rejected, "threads_left_to_analyze": left}


def _resolve(store: Store, source_id: str):
    sid = source_id.strip()
    kind, _, raw = sid.partition(":") if ":" in sid else ("", "", sid)
    raw = raw or sid
    if kind in ("", "c"):
        c = store.one("SELECT * FROM comments WHERE id=?", (raw,))
        if c:
            return {"source_id": f"c:{c['id']}", "post_id": c["post_id"], "text": c["body"], "author": c["author"],
                    "score": c["score"], "permalink": c["permalink"]}
    if kind in ("", "p"):
        p = store.one("SELECT * FROM posts WHERE id=?", (raw,))
        if p:
            return {"source_id": f"p:{p['id']}", "post_id": p["id"], "text": f"{p['title']}\n{p['selftext'] or ''}",
                    "author": p["author"], "score": p["score"], "permalink": p["permalink"]}
    return None


def next_threads(store: Store, study_id: int, count: int = 5) -> list[dict]:
    rows = store.q(
        "SELECT p.id, p.title, p.subreddit, p.fetched_comments, sp.priority, COALESCE(g.pagerank,0) pr "
        "FROM study_posts sp JOIN posts p ON p.id=sp.post_id LEFT JOIN graph_nodes g "
        "ON g.study_id=sp.study_id AND g.post_id=sp.post_id "
        "WHERE sp.study_id=? AND sp.status='fetched' AND sp.analyzed=0 "
        "ORDER BY sp.priority + 5*COALESCE(g.pagerank,0) DESC LIMIT ?",
        (study_id, count),
    )
    return [dict(r) for r in rows]


def report(store: Store, study_id: int, kind: str | None = None, min_support: int = 1, limit: int = 25,
           quotes_per_label: int = 3) -> list[dict]:
    """Group insights by kind+label. Support = distinct people who said it (repeats by one person count once)."""
    params: list = [study_id]
    where = "study_id=?"
    if kind:
        where += " AND kind=?"
        params.append(kind)
    groups = store.q(
        f"SELECT kind, label, COUNT(DISTINCT author) support, COUNT(*) mentions, COUNT(DISTINCT post_id) threads, "
        f"SUM(MAX(score,0)) upvotes FROM insights WHERE {where} GROUP BY kind, label HAVING support>=? "
        f"ORDER BY support DESC, upvotes DESC LIMIT ?",
        (*params, min_support, limit),
    )
    out = []
    for g in groups:
        quotes = store.q(
            "SELECT quote, score, permalink, note FROM insights WHERE study_id=? AND kind=? AND label=? "
            "ORDER BY score DESC LIMIT ?", (study_id, g["kind"], g["label"], quotes_per_label))
        out.append(dict(g) | {"quotes": [dict(q) for q in quotes]})
    return out
