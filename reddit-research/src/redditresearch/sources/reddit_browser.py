"""Reddit itself, read through a real browser profile on YOUR computer.

Why a browser: since May 2026 Reddit refuses logged-out `.json` requests from scripts, and new API apps
need weeks of manual approval. A real Chrome profile that you've logged into once is treated like you
browsing: it's the same technique the redditcommentscraper.com extension uses (it calls reddit.com
`.json` endpoints from inside your browser). Requests run inside a reddit.com tab with your cookies,
spaced out politely (default 1.5 s apart).
"""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from urllib.parse import quote, urlencode

from ..util import RateLimiter
from .base import BlockedError, SourceError, Source

log = logging.getLogger(__name__)
ORIGIN = "https://www.reddit.com"

_FETCH_JS = """
async (url) => {
  const r = await fetch(url, {credentials: 'include', headers: {'Accept': 'application/json'}});
  return {status: r.status, reset: r.headers.get('x-ratelimit-reset'),
          remaining: r.headers.get('x-ratelimit-remaining'), body: await r.text()};
}
"""


class RedditBrowserSource(Source):
    name = "reddit"

    def __init__(self, profile_dir: Path, headless: bool = True, channel: str = "chrome", min_interval: float = 1.5):
        self.profile_dir = Path(profile_dir)
        self.headless = headless
        self.channel = channel
        self.limiter = RateLimiter(min_interval)
        self._pw = self._ctx = self._page = None
        self._start_lock = asyncio.Lock()

    # ------------------------------------------------------------------ browser lifecycle
    async def _launch(self, headless: bool, user_agent: str | None = None):
        from playwright.async_api import async_playwright

        if self._pw is None:
            self._pw = await async_playwright().start()
        kwargs = dict(headless=headless, viewport={"width": 1280, "height": 900},
                      args=["--disable-blink-features=AutomationControlled"])
        if user_agent:
            kwargs["user_agent"] = user_agent
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        try:
            return await self._pw.chromium.launch_persistent_context(str(self.profile_dir), channel=self.channel, **kwargs)
        except Exception as exc:  # Chrome not installed -> Playwright's bundled Chromium
            log.info("Couldn't launch %s (%s); using bundled Chromium", self.channel, exc)
            return await self._pw.chromium.launch_persistent_context(str(self.profile_dir), **kwargs)

    async def start(self) -> None:
        async with self._start_lock:
            if self._page is not None:
                return
            try:
                await self._open()
            except SourceError:
                raise
            except Exception as exc:
                await self.close()
                raise SourceError(
                    f"Couldn't start the browser ({exc}). Run `rr doctor` to check the setup."
                ) from exc

    async def _open(self) -> None:
        self._ctx = await self._launch(self.headless)
        page = self._ctx.pages[0] if self._ctx.pages else await self._ctx.new_page()
        ua = await page.evaluate("navigator.userAgent")
        if "HeadlessChrome" in ua:  # headless announces itself; present as normal Chrome instead
            await self._ctx.close()
            self._ctx = await self._launch(self.headless, ua.replace("HeadlessChrome", "Chrome"))
            page = self._ctx.pages[0] if self._ctx.pages else await self._ctx.new_page()
        await page.goto(ORIGIN + "/", wait_until="domcontentloaded", timeout=60_000)
        self._page = page

    async def close(self) -> None:
        if self._ctx is not None:
            await self._ctx.close()
        if self._pw is not None:
            await self._pw.stop()
        self._pw = self._ctx = self._page = None

    async def logged_in(self) -> bool:
        await self.start()
        cookies = await self._ctx.cookies(ORIGIN)
        return any(c["name"] == "reddit_session" for c in cookies)

    async def login(self, timeout_s: int = 600) -> bool:
        """Open a visible window on the Reddit login page and wait until you've signed in."""
        await self.close()
        self.headless = False
        self._ctx = await self._launch(headless=False)
        page = self._ctx.pages[0] if self._ctx.pages else await self._ctx.new_page()
        await page.goto(ORIGIN + "/login/", wait_until="domcontentloaded", timeout=60_000)
        for _ in range(timeout_s // 2):
            cookies = await self._ctx.cookies(ORIGIN)
            if any(c["name"] == "reddit_session" for c in cookies):
                await asyncio.sleep(2)  # let the session settle
                await self.close()
                return True
            await asyncio.sleep(2)
        await self.close()
        return False

    # ------------------------------------------------------------------ requests
    async def get_json(self, path: str, params: dict | None = None, attempts: int = 4):
        await self.start()
        query = {"raw_json": 1, **(params or {})}
        url = f"{ORIGIN}{path}?{urlencode(query, doseq=True, quote_via=quote)}"
        last = ""
        for attempt in range(1, attempts + 1):
            await self.limiter.wait()
            try:
                res = await self._page.evaluate(_FETCH_JS, url)
            except Exception as exc:  # page crashed / navigated: reopen once
                last = f"browser error: {exc}"
                self._page = None
                await self.close()
                await self.start()
                continue
            status = res["status"]
            if status == 200:
                try:
                    return json.loads(res["body"])
                except json.JSONDecodeError:
                    last = "non-JSON response (Reddit served a page instead of data)"
                    await asyncio.sleep(3 * attempt)
                    continue
            last = f"HTTP {status}"
            if status == 429:
                await asyncio.sleep(min(float(res.get("reset") or 30 * attempt), 120))
            elif status in (500, 502, 503, 504):
                await asyncio.sleep(2 * attempt)
            elif status in (401, 403):
                raise BlockedError(
                    f"Reddit refused the request ({status}). Run `rr login` once to sign this tool's browser "
                    "profile into Reddit, then try again."
                )
            elif status == 404:
                raise SourceError(f"Not found on Reddit: {path}")
            else:
                break
        raise SourceError(f"Reddit request failed: {path}: {last}")

    async def thread(self, post_id: str) -> tuple[dict, list]:
        data = await self.get_json(f"/comments/{post_id}.json", {"limit": 500, "sort": "top"})
        post = data[0]["data"]["children"][0]["data"]
        return post, data[1]["data"]["children"]

    async def more_children(self, post_id: str, ids: list[str]) -> list:
        out = []
        for i in range(0, len(ids), 100):
            data = await self.get_json("/api/morechildren.json", {
                "api_type": "json", "link_id": f"t3_{post_id}", "children": ",".join(ids[i : i + 100]),
                "limit_children": "false", "sort": "top"})
            out += ((data or {}).get("json", {}).get("data", {}).get("things")) or []
        return out

    async def subtree(self, post_id: str, comment_id: str) -> list:
        data = await self.get_json(f"/comments/{post_id}/_/{comment_id}.json", {"limit": 500, "sort": "top"})
        return data[1]["data"]["children"]

    async def _paged(self, path: str, params: dict, limit: int) -> list[dict]:
        out, after = [], None
        while len(out) < limit:
            p = {**params, "limit": min(100, limit - len(out))}
            if after:
                p["after"] = after
            data = await self.get_json(path, p)
            listing = data["data"] if isinstance(data, dict) else data[-1]["data"]
            out += [c["data"] for c in listing.get("children", []) if c.get("kind") == "t3"]
            after = listing.get("after")
            if not after or not listing.get("children"):
                break
        return out[:limit]

    async def search(self, query: str, subreddit: str | None = None, sort: str = "relevance",
                     time_range: str = "all", limit: int = 100) -> list[dict]:
        params = {"q": query, "sort": sort, "t": time_range, "type": "link"}
        if subreddit:
            params["restrict_sr"] = "on"
            return await self._paged(f"/r/{subreddit}/search.json", params, limit)
        return await self._paged("/search.json", params, limit)

    async def listing(self, subreddit: str, sort: str = "top", time_range: str = "year", limit: int = 100) -> list[dict]:
        sort = "top" if sort == "comments" else sort
        return await self._paged(f"/r/{subreddit}/{sort}.json", {"t": time_range}, limit)

    async def info(self, post_ids: list[str]) -> list[dict]:
        out = []
        for i in range(0, len(post_ids), 100):
            data = await self.get_json("/api/info.json", {"id": ",".join(f"t3_{p}" for p in post_ids[i : i + 100])})
            out += [c["data"] for c in data["data"]["children"]]
        return out

    async def posts_with_url(self, url: str) -> list[dict]:
        data = await self.get_json("/api/info.json", {"url": url, "limit": 100})
        return [c["data"] for c in data["data"]["children"] if c.get("kind") == "t3"]

    async def crossposts(self, post_id: str) -> list[dict]:
        data = await self.get_json(f"/duplicates/{post_id}.json", {"limit": 100})
        return [c["data"] for c in data[1]["data"]["children"]] if isinstance(data, list) and len(data) > 1 else []

    async def find_subreddits(self, query: str, limit: int = 15) -> list[dict]:
        data = await self.get_json("/subreddits/search.json", {"q": query, "limit": limit})
        return [{"name": c["data"].get("display_name"), "subscribers": c["data"].get("subscribers"),
                 "description": c["data"].get("public_description") or ""} for c in data["data"]["children"]]
