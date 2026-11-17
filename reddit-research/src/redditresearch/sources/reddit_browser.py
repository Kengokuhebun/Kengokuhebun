"""Reddit itself, read through a real browser profile on YOUR computer.

Why a browser: since May 2026 Reddit refuses logged-out `.json` requests from scripts, and new API apps
need weeks of manual approval. A real Chrome/Edge profile that you've logged into once is treated like you
browsing: it's the same technique the redditcommentscraper.com extension uses (it calls reddit.com
`.json` endpoints from inside your browser).

How it stays a *normal* browser: we start your installed Chrome (or Edge) ourselves, with a private
profile folder and no automation flags, then attach to it over Chrome's DevTools port only to run fetch()
inside a reddit.com tab. Automation-launched browsers (Playwright/Selenium defaults) get captcha'd by
Reddit's login page, so `rr login` doesn't automate anything at all: you log in by hand and close the window.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
import subprocess
import sys
import time
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


def find_browser(preferred: str = "") -> str | None:
    """Path to an installed Chromium-family browser: Chrome first, then Edge (on every Windows PC), Chromium."""
    if preferred and Path(preferred).exists():
        return preferred
    env = os.environ.get
    candidates = []
    if sys.platform.startswith("win"):
        for base in (env("ProgramFiles"), env("ProgramFiles(x86)"), env("LOCALAPPDATA")):
            if base:
                candidates += [Path(base) / "Google/Chrome/Application/chrome.exe",
                               Path(base) / "Microsoft/Edge/Application/msedge.exe",
                               Path(base) / "BraveSoftware/Brave-Browser/Application/brave.exe"]
    elif sys.platform == "darwin":
        candidates += [Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                       Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
                       Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
                       Path("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser")]
    for c in candidates:
        if c.exists():
            return str(c)
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"):
        found = shutil.which(name)
        if found:
            return found
    return None


async def _playwright_chromium() -> str | None:
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as pw:
            path = pw.chromium.executable_path
        return path if path and Path(path).exists() else None
    except Exception:  # noqa: BLE001
        return None


class RedditBrowserSource(Source):
    name = "reddit"

    def __init__(self, profile_dir: Path, headless: bool = True, browser_path: str = "", min_interval: float = 1.5,
                 origin: str = ORIGIN):
        self.profile_dir = Path(profile_dir)
        self.headless = headless
        self.browser_path = browser_path
        self.origin = origin
        self.limiter = RateLimiter(min_interval)
        self._pw = self._browser = self._ctx = self._page = None
        self._proc: subprocess.Popen | None = None
        self._start_lock = asyncio.Lock()

    # ------------------------------------------------------------------ browser lifecycle
    async def _exe(self) -> str:
        exe = find_browser(self.browser_path) or await _playwright_chromium()
        if not exe:
            raise SourceError("No Chrome, Edge or Chromium found. Install Google Chrome, or run `rr setup-browser`.")
        return exe

    def _spawn(self, exe: str, extra: list[str]) -> subprocess.Popen:
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        args = [exe, f"--user-data-dir={self.profile_dir}", "--no-first-run", "--no-default-browser-check",
                *os.environ.get("RR_BROWSER_ARGS", "").split(), *extra]  # RR_BROWSER_ARGS: for containers/CI only
        flags = subprocess.CREATE_NO_WINDOW if sys.platform.startswith("win") else 0
        return subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)

    async def start(self) -> None:
        async with self._start_lock:
            if self._page is not None:
                return
            try:
                await self._open()
            except SourceError:
                await self.close()
                raise
            except Exception as exc:
                await self.close()
                raise SourceError(f"Couldn't start the browser ({exc}). Run `rr doctor` to check the setup.") from exc

    async def _open(self) -> None:
        from playwright.async_api import async_playwright

        exe = await self._exe()
        port_file = self.profile_dir / "DevToolsActivePort"
        port_file.unlink(missing_ok=True)
        extra = ["--remote-debugging-port=0", "about:blank"]
        if self.headless:
            # Headless Chrome reports navigator.webdriver=true; this switch restores the normal value.
            extra = ["--headless=new", "--window-size=1280,900", "--disable-blink-features=AutomationControlled", *extra]
        self._proc = self._spawn(exe, extra)
        deadline = time.monotonic() + 30
        port = None
        while time.monotonic() < deadline:
            if self._proc.poll() is not None:
                raise SourceError(
                    "The browser closed immediately. Is a reddit-research browser window still open? Close it "
                    "and try again."
                )
            try:
                port = int(port_file.read_text().splitlines()[0])
                break
            except (FileNotFoundError, ValueError, IndexError):
                await asyncio.sleep(0.25)
        if not port:
            raise SourceError("The browser didn't start in time.")
        self._pw = await async_playwright().start()
        self._browser = await self._pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        self._ctx = self._browser.contexts[0] if self._browser.contexts else await self._browser.new_context()
        page = self._ctx.pages[0] if self._ctx.pages else await self._ctx.new_page()
        ua = await page.evaluate("navigator.userAgent")
        if "HeadlessChrome" in ua:  # headless announces itself in the user agent; present as normal Chrome
            cdp = await self._ctx.new_cdp_session(page)
            await cdp.send("Network.setUserAgentOverride", {"userAgent": ua.replace("HeadlessChrome", "Chrome")})
        await page.goto(self.origin + "/", wait_until="domcontentloaded", timeout=60_000)
        self._page = page

    async def close(self) -> None:
        if self._browser is not None:
            try:  # graceful close so Chrome writes cookies to disk
                cdp = await self._browser.new_browser_cdp_session()
                await cdp.send("Browser.close")
            except Exception:  # noqa: BLE001
                pass
        if self._pw is not None:
            try:
                await self._pw.stop()
            except Exception:  # noqa: BLE001
                pass
        if self._proc is not None:
            try:
                await asyncio.to_thread(self._proc.wait, 10)
            except subprocess.TimeoutExpired:
                self._proc.terminate()
        self._pw = self._browser = self._ctx = self._page = self._proc = None

    async def logged_in(self) -> bool:
        await self.start()
        cookies = await self._ctx.cookies(self.origin)
        return any(c["name"] == "reddit_session" for c in cookies)

    async def login(self, timeout_s: int = 900) -> bool:
        """Open a normal browser window on Reddit's login page. You log in, then close the window."""
        await self.close()
        exe = await self._exe()
        proc = self._spawn(exe, [self.origin + "/login/"])
        try:
            await asyncio.to_thread(proc.wait, timeout_s)
        except subprocess.TimeoutExpired:
            proc.terminate()
        self.headless = True
        try:
            return await self.logged_in()
        finally:
            await self.close()

    # ------------------------------------------------------------------ requests
    async def get_json(self, path: str, params: dict | None = None, attempts: int = 4):
        await self.start()
        query = {"raw_json": 1, **(params or {})}
        url = f"{self.origin}{path}?{urlencode(query, doseq=True, quote_via=quote)}"
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
