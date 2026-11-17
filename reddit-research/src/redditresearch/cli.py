"""Command line: `rr <command>`. Run `rr --help` for the list."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys

from . import config
from . import graph as graphlib
from . import insights as insightlib
from .app import App
from .export import export_study, export_thread
from .fetcher import parse_post_id
from .render import thread_text


def _print(obj) -> None:
    print(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=1, default=str))


async def cmd_login(args) -> None:
    import shutil

    from .sources.reddit_browser import RedditBrowserSource, find_browser

    s = config.load_settings()
    if args.fresh and config.profile_dir().exists():
        shutil.rmtree(config.profile_dir(), ignore_errors=True)
        print("Cleared the old browser profile.")
    src = RedditBrowserSource(config.profile_dir(), headless=False, browser_path=s.get("browser_path", ""))
    print(f"Opening {find_browser(s.get('browser_path', '')) or 'a browser'} on Reddit's login page.")
    print("1. Log in normally (Google/Apple/email all work).")
    print("2. When you can see your Reddit home feed, CLOSE that browser window.")
    print("(It's a separate, private browser profile, so your normal Chrome is untouched.)")
    ok = await src.login(timeout_s=args.timeout)
    if ok:
        print(f"Logged in. Your session is stored only on this computer: {config.profile_dir()}")
        if s["source"] == "arctic":
            config.save_setting("source", "auto")
    else:
        print("Not logged in yet. Run `rr login` again, finish logging in, then close the window.")


async def cmd_doctor(args) -> None:
    from .sources.arctic import ArcticShiftSource

    print(f"Data folder: {config.home()}")
    print(f"Settings: {config.load_settings()}")
    try:
        import playwright  # noqa: F401
        print("Playwright: installed")
    except ImportError:
        print("Playwright: MISSING (pip install playwright)")
    arctic = ArcticShiftSource()
    try:
        subs = await arctic.find_subreddits("beyondthebump", 1)
        print(f"Arctic Shift archive: OK ({subs[0]['name'] if subs else 'reachable'})")
    except Exception as exc:  # noqa: BLE001 - diagnostic output
        print(f"Arctic Shift archive: FAILED ({exc})")
    finally:
        await arctic.close()
    if (config.profile_dir()).exists():
        from .sources.reddit_browser import RedditBrowserSource

        s = config.load_settings()
        from .sources.reddit_browser import find_browser

        print(f"Browser: {find_browser(s.get('browser_path', '')) or 'none found (run rr setup-browser)'}")
        src = RedditBrowserSource(config.profile_dir(), headless=True, browser_path=s.get("browser_path", ""))
        try:
            print(f"Reddit login: {'yes' if await src.logged_in() else 'NO (run rr login)'}")
            data = await src.get_json("/r/beyondthebump/top.json", {"t": "week", "limit": 1})
            print(f"Reddit via your browser: OK ({len(data['data']['children'])} post fetched)")
        except Exception as exc:  # noqa: BLE001
            print(f"Reddit via your browser: FAILED ({exc})")
        finally:
            await src.close()
    else:
        print("Reddit via your browser: not set up (run `rr login`). Arctic Shift will be used until then.")


async def run(args) -> None:
    if args.cmd == "login":
        return await cmd_login(args)
    if args.cmd == "doctor":
        return await cmd_doctor(args)
    if args.cmd == "setup-browser":
        import subprocess

        print("Downloading Playwright's Chromium (only needed if Google Chrome isn't installed)...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
        return None
    if args.cmd == "set":
        value = args.value
        if value.lower() in ("true", "false"):
            value = value.lower() == "true"
        else:
            try:
                value = float(value)
            except ValueError:
                pass
        return _print(config.save_setting(args.key, value))
    a = App()
    try:
        r = a.researcher
        if args.cmd == "fetch":
            res = await r.fetch(args.url, args.study)
            _print(res)
            if args.format:
                _print(f"Saved {export_thread(a.store, res['id'], args.format, config.export_dir())}")
        elif args.cmd == "study":
            sid = r.create_study(args.name, args.brief, args.keywords or [])
            _print(f"Study '{args.name}' ready (id {sid})")
        elif args.cmd == "subs":
            _print(await a.source.find_subreddits(args.query))
        elif args.cmd == "discover":
            _print(await r.discover(args.study, args.query or [], args.sub, args.time, args.limit, args.sort, 86400))
        elif args.cmd == "crawl":
            res = await r.crawl(args.study, args.max_threads, args.hops, args.min_relevance, args.per_sub,
                                args.max_seconds)
            _print(res)
        elif args.cmd == "read":
            _print(thread_text(a.store, parse_post_id(args.thread), args.mode, args.max_chars, args.offset))
        elif args.cmd == "search":
            sid = a.store.study_id(args.study) if args.study else None
            for row in a.store.search(args.query, args.kind, sid, args.limit):
                _print(f"{row['id']}  {row.get('snip')}")
        elif args.cmd == "graph":
            sid = a.store.study_id(args.study)
            _print(graphlib.build(a.store, sid))
            _print(graphlib.overview(a.store, sid))
            _print(f"Saved {export_study(a.store, sid, 'html', config.export_dir())}")
        elif args.cmd == "report":
            _print(insightlib.report(a.store, a.store.study_id(args.study), args.kind, args.min_support))
        elif args.cmd == "export":
            if args.thread:
                path = export_thread(a.store, parse_post_id(args.thread), args.format, config.export_dir())
            else:
                path = export_study(a.store, a.store.study_id(args.study), args.format, config.export_dir())
            _print(f"Saved {path}")
        elif args.cmd == "stats":
            _print(a.store.stats())
        notes = getattr(a._source, "notes", None) if a._source else None
        if notes:
            print("Notes: " + "; ".join(notes), file=sys.stderr)
    finally:
        await a.close()


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="rr", description="Free Reddit research engine for Claude.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("login", help="sign this tool's browser profile into Reddit (one time)")
    s.add_argument("--timeout", type=int, default=900)
    s.add_argument("--fresh", action="store_true", help="delete the tool's old browser profile first")
    sub.add_parser("doctor", help="check that everything works")
    sub.add_parser("setup-browser", help="download Chromium (only if no Chrome/Edge/Brave is installed)")
    s = sub.add_parser("set", help="change a setting, e.g. `rr set source arctic`")
    s.add_argument("key", choices=sorted(config.DEFAULTS))
    s.add_argument("value")
    sub.add_parser("serve", help="run the MCP server (Claude starts this for you)")
    sub.add_parser("stats", help="database totals")

    s = sub.add_parser("fetch", help="fetch one full thread")
    s.add_argument("url")
    s.add_argument("--study")
    s.add_argument("--format", choices=["csv", "json", "text"])

    s = sub.add_parser("study", help="create a study")
    s.add_argument("name")
    s.add_argument("--brief", required=True)
    s.add_argument("--keywords", nargs="*")

    s = sub.add_parser("subs", help="find subreddits")
    s.add_argument("query")

    s = sub.add_parser("discover", help="search for seed threads")
    s.add_argument("study")
    s.add_argument("-q", "--query", action="append")
    s.add_argument("-s", "--sub", action="append")
    s.add_argument("--time", default="all")
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("--sort", default="relevance")

    s = sub.add_parser("crawl", help="fetch candidates and follow links between threads")
    s.add_argument("study")
    s.add_argument("--max-threads", type=int, default=25)
    s.add_argument("--hops", type=int, default=2)
    s.add_argument("--min-relevance", type=float, default=0.2)
    s.add_argument("--per-sub", type=int)
    s.add_argument("--max-seconds", type=float, default=3600)

    s = sub.add_parser("read", help="print a stored thread")
    s.add_argument("thread")
    s.add_argument("--mode", default="top", choices=["outline", "top", "all"])
    s.add_argument("--max-chars", type=int, default=20000)
    s.add_argument("--offset", type=int, default=0)

    s = sub.add_parser("search", help="full-text search stored comments/posts")
    s.add_argument("query")
    s.add_argument("--study")
    s.add_argument("--kind", default="comments", choices=["comments", "posts"])
    s.add_argument("--limit", type=int, default=20)

    s = sub.add_parser("graph", help="build the thread web and save an interactive map")
    s.add_argument("study")

    s = sub.add_parser("report", help="aggregated insights")
    s.add_argument("study")
    s.add_argument("--kind")
    s.add_argument("--min-support", type=int, default=1)

    s = sub.add_parser("export", help="export a study or a thread")
    s.add_argument("study", nargs="?")
    s.add_argument("--thread")
    s.add_argument("--format", default="md")
    return p


def main(argv: list[str] | None = None) -> None:
    import logging

    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")  # emoji-safe on Windows consoles
    args = parser().parse_args(argv)
    if args.cmd == "serve":
        from .server import main as serve_main

        serve_main()
        return
    try:
        asyncio.run(run(args))
    except KeyboardInterrupt:
        print("\nStopped. Progress is saved; run the same command again to continue.")
    except (KeyError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
