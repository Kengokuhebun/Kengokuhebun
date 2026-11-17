import asyncio

import pytest

from redditresearch import graph as graphlib
from redditresearch import insights as insightlib
from redditresearch.export import export_study, export_thread, thread_rows
from redditresearch.fetcher import fetch_full_thread, parse_post_id
from redditresearch.links import extract, product_key
from redditresearch.render import thread_text
from redditresearch.research import Researcher
from redditresearch.sources.base import FallbackSource, SourceError
from redditresearch.store import Store
from redditresearch.util import quote_in_text

from fakes import FakeReddit


def run(coro):
    return asyncio.run(coro)


@pytest.fixture
def store(tmp_path):
    s = Store(tmp_path / "t.db")
    yield s
    s.close()


def test_parse_post_id():
    assert parse_post_id("https://www.reddit.com/r/beyondthebump/comments/1w4szr6/some_title/") == "1w4szr6"
    assert parse_post_id("https://old.reddit.com/r/x/comments/abc123/t/def456/?context=3") == "abc123"
    assert parse_post_id("https://redd.it/abc123") == "abc123"
    assert parse_post_id("abc123") == "abc123"
    with pytest.raises(ValueError):
        parse_post_id("https://example.com/")


def test_full_thread_expands_more_and_continue_stubs():
    fake = FakeReddit()
    post, comments, stats = run(fetch_full_thread(fake, "aaa111"))
    ids = {c["id"] for c in comments}
    assert ids == {"c1", "c2", "c3", "c4", "c5", "c6"}  # c4/c5 via morechildren, c6 via continue-thread
    by_id = {c["id"]: c for c in comments}
    assert by_id["c6"]["depth"] == 2 and by_id["c6"]["path"] == "c1/c2/c6"
    assert by_id["c4"]["depth"] == 0
    assert ("more", "aaa111", ("c4", "c5")) in fake.calls
    assert ("subtree", "aaa111", "c2") in fake.calls
    assert stats["unexpanded_stubs"] == 0


def test_links_and_products():
    found = extract("see https://old.reddit.com/r/Hair/comments/xyz789/title/ and redd.it/abc123 "
                    "and https://www.amazon.com/dp/B0ABCDEF12?ref=x and https://shop.example.com/products/Scalp-Oil")
    kinds = {(f["kind"], f.get("target_post_id") or f.get("product_key")) for f in found}
    assert ("reddit_thread", "xyz789") in kinds and ("reddit_thread", "abc123") in kinds
    assert ("external", "amazon:B0ABCDEF12") in kinds
    assert ("external", "shop:shop.example.com/scalp-oil") in kinds
    assert product_key("https://www.amazon.com/Some-Thing/dp/B0ABCDEF12/ref=sr_1") == "amazon:B0ABCDEF12"


def test_quote_verification():
    src = "I tried biotin for three months and it did “absolutely nothing” for my  shedding."
    assert quote_in_text('it did "absolutely nothing" for my shedding', src)
    assert quote_in_text("I tried biotin ... for my shedding", src)
    assert quote_in_text("I TRIED BIOTIN for three months", src)  # case-insensitive
    assert not quote_in_text("biotin did nothing for my shedding", src)  # paraphrase
    assert not quote_in_text("for my shedding ... I tried biotin", src)  # wrong order
    assert not quote_in_text("biotin", src)  # too short to be evidence


