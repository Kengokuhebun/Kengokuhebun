"""MCP server: the tools Claude uses. Every tool returns compact text, paged, so a study of thousands of
threads never floods Claude's context."""

from __future__ import annotations

import json
import logging
import sys
from contextlib import asynccontextmanager

from mcp.server.mcpserver import MCPServer

from . import config
from . import graph as graphlib
from . import insights as insightlib
from .app import App
from .export import export_study, export_thread
from .fetcher import parse_post_id
from .render import thread_text
from .util import clip

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

INSTRUCTIONS = """Reddit research engine for ecommerce/market research. Data lives in a local database and
persists between sessions. Typical flow:
1. create_study (brief = product + avatar + what you want to learn), 2. find_subreddits, 3. discover_threads,
4. crawl_web (repeat until enough threads), 5. graph_overview to see the web of threads and groups,
6. loop: next_threads_to_analyze -> read_thread -> save_insights (quotes must be copied exactly),
7. insights_report / export_study. Use search_corpus to check how widespread a phrase or product is.
IDs: threads are p:<id>, comments are c:<id>. Never invent quotes: save_insights rejects anything that isn't verbatim."""

_app: App | None = None


def app() -> App:
    global _app
    if _app is None:
        _app = App()
    return _app


@asynccontextmanager
async def lifespan(_server):
    try:
        yield {}
    finally:
        if _app is not None:
            await _app.close()


mcp = MCPServer("reddit-research", instructions=INSTRUCTIONS, lifespan=lifespan)


def _j(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, default=str)


@mcp.tool()
async def status() -> str:
    """Database totals, which data source is active, and whether Reddit login is set up."""
    a = app()
    info = a.store.stats() | {"source_setting": a.settings["source"], "active_source": a.source.name,
                              "data_folder": str(config.home())}
    studies = [dict(r) for r in a.store.q(
        "SELECT s.name, s.brief, COUNT(sp.post_id) FILTER (WHERE sp.status='fetched') threads, "
        "COUNT(sp.post_id) FILTER (WHERE sp.status='candidate') candidates FROM studies s LEFT JOIN study_posts sp "
        "ON sp.study_id=s.id GROUP BY s.id ORDER BY s.id")]
    return _j(info | {"studies": studies})


@mcp.tool()
async def create_study(name: str, brief: str, keywords: list[str] | None = None) -> str:
    """Start (or update) a research study. `brief`: the product, the avatar and what you want to learn,
    in plain words; it drives relevance scoring. `keywords`: extra must-know terms (products, symptoms, brands)."""
    sid = app().researcher.create_study(name, brief, keywords or [])
    return f"Study '{name}' ready (id {sid}). Next: find_subreddits, then discover_threads."


@mcp.tool()
async def find_subreddits(query: str, limit: int = 15) -> str:
    """Find communities by name/topic, with subscriber counts. Use to pick where the avatar hangs out."""
    rows = await app().source.find_subreddits(query, limit)
    return _j(rows)


@mcp.tool()
async def discover_threads(study: str, queries: list[str], subreddits: list[str] | None = None,
                           time_range: str = "all", limit_per_query: int = 50, sort: str = "relevance",
                           max_seconds: int = 300) -> str:
    """Seed the study: search Reddit for each query (inside each subreddit if given). Results become crawl
    candidates ranked by relevance and engagement. time_range: hour/day/week/month/year/all.
    sort: relevance/top/comments/new. With no queries, pulls each subreddit's top threads. Searches left
    undone when max_seconds runs out are listed in not_run_time_limit; call again with just those."""
    res = await app().researcher.discover(study, queries, subreddits, time_range, limit_per_query, sort, max_seconds)
    res["top_candidates"] = [f"p:{c['id']} | r/{c['subreddit']} | {c['num_comments']} comments | {clip(c['title'], 90)}"
                             for c in res["top_candidates"]]
    return _j(res)


@mcp.tool()
async def crawl_web(study: str, max_threads: int = 25, max_hops: int = 2, min_relevance: float = 0.2,
                    per_subreddit_cap: int | None = None, max_seconds: int = 240) -> str:
    """Fetch the best candidates (full comment trees) and follow their connections: threads linked in
    comments, crossposts and other submissions of the same link. Each hop away from the seeds lowers
    priority. Stops at max_threads or max_seconds; call again to continue."""
    res = await app().researcher.crawl(study, max_threads, max_hops, min_relevance, per_subreddit_cap, max_seconds)
    res["fetched"] = [f"p:{f['id']} | {f['comments']} comments ({round(f['coverage'] * 100)}%) | hop {f['hop']} | "
                      f"{clip(f['title'], 80)}" for f in res["fetched"]]
    return _j(res)


@mcp.tool()
async def fetch_thread(url_or_id: str, study: str | None = None) -> str:
    """Fetch one thread completely (every hidden reply expanded) by URL or id; optionally add it to a study."""
    res = await app().researcher.fetch(url_or_id, study)
    return _j(res)


@mcp.tool()
async def read_thread(thread_id: str, mode: str = "top", max_chars: int = 12000, offset: int = 0,
                      min_score: int | None = None) -> str:
    """Read a stored thread. mode: 'outline' (top-level comments, short), 'top' (best comments to depth 2),
    'all' (every comment, paged with offset). Comments show [c:id|score|Ldepth|OP]."""
    return thread_text(app().store, parse_post_id(thread_id.removeprefix("p:")), mode, max_chars, offset, min_score)


