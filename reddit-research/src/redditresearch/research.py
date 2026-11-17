"""The research engine: studies, discovery, and the best-first crawl that builds the thread web."""

from __future__ import annotations

import logging
import math
import time

from .fetcher import fetch_full_thread, parse_post_id
from .sources.base import Source, SourceError
from .store import Store
from .util import tokens

log = logging.getLogger(__name__)


def relevance(terms: set[str], title: str, body: str) -> float:
    """How on-topic a post looks for the study's brief and keywords (0-1). Title hits count double."""
    if not terms:
        return 0.5
    t = set(tokens(title))
    b = set(tokens((body or "")[:4000])) - t
    denom = 2 * min(len(terms), 5)
    return min(1.0, (2 * len(terms & t) + len(terms & b)) / denom)


def engagement(num_comments: int) -> float:
    return min(1.0, math.log1p(max(num_comments or 0, 0)) / math.log1p(300))


def priority(rel: float, num_comments: int, hop: int) -> float:
    return round((0.65 * rel + 0.35 * engagement(num_comments)) * (0.85 ** hop), 4)


class Researcher:
    def __init__(self, store: Store, source: Source):
        self.store = store
        self.source = source

    def study_terms(self, study_id: int) -> set[str]:
        s = self.store.study(study_id)
        return set(tokens(s["brief"])) | set(tokens(" ".join(s["keywords"])))

    # ------------------------------------------------------------------ studies
    def create_study(self, name: str, brief: str, keywords: list[str] | None = None) -> int:
        return self.store.create_study(name, brief, keywords or [])

    # ------------------------------------------------------------------ discovery
    async def discover(self, study: str, queries: list[str], subreddits: list[str] | None = None,
                       time_range: str = "all", limit_per_query: int = 50, sort: str = "relevance",
                       max_seconds: float = 300) -> dict:
        sid = self.store.study_id(study)
        started = time.monotonic()
        terms = self.study_terms(sid)
        subs = [s.strip().removeprefix("r/") for s in (subreddits or []) if s.strip()]
        added, seen, errors = 0, 0, []
        jobs = [(q, s) for q in queries for s in (subs or [None])]
        if not queries and subs:
            jobs = [(None, s) for s in subs]
        skipped = []
        for query, sub in jobs:
            if time.monotonic() - started > max_seconds:
                skipped.append(f"{query or 'top'} in r/{sub or 'all'}")
                continue
            try:
                if query:
                    results = await self.source.search(query, subreddit=sub, sort=sort, time_range=time_range,
                                                       limit=limit_per_query)
                else:
                    results = await self.source.listing(sub, sort="top", time_range=time_range, limit=limit_per_query)
            except SourceError as exc:
                errors.append(f"{query or 'top'} in r/{sub or 'all'}: {exc}")
                continue
            for raw in results:
                pid = self.store.upsert_post_meta(raw, self.source.name)
                if not pid:
                    continue
                seen += 1
                rel = max(relevance(terms, raw.get("title", ""), raw.get("selftext", "")), 0.35 if query else 0.2)
                if self.store.add_candidate(sid, pid, rel, priority(rel, raw.get("num_comments", 0), 0), 0,
                                            f"search:{query}" if query else f"top:r/{sub}", query):
                    added += 1
        self.store.db.commit()
        top = self.store.q(
            "SELECT p.id, p.title, p.subreddit, p.num_comments, sp.priority FROM study_posts sp JOIN posts p "
            "ON p.id=sp.post_id WHERE sp.study_id=? AND sp.status='candidate' ORDER BY sp.priority DESC LIMIT 15",
            (sid,),
        )
        return {"results_seen": seen, "new_candidates": added, "errors": errors,
                "not_run_time_limit": skipped,
                "top_candidates": [dict(r) for r in top], "notes": getattr(self.source, "notes", [])}

    # ------------------------------------------------------------------ crawl
    async def crawl(self, study: str, max_threads: int = 25, max_hops: int = 2, min_relevance: float = 0.2,
                    per_subreddit_cap: int | None = None, max_seconds: float = 240,
                    follow_same_link: bool = True) -> dict:
        sid = self.store.study_id(study)
        terms = self.study_terms(sid)
        started = time.monotonic()
        fetched, failed = [], []
        while len(fetched) < max_threads and time.monotonic() - started < max_seconds:
            cand = self._next_candidate(sid, min_relevance, per_subreddit_cap)
            if cand is None:
                break
            pid, hop = cand["post_id"], cand["hop"]
            try:
                post, comments, stats = await fetch_full_thread(self.source, pid)
            except (SourceError, KeyError, IndexError, TypeError) as exc:
                self._set_status(sid, pid, "failed")
                failed.append({"id": pid, "error": str(exc)[:200]})
                continue
            saved = self.store.save_thread(post, comments, self.source.name)
            self._set_status(sid, pid, "fetched")
            saved["hop"] = hop
            saved["unexpanded_stubs"] = stats["unexpanded_stubs"]
            fetched.append(saved)
            log.info("[%d/%d] %s: %d comments (%d%%), hop %d: %s", len(fetched), max_threads, pid,
                     saved["comments"], round(saved["coverage"] * 100), hop, saved["title"][:70])
            if hop < max_hops:
                await self._expand(sid, pid, hop, terms, follow_same_link)
        remaining = self.store.one(
            "SELECT COUNT(*) FROM study_posts WHERE study_id=? AND status='candidate' AND relevance>=?",
            (sid, min_relevance),
        )[0]
        return {
            "fetched": fetched, "failed": failed, "candidates_remaining": remaining,
            "stopped_because": "budget" if len(fetched) >= max_threads else
                               ("time limit, call again to continue" if remaining else "no more candidates"),
            "notes": getattr(self.source, "notes", []),
        }

    def _next_candidate(self, sid: int, min_relevance: float, cap: int | None):
        rows = self.store.q(
            "SELECT sp.post_id, sp.hop, p.subreddit FROM study_posts sp JOIN posts p ON p.id=sp.post_id "
            "WHERE sp.study_id=? AND sp.status='candidate' AND sp.relevance>=? ORDER BY sp.priority DESC LIMIT 200",
            (sid, min_relevance),
        )
        if not cap:
            return rows[0] if rows else None
        counts = {r["subreddit"]: r["n"] for r in self.store.q(
            "SELECT p.subreddit, COUNT(*) n FROM study_posts sp JOIN posts p ON p.id=sp.post_id "
            "WHERE sp.study_id=? AND sp.status='fetched' GROUP BY p.subreddit", (sid,))}
        for r in rows:
            if counts.get(r["subreddit"], 0) < cap:
                return r
            self._set_status(sid, r["post_id"], "skipped_cap")
        return None

    def _set_status(self, sid: int, pid: str, status: str) -> None:
        self.store.db.execute("UPDATE study_posts SET status=? WHERE study_id=? AND post_id=?", (status, sid, pid))
        self.store.db.commit()

    async def _expand(self, sid: int, pid: str, hop: int, terms: set[str], follow_same_link: bool) -> None:
        """Queue threads this one connects to: links in its comments, crossposts, same-link submissions."""
        targets: dict[str, str] = {}
        for r in self.store.q("SELECT DISTINCT target_post_id FROM links WHERE post_id=? AND kind='reddit_thread' "
                              "AND target_post_id IS NOT NULL", (pid,)):
            targets[r["target_post_id"]] = f"link_from:{pid}"
        post = self.store.post(pid)
        if post["crosspost_parent"]:
            targets[post["crosspost_parent"]] = f"crosspost_of:{pid}"
        raws: list[dict] = []
        if follow_same_link and post["url"] and post["domain"] and "reddit" not in post["domain"]:
            for fn in (self.source.posts_with_url, ):
                try:
                    raws += await fn(post["url"])
                except (SourceError, NotImplementedError):
                    pass
        if post["num_crossposts"]:  # only ask when Reddit says crossposts exist (saves a slow search)
            try:
                raws += await self.source.crossposts(pid)
            except (SourceError, NotImplementedError):
                pass
        for raw in raws:
            rid = self.store.upsert_post_meta(raw, self.source.name)
            if rid and rid != pid:
                targets.setdefault(rid, f"same_link_as:{pid}")
        missing = [t for t in targets if self.store.post(t) is None]
        if missing:
            try:
                for raw in await self.source.info(missing):
                    self.store.upsert_post_meta(raw, self.source.name)
            except (SourceError, NotImplementedError):
                pass
        for tid, via in targets.items():
            meta = self.store.post(tid)
            if meta is None:
                continue
            rel = relevance(terms, meta["title"], meta["selftext"])
            # A thread people explicitly point to deserves a look even if its title is off-keyword.
            if via.startswith("link_from"):
                rel = max(rel, 0.25)
            self.store.add_candidate(sid, tid, rel, priority(rel, meta["num_comments"], hop + 1), hop + 1, via)
        self.store.db.commit()

    # ------------------------------------------------------------------ single thread
    async def fetch(self, url_or_id: str, study: str | None = None) -> dict:
        pid = parse_post_id(url_or_id)
        post, comments, stats = await fetch_full_thread(self.source, pid)
        saved = self.store.save_thread(post, comments, self.source.name)
        if study:
            sid = self.store.study_id(study)
            self.store.add_candidate(sid, pid, 1.0, 1.0, 0, "manual")
            self._set_status(sid, pid, "fetched")
        return saved | {"unexpanded_stubs": stats["unexpanded_stubs"], "requests": stats["requests"]}
