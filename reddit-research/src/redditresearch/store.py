"""SQLite storage: threads, comments, full-text index, studies, the thread web, and verified insights."""

from __future__ import annotations

import json
import math
import re
import sqlite3
import time
from pathlib import Path

from . import links as linklib
from .util import strip_prefix

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS posts(
  id TEXT PRIMARY KEY, subreddit TEXT, title TEXT, selftext TEXT, author TEXT, score INTEGER,
  upvote_ratio REAL, num_comments INTEGER, created_utc INTEGER, url TEXT, domain TEXT, permalink TEXT,
  flair TEXT, over_18 INTEGER, crosspost_parent TEXT, num_crossposts INTEGER DEFAULT 0, fetched_comments INTEGER DEFAULT 0,
  coverage REAL, source TEXT, fetched_at INTEGER, meta_only INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS comments(
  id TEXT PRIMARY KEY, post_id TEXT, parent_id TEXT, path TEXT, depth INTEGER, author TEXT, score INTEGER,
  body TEXT, created_utc INTEGER, is_submitter INTEGER, controversiality INTEGER, permalink TEXT
);
CREATE INDEX IF NOT EXISTS comments_post ON comments(post_id);
CREATE INDEX IF NOT EXISTS comments_author ON comments(author);
CREATE VIRTUAL TABLE IF NOT EXISTS posts_fts USING fts5(id UNINDEXED, title, selftext, tokenize='porter unicode61');
CREATE VIRTUAL TABLE IF NOT EXISTS comments_fts USING fts5(id UNINDEXED, post_id UNINDEXED, body, tokenize='porter unicode61');
CREATE TABLE IF NOT EXISTS links(
  source_id TEXT, post_id TEXT, kind TEXT, url TEXT, target_post_id TEXT, domain TEXT,
  product_key TEXT, brand_domain TEXT, PRIMARY KEY(source_id, url)
);
CREATE INDEX IF NOT EXISTS links_post ON links(post_id);
CREATE TABLE IF NOT EXISTS studies(
  id INTEGER PRIMARY KEY, name TEXT UNIQUE, brief TEXT, keywords TEXT, created_at INTEGER
);
CREATE TABLE IF NOT EXISTS study_posts(
  study_id INTEGER, post_id TEXT, status TEXT DEFAULT 'candidate', relevance REAL DEFAULT 0,
  priority REAL DEFAULT 0, hop INTEGER DEFAULT 0, via TEXT, queries TEXT DEFAULT '', analyzed INTEGER DEFAULT 0,
  added_at INTEGER, PRIMARY KEY(study_id, post_id)
);
CREATE TABLE IF NOT EXISTS edges(
  study_id INTEGER, src TEXT, dst TEXT, type TEXT, weight REAL, evidence TEXT,
  PRIMARY KEY(study_id, src, dst, type)
);
CREATE TABLE IF NOT EXISTS graph_nodes(
  study_id INTEGER, post_id TEXT, community INTEGER, pagerank REAL, betweenness REAL, degree INTEGER,
  PRIMARY KEY(study_id, post_id)
);
CREATE TABLE IF NOT EXISTS communities(
  study_id INTEGER, community INTEGER, label TEXT, terms TEXT, size INTEGER, PRIMARY KEY(study_id, community)
);
CREATE TABLE IF NOT EXISTS insights(
  id INTEGER PRIMARY KEY, study_id INTEGER, kind TEXT, label TEXT, quote TEXT, source_id TEXT, post_id TEXT,
  author TEXT, score INTEGER, permalink TEXT, note TEXT, created_at INTEGER,
  UNIQUE(study_id, kind, label, source_id, quote)
);
"""


class Store:
    def __init__(self, path: str | Path):
        self.path = str(path)
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        # Portable log(): SQLite's own math functions aren't compiled into every Python build.
        self.db.create_function("rr_log", 1, lambda x: math.log(x) if x and x > 0 else 0.0, deterministic=True)
        self.db.executescript(SCHEMA)
        self._migrate()

    def _migrate(self) -> None:
        """Add columns introduced after a database was first created."""
        added = {"posts": {"num_crossposts": "INTEGER DEFAULT 0"}}
        for table, cols in added.items():
            have = {r["name"] for r in self.db.execute(f"PRAGMA table_info({table})")}
            for col, decl in cols.items():
                if col not in have:
                    self.db.execute(f"ALTER TABLE {table} ADD COLUMN {col} {decl}")
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    def q(self, sql: str, params=()) -> list[sqlite3.Row]:
        return self.db.execute(sql, params).fetchall()

    def one(self, sql: str, params=()):
        return self.db.execute(sql, params).fetchone()

    # ---------------------------------------------------------------- posts & comments
    def upsert_post_meta(self, raw: dict, source: str) -> str | None:
        """Store post metadata (from search/listing/info) without clobbering a fetched thread."""
        p = normalize_post(raw)
        if not p["id"]:
            return None
        existing = self.one("SELECT meta_only FROM posts WHERE id=?", (p["id"],))
        if existing is None:
            self.db.execute(
                "INSERT INTO posts(id,subreddit,title,selftext,author,score,upvote_ratio,num_comments,created_utc,"
                "url,domain,permalink,flair,over_18,crosspost_parent,num_crossposts,source,fetched_at,meta_only) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)",
                (p["id"], p["subreddit"], p["title"], p["selftext"], p["author"], p["score"], p["upvote_ratio"],
                 p["num_comments"], p["created_utc"], p["url"], p["domain"], p["permalink"], p["flair"],
                 p["over_18"], p["crosspost_parent"], p["num_crossposts"], source, int(time.time())),
            )
            self._index_post(p)
        elif existing["meta_only"]:
            # Prefer the larger engagement numbers (archives report 0/1 for very fresh posts).
            self.db.execute(
                "UPDATE posts SET score=MAX(COALESCE(score,0),?), num_comments=MAX(COALESCE(num_comments,0),?),"
                " title=COALESCE(NULLIF(title,''),?), selftext=COALESCE(NULLIF(selftext,''),?) WHERE id=?",
                (p["score"], p["num_comments"], p["title"], p["selftext"], p["id"]),
            )
        self.db.commit()
        return p["id"]

    def save_thread(self, raw_post: dict, comments: list[dict], source: str) -> dict:
        p = normalize_post(raw_post)
        alive = [c for c in comments if c["body"] not in ("[deleted]", "[removed]")]
        coverage = round(len(alive) / p["num_comments"], 3) if p["num_comments"] else 1.0
        self.db.execute("DELETE FROM posts WHERE id=?", (p["id"],))
        self.db.execute(
            "INSERT INTO posts(id,subreddit,title,selftext,author,score,upvote_ratio,num_comments,created_utc,url,"
            "domain,permalink,flair,over_18,crosspost_parent,num_crossposts,fetched_comments,coverage,source,fetched_at,"
            "meta_only) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)",
            (p["id"], p["subreddit"], p["title"], p["selftext"], p["author"], p["score"], p["upvote_ratio"],
             max(p["num_comments"], len(alive)), p["created_utc"], p["url"], p["domain"], p["permalink"], p["flair"],
             p["over_18"], p["crosspost_parent"], p["num_crossposts"], len(alive), min(coverage, 1.0), source,
             int(time.time())),
        )
        self.db.execute("DELETE FROM comments WHERE post_id=?", (p["id"],))
        self.db.execute("DELETE FROM comments_fts WHERE post_id=?", (p["id"],))
        self.db.executemany(
            "INSERT OR REPLACE INTO comments(id,post_id,parent_id,path,depth,author,score,body,created_utc,"
            "is_submitter,controversiality,permalink) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            [(c["id"], p["id"], c["parent_id"], c["path"], c["depth"], c["author"], c["score"], c["body"],
              c["created_utc"], c["is_submitter"], c["controversiality"], c["permalink"]) for c in comments],
        )
        self.db.executemany(
            "INSERT INTO comments_fts(id,post_id,body) VALUES(?,?,?)",
            [(c["id"], p["id"], c["body"]) for c in alive],
        )
        self._index_post(p)
        self._save_links(p, comments)
        self.db.commit()
        return {"id": p["id"], "title": p["title"], "comments": len(alive), "num_comments": p["num_comments"],
                "coverage": min(coverage, 1.0)}

    def _index_post(self, p: dict) -> None:
        self.db.execute("DELETE FROM posts_fts WHERE id=?", (p["id"],))
        self.db.execute("INSERT INTO posts_fts(id,title,selftext) VALUES(?,?,?)", (p["id"], p["title"], p["selftext"]))

    def _save_links(self, p: dict, comments: list[dict]) -> None:
        self.db.execute("DELETE FROM links WHERE post_id=?", (p["id"],))
        rows = []
        sources = [(f"p:{p['id']}", (p["selftext"] or "") + "\n" + (p["url"] or ""))]
        sources += [(f"c:{c['id']}", c["body"]) for c in comments]
        for source_id, text in sources:
            for ln in linklib.extract(text):
                if ln.get("target_post_id") == p["id"]:
                    continue  # self-reference
                rows.append((source_id, p["id"], ln["kind"], ln["url"][:500], ln.get("target_post_id"),
                             ln.get("domain"), ln.get("product_key"), ln.get("brand_domain")))
        self.db.executemany("INSERT OR IGNORE INTO links VALUES(?,?,?,?,?,?,?,?)", rows)

    def post(self, post_id: str):
        return self.one("SELECT * FROM posts WHERE id=?", (post_id,))

    def comments_for(self, post_id: str) -> list[sqlite3.Row]:
        return self.q("SELECT * FROM comments WHERE post_id=?", (post_id,))

    # ---------------------------------------------------------------- studies
    def create_study(self, name: str, brief: str, keywords: list[str]) -> int:
        self.db.execute(
            "INSERT INTO studies(name,brief,keywords,created_at) VALUES(?,?,?,?) "
            "ON CONFLICT(name) DO UPDATE SET brief=excluded.brief, keywords=excluded.keywords",
            (name, brief, json.dumps(keywords), int(time.time())),
        )
        self.db.commit()
        return self.study_id(name)

    def study_id(self, name_or_id) -> int:
        row = self.one("SELECT id FROM studies WHERE name=? OR CAST(id AS TEXT)=?", (str(name_or_id), str(name_or_id)))
        if not row:
            names = [r["name"] for r in self.q("SELECT name FROM studies ORDER BY id")]
            raise KeyError(f"No study named {name_or_id!r}. Existing studies: {names or 'none (create one first)'}")
        return row["id"]

    def study(self, study_id: int):
        row = self.one("SELECT * FROM studies WHERE id=?", (study_id,))
        return dict(row) | {"keywords": json.loads(row["keywords"] or "[]")}

    def add_candidate(self, study_id: int, post_id: str, relevance: float, priority: float, hop: int,
                      via: str, query: str | None = None) -> bool:
        """Add or strengthen a candidate. Returns True if it is new to the study."""
        row = self.one("SELECT priority, queries FROM study_posts WHERE study_id=? AND post_id=?", (study_id, post_id))
        if row is None:
            self.db.execute(
                "INSERT INTO study_posts(study_id,post_id,relevance,priority,hop,via,queries,added_at) VALUES(?,?,?,?,?,?,?,?)",
                (study_id, post_id, relevance, priority, hop, via, query or "", int(time.time())),
            )
            return True
        queries = set(filter(None, (row["queries"] or "").split("\x1f")))
        if query:
            queries.add(query)
        bonus = 0.05 * max(0, len(queries) - 1)  # found by several searches -> more central
        self.db.execute(
            "UPDATE study_posts SET priority=MAX(priority,?)+?, relevance=MAX(relevance,?), hop=MIN(hop,?), queries=? "
            "WHERE study_id=? AND post_id=?",
            (priority, bonus, relevance, hop, "\x1f".join(sorted(queries)), study_id, post_id),
        )
        return False

    def study_post_ids(self, study_id: int, status: str | None = "fetched") -> list[str]:
        if status:
            rows = self.q("SELECT post_id FROM study_posts WHERE study_id=? AND status=?", (study_id, status))
        else:
            rows = self.q("SELECT post_id FROM study_posts WHERE study_id=?", (study_id,))
        return [r["post_id"] for r in rows]

    def stats(self) -> dict:
        def count(sql):
            return self.one(sql)[0]
        return {
            "threads_fetched": count("SELECT COUNT(*) FROM posts WHERE meta_only=0"),
            "posts_known": count("SELECT COUNT(*) FROM posts"),
            "comments": count("SELECT COUNT(*) FROM comments"),
            "studies": count("SELECT COUNT(*) FROM studies"),
            "insights": count("SELECT COUNT(*) FROM insights"),
        }

    # ---------------------------------------------------------------- search
    def search(self, query: str, kind: str = "comments", study_id: int | None = None, limit: int = 20,
               offset: int = 0, min_score: int | None = None) -> list[dict]:
        match = fts_query(query)
        params: list = [match]
        if kind == "posts":
            sql = ("SELECT p.*, snippet(posts_fts, 2, '[', ']', '…', 24) AS snip, bm25(posts_fts) AS rank "
                   "FROM posts_fts JOIN posts p ON p.id = posts_fts.id WHERE posts_fts MATCH ?")
            if study_id is not None:
                sql += " AND p.id IN (SELECT post_id FROM study_posts WHERE study_id=?)"
                params.append(study_id)
            if min_score is not None:
                sql += " AND p.score >= ?"
                params.append(min_score)
        else:
            sql = ("SELECT c.*, p.title AS post_title, p.subreddit, snippet(comments_fts, 2, '[', ']', '…', 32) AS snip, "
                   "bm25(comments_fts) AS rank FROM comments_fts JOIN comments c ON c.id = comments_fts.id "
                   "JOIN posts p ON p.id = c.post_id WHERE comments_fts MATCH ?")
            if study_id is not None:
                sql += " AND c.post_id IN (SELECT post_id FROM study_posts WHERE study_id=? AND status='fetched')"
                params.append(study_id)
            if min_score is not None:
                sql += " AND c.score >= ?"
                params.append(min_score)
        # Blend text relevance with upvotes: bm25 is negative (lower = better).
        alias = "p" if kind == "posts" else "c"
        sql += f" ORDER BY rank - 0.5 * rr_log(MAX({alias}.score, 1) + 1) LIMIT ? OFFSET ?"
        params += [limit, offset]
        return [dict(r) for r in self.q(sql, params)]


def fts_query(query: str) -> str:
    """Pass FTS5 syntax through when it looks intentional; otherwise AND the quoted words."""
    q = (query or "").strip()
    if re.search(r'"|\bOR\b|\bAND\b|\bNOT\b|\bNEAR\(|\*', q):
        return q
    words = re.findall(r"[\w']+", q)
    return " ".join(f'"{w}"' for w in words) or '""'


def normalize_post(raw: dict) -> dict:
    d = raw.get("data", raw) if isinstance(raw, dict) else {}
    pid = d.get("id") or strip_prefix(d.get("name"))
    permalink = d.get("permalink") or (f"/comments/{pid}/" if pid else "")
    url = d.get("url") or d.get("url_overridden_by_dest") or ""
    is_self = d.get("is_self") or (url and "reddit.com" in url and f"/comments/{pid}" in url)
    crosspost = d.get("crosspost_parent")
    if not crosspost and d.get("crosspost_parent_list"):
        crosspost = d["crosspost_parent_list"][0].get("name")
    return {
        "id": pid,
        "subreddit": d.get("subreddit") or "",
        "title": d.get("title") or "",
        "selftext": d.get("selftext") or "",
        "author": d.get("author") or "[deleted]",
        "score": _int(d.get("score")),
        "upvote_ratio": d.get("upvote_ratio"),
        "num_comments": _int(d.get("num_comments")),
        "created_utc": _int(d.get("created_utc")),
        "url": "" if is_self else url,
        "domain": "" if is_self else linklib.domain_of(url),
        "permalink": "https://www.reddit.com" + permalink if permalink.startswith("/") else permalink,
        "flair": d.get("link_flair_text") or "",
        "over_18": 1 if d.get("over_18") else 0,
        "crosspost_parent": strip_prefix(crosspost),
        "num_crossposts": _int(d.get("num_crossposts")),
    }


def _int(v) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0