@mcp.tool()
async def search_corpus(query: str, study: str | None = None, kind: str = "comments", limit: int = 20,
                        offset: int = 0, min_score: int | None = None) -> str:
    """Full-text search over everything fetched (or one study). kind: comments/posts. Supports "exact phrase",
    OR, NOT, prefix*. Results are ranked by match quality and upvotes."""
    a = app()
    sid = a.store.study_id(study) if study else None
    rows = a.store.search(query, kind, sid, limit, offset, min_score)
    if kind == "posts":
        lines = [f"p:{r['id']} | r/{r['subreddit']} | {r['num_comments']} comments | {clip(r['title'], 90)} | {r['snip']}"
                 for r in rows]
    else:
        lines = [f"c:{r['id']} (p:{r['post_id']}, {r['score']:+d}) {r['snip']}" for r in rows]
    return "\n".join(lines) or "No matches."


@mcp.tool()
async def graph_overview(study: str, rebuild: bool = True) -> str:
    """Build the web of threads and summarise it: groups (communities) of connected threads with their key
    terms, hub threads (most central), bridge threads (connect different groups), and subreddit spread."""
    a = app()
    sid = a.store.study_id(study)
    built = graphlib.build(a.store, sid) if rebuild else {}
    ov = graphlib.overview(a.store, sid)
    for c in ov["communities"]:
        c["hub_threads"] = [f"p:{t['id']} | r/{t['subreddit']} | {t['num_comments']} comments | {clip(t['title'], 80)}"
                            for t in c["hub_threads"]]
    ov["bridge_threads"] = [f"p:{b['id']} | group {b['community']} | {clip(b['title'], 80)}" for b in ov["bridge_threads"]]
    return _j({"build": built} | ov)


@mcp.tool()
async def name_group(study: str, community: int, label: str) -> str:
    """Give a thread group (community number from graph_overview) a human name, e.g. 'minoxidil dread'."""
    a = app()
    graphlib.label_community(a.store, a.store.study_id(study), community, label)
    return "ok"


@mcp.tool()
async def thread_neighbors(study: str, thread_id: str, limit: int = 15) -> str:
    """Threads connected to this one in the study's web, strongest first, with why they're connected."""
    a = app()
    rows = graphlib.neighbors(a.store, a.store.study_id(study), thread_id.removeprefix("p:"), limit)
    return _j([f"p:{r['id']} | w={r['weight']} | {clip(r['title'], 70)} | {'; '.join(r['connections'][:3])}"
               for r in rows])


@mcp.tool()
async def next_threads_to_analyze(study: str, count: int = 5) -> str:
    """The next fetched-but-unanalysed threads, most important first. Read each, then save_insights with
    analyzed_thread_ids so they drop off this list."""
    a = app()
    rows = insightlib.next_threads(a.store, a.store.study_id(study), count)
    return _j({"insight_kinds": insightlib.KINDS,
               "threads": [f"p:{r['id']} | r/{r['subreddit']} | {r['fetched_comments']} comments | {clip(r['title'], 80)}"
                           for r in rows]})


@mcp.tool()
async def save_insights(study: str, items: list[dict], analyzed_thread_ids: list[str] | None = None) -> str:
    """Save findings. Each item: {kind, label, quote, source_id, note?}. kind is one of the insight kinds
    (pain, desire, failed_solution, objection, belief, trigger, brand, price, buying_intent, question,
    identity, language, angle, other). label = short normalized name you'll reuse across threads
    (e.g. 'biotin', 'shedding panic'). quote must be copied exactly from the source (use ... to skip words).
    source_id = c:<id> or p:<id>. Items whose quote isn't verbatim are rejected with a reason."""
    a = app()
    return _j(insightlib.save(a.store, a.store.study_id(study), items, analyzed_thread_ids))


@mcp.tool()
async def insights_report(study: str, kind: str | None = None, min_support: int = 1, limit: int = 25,
                          quotes_per_label: int = 3) -> str:
    """Aggregated findings: each label with how many distinct people said it, in how many threads, total
    upvotes, and the strongest verbatim quotes with links."""
    a = app()
    rows = insightlib.report(a.store, a.store.study_id(study), kind, min_support, limit, quotes_per_label)
    return _j(rows)


@mcp.tool()
async def export_results(study: str | None = None, format: str = "md", thread_id: str | None = None) -> str:
    """Write files to the exports folder. Study formats: md (insights report), insights_csv, csv/json (all
    comments), html (interactive thread-web map), gexf (for Gephi). Thread formats (thread_id): csv/json/text."""
    a = app()
    folder = config.export_dir()
    if thread_id:
        path = export_thread(a.store, thread_id.removeprefix("p:"), format, folder)
    else:
        sid = a.store.study_id(study)
        if format in ("html", "gexf") and not a.store.one("SELECT 1 FROM graph_nodes WHERE study_id=?", (sid,)):
            graphlib.build(a.store, sid)
        path = export_study(a.store, sid, format, folder)
    return f"Saved {path}"


def main() -> None:
    mcp.run("stdio")


if __name__ == "__main__":
    main()