def test_discover_crawl_graph_insights_export(store, tmp_path):
    fake = FakeReddit()
    r = Researcher(store, fake)
    r.create_study("pp-hair", "postpartum hair loss shedding scalp oil, failed solutions like biotin and minoxidil",
                   ["rosemary oil", "biotin"])
    res = run(r.discover("pp-hair", ["postpartum hair loss"], ["beyondthebump"]))
    assert res["new_candidates"] >= 1 and not res["errors"]

    crawl = run(r.crawl("pp-hair", max_threads=10, max_hops=1, min_relevance=0.2))
    fetched = {f.split(" | ")[0] if isinstance(f, str) else f["id"] for f in crawl["fetched"]}
    assert "aaa111" in fetched
    assert "bbb222" in fetched  # reached by following the link inside comment c3 (hop 1)
    assert "ccc333" not in fetched  # off-topic stroller thread never crawled
    hops = {f["id"]: f["hop"] for f in crawl["fetched"]}
    assert hops["bbb222"] in (0, 1)

    # Add the minoxidil thread manually and build the web.
    run(r.fetch("https://www.reddit.com/r/FemaleHairLoss/comments/ddd444/x/", "pp-hair"))
    sid = store.study_id("pp-hair")
    built = graphlib.build(store, sid)
    assert built["threads"] == 3
    types = built["edge_types"]
    assert types.get("link") == 1  # aaa111 -> bbb222
    assert types.get("shared_product") == 1  # same Amazon dropper in bbb222 and ddd444
    ov = graphlib.overview(store, sid)
    assert ov["communities"] and ov["edge_types"]
    nb = graphlib.neighbors(store, sid, "aaa111")
    assert any(n["id"] == "bbb222" for n in nb)

    text = thread_text(store, "aaa111", mode="all")
    assert "[c:c6|+6|L2]" in text and "end of thread" in text
    paged = thread_text(store, "aaa111", mode="all", max_chars=300)
    assert "Next page: offset=" in paged

    nxt = insightlib.next_threads(store, sid, 10)
    assert len(nxt) == 3
    out = insightlib.save(store, sid, [
        {"kind": "failed_solution", "label": "Biotin", "quote": "biotin for three months and it did absolutely nothing",
         "source_id": "c:c1"},
        {"kind": "failed_solution", "label": "biotin", "quote": "Biotin did nothing for me either", "source_id": "c:c12"},
        {"kind": "failed_solution", "label": "biotin", "quote": "biotin just gave me acne", "source_id": "c2"},
        {"kind": "pain", "label": "shedding panic", "quote": "The 2am shower panic is real", "source_id": "c:c6"},
        {"kind": "pain", "label": "made up", "quote": "my hair is falling out in handfuls", "source_id": "c:c6"},
        {"kind": "nonsense", "label": "x", "quote": "whatever whatever", "source_id": "c:c6"},
    ], analyzed_thread_ids=["p:aaa111"])
    assert out["saved"] == 4
    assert len(out["rejected"]) == 2 and out["threads_left_to_analyze"] == 2
    rep = insightlib.report(store, sid, kind="failed_solution")
    assert rep[0]["label"] == "biotin" and rep[0]["support"] == 3 and rep[0]["threads"] == 2

    hits = store.search("biotin", "comments", sid)
    assert {h["id"] for h in hits} >= {"c1", "c12"}
    assert store.search('"dread shed"', "comments", sid)[0]["id"] == "c30"

    folder = tmp_path / "exports"
    folder.mkdir()
    rows = thread_rows(store, "aaa111")
    assert rows[0]["type"] == "post" and len(rows) == 7
    for fmt in ("csv", "json", "text"):
        assert export_thread(store, "aaa111", fmt, folder).stat().st_size > 50
    for fmt in ("csv", "json", "html", "gexf", "md", "insights_csv"):
        path = export_study(store, sid, fmt, folder)
        assert path.stat().st_size > 50, fmt
    md = (folder / "study-pp-hair-insights.md").read_text(encoding="utf-8")
    assert "biotin" in md and "absolutely nothing" in md


def test_fallback_source_routes_around_failures():
    class Broken(FakeReddit):
        name = "broken"

        async def thread(self, post_id):
            raise SourceError("403")

    fb = FallbackSource(Broken(), FakeReddit())
    post, children = run(fb.thread("aaa111"))
    assert post["id"] == "aaa111" and fb.notes
