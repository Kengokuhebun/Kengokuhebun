"""Arctic Shift (arctic-shift.photon-reddit.com): a free public Reddit archive. No login, works anywhere.

Limits worth knowing:
  * keyword search needs a subreddit (or author), and is sometimes overloaded -> we fall back to
    scanning the subreddit by date and filtering locally;
  * score / num_comments are 0-1 for posts younger than ~36 hours;
  * be gentle: it's a free community service.
"""

from __future__ import annotations

import asyncio
import logging
import time

import httpx

from ..util import RateLimiter, tokens
from .base import SourceError, Source

log = logging.getLogger(__name__)
BASE = "https://arctic-shift.photon-reddit.com/api"
TIME_RANGES = {"hour": 3600, "day": 86400, "week": 7 * 86400, "month": 31 * 86400, "year": 366 * 86400}


class ArcticShiftSource(Source):
    name = "arctic"

    def __init__(self, min_interval: float = 1.5, scan_pages: int = 15, client: httpx.AsyncClient | None = None):
        self.limiter = RateLimiter(min_interval)
        self.scan_pages = scan_pages
        self._client = client

    async def start(self) -> None:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(90.0), headers={"User-Agent": "reddit-research/0.1 (personal research tool)"}
            )

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _get(self, path: str, params: dict, attempts: int = 5):
        await self.start()
        last = ""
        for attempt in range(1, attempts + 1):
            await self.limiter.wait()
            try:
                r = await self._client.get(f"{BASE}/{path}", params=params)
            except httpx.HTTPError as exc:
                last = f"network error: {exc}"
                await asyncio.sleep(3 * attempt)
                continue
            if r.status_code == 200:
                body = r.json()
                if body.get("error"):
                    raise SourceError(f"Arctic Shift: {body['error']}")
                return body.get("data")
            text = r.text[:200]
            last = f"HTTP {r.status_code}: {text}"
            if r.status_code == 429:
                wait = float(r.headers.get("x-ratelimit-reset", 10 * attempt))
                await asyncio.sleep(min(max(wait, 2), 70))
            elif r.status_code == 422 and "timeout" in text.lower():
                # "Timeout. Maybe slow down a bit": overloaded query. Back off, then retry.
                await asyncio.sleep(min(6 * attempt, 30))
            elif r.status_code >= 500:
                await asyncio.sleep(4 * attempt)
            else:
                break
        raise SourceError(f"Arctic Shift {path} failed: {last}")

    # ------------------------------------------------------------------ threads
    async def thread(self, post_id: str) -> tuple[dict, list]:
        posts = await self._get("posts/ids", {"ids": post_id})
        if not posts:
            raise SourceError(f"Arctic Shift has no post {post_id}")
        children = await self._get(
            "comments/tree",
            {"link_id": f"t3_{post_id}", "limit": 25000, "start_breadth": 9999, "start_depth": 9999},
        )
        return posts[0], children or []

    async def more_children(self, post_id: str, ids: list[str]) -> list:
        out = []
        for i in range(0, len(ids), 100):
            batch = await self._get("comments/ids", {"ids": ",".join(ids[i : i + 100])}) or []
            out += [{"kind": "t1", "data": c} for c in batch]
        return out

    async def subtree(self, post_id: str, comment_id: str) -> list:
        data = await self._get(
            "comments/tree",
            {"link_id": f"t3_{post_id}", "parent_id": f"t1_{comment_id}", "limit": 25000,
             "start_breadth": 9999, "start_depth": 9999},
        )
        return data or []

    # ------------------------------------------------------------------ discovery
    async def search(self, query: str, subreddit: str | None = None, sort: str = "relevance",
                     time_range: str = "all", limit: int = 100) -> list[dict]:
        if not subreddit:
            raise SourceError(
                "Arctic Shift can only keyword-search inside a subreddit. Pass subreddits=[...] "
                "(use find_subreddits to pick some), or log in with `rr login` to use Reddit's own search."
            )
        params = {"subreddit": subreddit, "query": query, "limit": min(limit, 100), "sort": "desc"}
        after = _after(time_range)
        if after:
            params["after"] = after
        try:
            return await self._get("posts/search", params, attempts=2) or []
        except SourceError as exc:
            log.info("Arctic keyword search failed (%s); scanning r/%s by date instead", exc, subreddit)
            return await self._scan(subreddit, query, after, limit)

    async def _scan(self, subreddit: str, query: str, after: int | None, limit: int) -> list[dict]:
        """Page backwards through a subreddit and keep posts whose title/body contain every query word."""
        want = set(tokens(query))
        hits, before = [], None
        for _ in range(self.scan_pages):
            params = {"subreddit": subreddit, "limit": 100, "sort": "desc",
                      "fields": "id,title,selftext,num_comments,score,created_utc,author,subreddit,url,link_flair_text"}
            if before:
                params["before"] = before
            if after:
                params["after"] = after
            page = await self._get("posts/search", params) or []
            if not page:
                break
            for p in page:
                have = set(tokens(f"{p.get('title', '')} {p.get('selftext', '')}"))
                if want <= have:
                    hits.append(p)
            before = min(int(p["created_utc"]) for p in page)
            if len(hits) >= limit:
                break
        return hits[:limit]

    async def listing(self, subreddit: str, sort: str = "top", time_range: str = "year", limit: int = 100) -> list[dict]:
        after = _after(time_range)
        rows, before = [], None
        while len(rows) < max(limit, 100) * 3 and len(rows) < 1000:
            params = {"subreddit": subreddit, "limit": 100, "sort": "desc"}
            if after:
                params["after"] = after
            if before:
                params["before"] = before
            page = await self._get("posts/search", params) or []
            if not page:
                break
            rows += page
            before = min(int(p["created_utc"]) for p in page)
        if sort in ("top", "comments"):  # the archive can't sort by score, so do it here
            rows.sort(key=lambda p: (p.get("num_comments") or 0, p.get("score") or 0), reverse=True)
        return rows[:limit]

    async def info(self, post_ids: list[str]) -> list[dict]:
        out = []
        for i in range(0, len(post_ids), 100):
            out += await self._get("posts/ids", {"ids": ",".join(post_ids[i : i + 100])}) or []
        return out

    async def posts_with_url(self, url: str) -> list[dict]:
        return await self._get("posts/search", {"url": url, "url_exact": "true", "limit": 100}, attempts=2) or []

    async def crossposts(self, post_id: str) -> list[dict]:
        return await self._get("posts/search", {"crosspost_parent_id": f"t3_{post_id}", "limit": 100}, attempts=2) or []

    async def find_subreddits(self, query: str, limit: int = 15) -> list[dict]:
        prefix = query.strip().lower().replace(" ", "").removeprefix("r/")
        data = await self._get("subreddits/search", {"subreddit_prefix": prefix, "limit": limit}) or []
        return [{"name": d.get("display_name"), "subscribers": d.get("subscribers"),
                 "description": d.get("public_description") or d.get("title") or ""} for d in data]


def _after(time_range: str) -> int | None:
    seconds = TIME_RANGES.get(time_range)
    return int(time.time()) - seconds if seconds else None

