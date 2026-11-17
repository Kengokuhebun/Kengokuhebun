"""Exports: per-thread files matching the reference scraper's columns, plus whole-study exports."""

from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx

from . import graph as graphlib
from . import insights as insightlib
from .render import ordered_comments
from .store import Store

FIELDS = ["type", "thread_id", "comment_id", "parent_id", "author", "score", "created_utc", "depth", "text", "permalink"]


def _iso(ts) -> str:
    return datetime.fromtimestamp(ts or 0, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def thread_rows(store: Store, post_id: str) -> list[dict]:
    p = store.post(post_id)
    rows = [{"type": "post", "thread_id": p["id"], "comment_id": "", "parent_id": "", "author": p["author"],
             "score": p["score"], "created_utc": _iso(p["created_utc"]), "depth": -1,
             "text": f"{p['title']}\n\n{p['selftext'] or ''}".strip(), "permalink": p["permalink"]}]
    for c in ordered_comments(store, post_id):
        rows.append({"type": "comment", "thread_id": p["id"], "comment_id": c["id"], "parent_id": c["parent_id"],
                     "author": c["author"], "score": c["score"], "created_utc": _iso(c["created_utc"]),
                     "depth": c["depth"], "text": c["body"], "permalink": c["permalink"]})
    return rows


def to_csv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def to_text(store: Store, post_id: str) -> str:
    """Plain text for pasting into any AI chat."""
    p = store.post(post_id)
    out = [f"{p['title']} (r/{p['subreddit']}, {p['num_comments']} comments)", p["selftext"] or "", ""]
    for c in ordered_comments(store, post_id):
        if c["body"] in ("[deleted]", "[removed]"):
            continue
        out.append(f"{'  ' * c['depth']}- ({c['score']}) {c['body']}")
    return "\n".join(out)


def export_thread(store: Store, post_id: str, fmt: str, folder: Path) -> Path:
    rows = thread_rows(store, post_id)
    path = folder / f"thread-{post_id}.{ 'txt' if fmt == 'text' else fmt}"
    if fmt == "csv":
        path.write_text(to_csv(rows), encoding="utf-8-sig", newline="")  # BOM so Excel reads emoji correctly
    elif fmt == "json":
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    elif fmt in ("text", "txt"):
        path.write_text(to_text(store, post_id), encoding="utf-8")
    else:
        raise ValueError("format must be csv, json or text")
    return path


def export_study(store: Store, study_id: int, fmt: str, folder: Path) -> Path:
    s = store.study(study_id)
    stem = folder / f"study-{s['name'].replace(' ', '_')}"
    ids = store.study_post_ids(study_id, "fetched")
    if fmt in ("csv", "json"):
        rows = [r for pid in ids for r in thread_rows(store, pid)]
        path = stem.with_suffix("." + fmt)
        if fmt == "csv":
            path.write_text(to_csv(rows), encoding="utf-8-sig", newline="")
        else:
            path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        return path
    if fmt == "html":
        path = stem.with_name(stem.name + "-web.html")
        path.write_text(graphlib.to_html(store, study_id, f"Thread web: {s['name']}"), encoding="utf-8")
        return path
    if fmt == "gexf":
        path = stem.with_suffix(".gexf")
        nx.write_gexf(graphlib.to_networkx(store, study_id), path)
        return path
    if fmt in ("md", "report"):
        path = stem.with_name(stem.name + "-insights.md")
        path.write_text(insights_markdown(store, study_id), encoding="utf-8")
        return path
    if fmt == "insights_csv":
        path = stem.with_name(stem.name + "-insights.csv")
        rows = [dict(r) for r in store.q(
            "SELECT kind,label,quote,note,author,score,permalink,post_id FROM insights WHERE study_id=? "
            "ORDER BY kind,label", (study_id,))]
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=["kind", "label", "quote", "note", "author", "score", "permalink", "post_id"])
        w.writeheader()
        w.writerows(rows)
        path.write_text(buf.getvalue(), encoding="utf-8-sig", newline="")
        return path
    raise ValueError("format must be csv, json, html, gexf, md or insights_csv")


def insights_markdown(store: Store, study_id: int) -> str:
    s = store.study(study_id)
    n_threads = len(store.study_post_ids(study_id, "fetched"))
    out = [f"# Research: {s['name']}", "", f"Brief: {s['brief']}", "",
           f"Threads analysed: {n_threads}. Every quote below was checked word-for-word against its source.", ""]
    for kind, desc in insightlib.KINDS.items():
        groups = insightlib.report(store, study_id, kind=kind, limit=40)
        if not groups:
            continue
        out += [f"## {kind.replace('_', ' ').title()}", f"_{desc}_", "",
                "| Label | People | Threads | Upvotes |", "|---|---|---|---|"]
        out += [f"| {g['label']} | {g['support']} | {g['threads']} | {g['upvotes'] or 0} |" for g in groups]
        out.append("")
        for g in groups[:12]:
            out.append(f"**{g['label']}**")
            for q in g["quotes"]:
                note = f" ({q['note']})" if q["note"] else ""
                out.append(f"> {q['quote']}{note}  \n> [source, {q['score']} upvotes]({q['permalink']})")
                out.append("")
    return "\n".join(out)
