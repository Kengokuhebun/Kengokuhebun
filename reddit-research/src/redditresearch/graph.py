"""Build and analyse the web of threads: which threads connect, which groups they form, which are hubs."""

from __future__ import annotations

import html
import json
import math
from collections import Counter, defaultdict
from itertools import combinations

import networkx as nx

from .store import Store
from .util import clip, tokens

IGNORED_AUTHORS = {"[deleted]", "AutoModerator", "[removed]"}
EDGE_LABELS = {
    "link": "one thread links to the other",
    "crosspost": "crossposted",
    "same_link": "both share the same URL",
    "shared_product": "both mention the same product page",
    "shared_brand": "both link the same brand site",
    "similar": "similar wording/topic",
    "audience": "same people commented in both",
}


# ---------------------------------------------------------------------- text similarity
def _docs(store: Store, ids: list[str]) -> dict[str, Counter]:
    docs = {}
    for pid in ids:
        p = store.post(pid)
        top = store.q("SELECT body FROM comments WHERE post_id=? ORDER BY score DESC LIMIT 30", (pid,))
        text = f"{p['title']} {p['title']} {p['selftext'] or ''} " + " ".join(r["body"] for r in top)
        docs[pid] = Counter(tokens(text))
    return docs


def _tfidf(docs: dict[str, Counter], keep: int = 60) -> tuple[dict[str, dict[str, float]], dict[str, float]]:
    n = len(docs)
    df = Counter(t for c in docs.values() for t in c)
    # Keep topic words unless nearly every thread has them: inside a focused study the shared vocabulary
    # (minoxidil vs rosemary vs biotin) is exactly what separates sub-topics.
    idf = {t: math.log((n + 1) / (d + 0.5)) for t, d in df.items() if d <= max(2, 0.85 * n)}
    vecs = {}
    for pid, counts in docs.items():
        w = {t: (1 + math.log(c)) * idf[t] for t, c in counts.items() if t in idf}
        top = dict(sorted(w.items(), key=lambda kv: -kv[1])[:keep])
        norm = math.sqrt(sum(v * v for v in top.values())) or 1.0
        vecs[pid] = {t: v / norm for t, v in top.items()}
    return vecs, idf


def _similar_pairs(vecs: dict[str, dict[str, float]], k: int = 3, threshold: float = 0.04) -> dict[tuple, float]:
    """k-nearest-neighbour similarity graph: each thread links to its k most similar threads."""
    postings: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for pid, v in vecs.items():
        for t, w in v.items():
            postings[t].append((pid, w))
    pairs = {}
    for pid, v in vecs.items():
        scores: Counter = Counter()
        for t, w in v.items():
            for other, w2 in postings[t]:
                if other != pid:
                    scores[other] += w * w2
        for other, s in scores.most_common(k):
            if s >= threshold:
                key = tuple(sorted((pid, other)))
                pairs[key] = max(pairs.get(key, 0), round(s, 3))
    return pairs


def pagerank(g: nx.Graph, alpha: float = 0.85, iters: int = 100, tol: float = 1e-8) -> dict:
    """Weighted PageRank by power iteration (pure Python, so no numpy/scipy install is needed)."""
    nodes = list(g.nodes)
    n = len(nodes)
    if not n:
        return {}
    rank = dict.fromkeys(nodes, 1.0 / n)
    strength = {u: sum(d.get("weight", 1.0) for _, _, d in g.edges(u, data=True)) for u in nodes}
    for _ in range(iters):
        dangling = alpha * sum(rank[u] for u in nodes if strength[u] == 0) / n
        new = dict.fromkeys(nodes, (1 - alpha) / n + dangling)
        for u in nodes:
            if strength[u]:
                share = alpha * rank[u] / strength[u]
                for _, v, d in g.edges(u, data=True):
                    new[v] += share * d.get("weight", 1.0)
        if sum(abs(new[u] - rank[u]) for u in nodes) < n * tol:
            return new
        rank = new
    return rank


# ---------------------------------------------------------------------- build
def build(store: Store, study_id: int) -> dict:
    ids = store.study_post_ids(study_id, "fetched")
    idset = set(ids)
    edges: dict[tuple, tuple[float, str]] = {}

    def add(a, b, typ, weight, evidence):
        if a == b or a not in idset or b not in idset:
            return
        key = (*sorted((a, b)), typ)
        if key not in edges or edges[key][0] < weight:
            edges[key] = (round(weight, 3), evidence)

    if not ids:
        return {"threads": 0, "edges": 0}
    marks = ",".join("?" * len(ids))
    for r in store.q(f"SELECT post_id, target_post_id, COUNT(*) n, MIN(source_id) ev FROM links WHERE kind='reddit_thread' "
                     f"AND post_id IN ({marks}) GROUP BY post_id, target_post_id", ids):
        add(r["post_id"], r["target_post_id"], "link", min(2.0, 1 + 0.25 * (r["n"] - 1)), f"{r['n']} link(s), e.g. {r['ev']}")
    for r in store.q(f"SELECT id, crosspost_parent FROM posts WHERE id IN ({marks}) AND crosspost_parent IS NOT NULL", ids):
        add(r["id"], r["crosspost_parent"], "crosspost", 1.5, "crosspost")
    by_url = defaultdict(list)
    for r in store.q(f"SELECT id, url FROM posts WHERE id IN ({marks}) AND url != ''", ids):
        by_url[r["url"]].append(r["id"])
    for url, group in by_url.items():
        for a, b in combinations(group[:30], 2):
            add(a, b, "same_link", 1.2, clip(url, 120))
    for col, typ, weight in (("product_key", "shared_product", 0.8), ("brand_domain", "shared_brand", 0.4)):
        groups = defaultdict(set)
        for r in store.q(f"SELECT post_id, {col} k FROM links WHERE {col} IS NOT NULL AND post_id IN ({marks})", ids):
            groups[r["k"]].add(r["post_id"])
        for key, group in groups.items():
            if 2 <= len(group) <= 30:
                for a, b in combinations(sorted(group), 2):
                    add(a, b, typ, weight, key)

    docs = _docs(store, ids)
    vecs, idf = _tfidf(docs)
    sims = _similar_pairs(vecs)
    top = max(sims.values(), default=1.0) or 1.0
    for (a, b), s in sims.items():
        add(a, b, "similar", 0.8 * s / top, f"cosine {s}")  # scaled so the closest pair in the study = 0.8

    authors = defaultdict(set)
    for r in store.q(f"SELECT post_id, author FROM comments WHERE post_id IN ({marks})", ids):
        if r["author"] not in IGNORED_AUTHORS:
            authors[r["post_id"]].add(r["author"])
    by_author = defaultdict(set)
    for pid, names in authors.items():
        for a in names:
            by_author[a].add(pid)
    shared = Counter()
    for pids in by_author.values():
        if 2 <= len(pids) <= 40:
            for a, b in combinations(sorted(pids), 2):
                shared[(a, b)] += 1
    for (a, b), n in shared.items():
        if n >= 3:  # aggregate count only: we never surface who the people are
            add(a, b, "audience", min(1.0, n / 10) * 0.6, f"{n} shared commenters")

    store.db.execute("DELETE FROM edges WHERE study_id=?", (study_id,))
    store.db.executemany("INSERT INTO edges VALUES(?,?,?,?,?,?)",
                         [(study_id, a, b, t, w, ev) for (a, b, t), (w, ev) in edges.items()])

    g = nx.Graph()
    g.add_nodes_from(ids)
    for (a, b, _t), (w, _ev) in edges.items():
        g.add_edge(a, b, weight=g[a][b]["weight"] + w if g.has_edge(a, b) else w)
    connected = [n for n in g.nodes if g.degree(n) > 0]
    community_of = {n: -1 for n in g.nodes}
    if connected:
        comms = nx.community.louvain_communities(g.subgraph(connected), weight="weight", seed=7)
        for i, members in enumerate(sorted(comms, key=len, reverse=True)):
            for m in members:
                community_of[m] = i
    pr = pagerank(g)
    k = min(len(ids), 300) if len(ids) > 300 else None
    bc = nx.betweenness_centrality(g, k=k, seed=7) if g.number_of_edges() else {n: 0.0 for n in ids}

    store.db.execute("DELETE FROM graph_nodes WHERE study_id=?", (study_id,))
    store.db.executemany("INSERT INTO graph_nodes VALUES(?,?,?,?,?,?)",
                         [(study_id, n, community_of[n], pr[n], bc[n], g.degree(n)) for n in ids])
    store.db.execute("DELETE FROM communities WHERE study_id=?", (study_id,))
    members = defaultdict(list)
    for n, c in community_of.items():
        if c >= 0:
            members[c].append(n)
    for c, group in members.items():
        agg = Counter()
        for n in group:
            agg.update(vecs.get(n, {}))
        terms = [t for t, _ in agg.most_common(8)]
        store.db.execute("INSERT INTO communities VALUES(?,?,?,?,?)",
                         (study_id, c, ", ".join(terms[:4]), json.dumps(terms), len(group)))
    store.db.commit()
    return {"threads": len(ids), "edges": len(edges), "communities": len(members),
            "isolated": sum(1 for n in ids if g.degree(n) == 0),
            "edge_types": dict(Counter(t for (_a, _b, t) in edges))}


def label_community(store: Store, study_id: int, community: int, label: str) -> None:
    store.db.execute("UPDATE communities SET label=? WHERE study_id=? AND community=?", (label, study_id, community))
    store.db.commit()


# ---------------------------------------------------------------------- read
def overview(store: Store, study_id: int, per_community: int = 4) -> dict:
    comms = []
    for c in store.q("SELECT * FROM communities WHERE study_id=? ORDER BY size DESC", (study_id,)):
        top = store.q("SELECT p.id, p.title, p.subreddit, p.num_comments, g.pagerank FROM graph_nodes g JOIN posts p "
                      "ON p.id=g.post_id WHERE g.study_id=? AND g.community=? ORDER BY g.pagerank DESC LIMIT ?",
                      (study_id, c["community"], per_community))
        subs = store.q("SELECT p.subreddit, COUNT(*) n FROM graph_nodes g JOIN posts p ON p.id=g.post_id WHERE "
                       "g.study_id=? AND g.community=? GROUP BY p.subreddit ORDER BY n DESC LIMIT 4",
                       (study_id, c["community"]))
        comms.append({"community": c["community"], "label": c["label"], "size": c["size"],
                      "key_terms": json.loads(c["terms"]), "subreddits": {s["subreddit"]: s["n"] for s in subs},
                      "hub_threads": [dict(t) for t in top]})
    bridges = store.q("SELECT p.id, p.title, p.subreddit, g.betweenness, g.community FROM graph_nodes g JOIN posts p "
                      "ON p.id=g.post_id WHERE g.study_id=? AND g.betweenness>0 ORDER BY g.betweenness DESC LIMIT 6",
                      (study_id,))
    edge_types = store.q("SELECT type, COUNT(*) n FROM edges WHERE study_id=? GROUP BY type ORDER BY n DESC", (study_id,))
    subs = store.q("SELECT p.subreddit, COUNT(*) n, SUM(p.fetched_comments) c FROM study_posts sp JOIN posts p ON "
                   "p.id=sp.post_id WHERE sp.study_id=? AND sp.status='fetched' GROUP BY p.subreddit ORDER BY n DESC "
                   "LIMIT 12", (study_id,))
    return {"communities": comms, "bridge_threads": [dict(b) for b in bridges],
            "edge_types": {e["type"]: e["n"] for e in edge_types},
            "subreddits": [dict(s) for s in subs]}


def neighbors(store: Store, study_id: int, post_id: str, limit: int = 15) -> list[dict]:
    rows = store.q("SELECT src, dst, type, weight, evidence FROM edges WHERE study_id=? AND (src=? OR dst=?)",
                   (study_id, post_id, post_id))
    agg: dict[str, dict] = {}
    for r in rows:
        other = r["dst"] if r["src"] == post_id else r["src"]
        a = agg.setdefault(other, {"id": other, "weight": 0.0, "connections": []})
        a["weight"] += r["weight"]
        a["connections"].append(f"{r['type']} ({r['evidence']})")
    out = sorted(agg.values(), key=lambda x: -x["weight"])[:limit]
    for a in out:
        p = store.post(a["id"])
        a.update(title=p["title"], subreddit=p["subreddit"], num_comments=p["num_comments"], weight=round(a["weight"], 2))
    return out


# ---------------------------------------------------------------------- export
def to_networkx(store: Store, study_id: int) -> nx.Graph:
    g = nx.Graph()
    for r in store.q("SELECT g.*, p.title, p.subreddit, p.num_comments, p.permalink FROM graph_nodes g JOIN posts p "
                     "ON p.id=g.post_id WHERE g.study_id=?", (study_id,)):
        g.add_node(r["post_id"], label=r["title"][:80], subreddit=r["subreddit"], comments=r["num_comments"] or 0,
                   community=r["community"], pagerank=float(r["pagerank"]), url=r["permalink"])
    for r in store.q("SELECT * FROM edges WHERE study_id=?", (study_id,)):
        if g.has_edge(r["src"], r["dst"]):
            g[r["src"]][r["dst"]]["weight"] += r["weight"]
            g[r["src"]][r["dst"]]["types"] += "," + r["type"]
        else:
            g.add_edge(r["src"], r["dst"], weight=r["weight"], types=r["type"])
    return g


PALETTE = ["#2a78d6", "#e8862a", "#3aa35b", "#c8423f", "#8a5cc7", "#8c6d4f", "#d460a8", "#6b7280", "#b5a62a", "#1fa2b0"]


def to_html(store: Store, study_id: int, title: str) -> str:
    g = to_networkx(store, study_id)
    labels = {r["community"]: r["label"] for r in store.q("SELECT * FROM communities WHERE study_id=?", (study_id,))}
    max_pr = max((d["pagerank"] for _, d in g.nodes(data=True)), default=1) or 1
    nodes = [{"id": n, "label": "", "title": f"{d['label']}\nr/{d['subreddit']} · {d['comments']} comments\n"
                                             f"group: {labels.get(d['community'], 'unconnected')}",
              "value": 4 + 30 * d["pagerank"] / max_pr, "url": d["url"],
              "color": PALETTE[d["community"] % len(PALETTE)] if d["community"] >= 0 else "#c4c4c4"}
             for n, d in g.nodes(data=True)]
    edges = [{"from": a, "to": b, "value": d["weight"], "title": d["types"]} for a, b, d in g.edges(data=True)]
    legend = "".join(f'<span><i style="background:{PALETTE[c % len(PALETTE)]}"></i>{html.escape(lbl)}</span>'
                     for c, lbl in sorted(labels.items()))
    data = json.dumps({"nodes": nodes, "edges": edges}).replace("</", "<\\/")
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>body{{margin:0;font:14px system-ui,sans-serif;background:#fafafa;color:#222}}
header{{padding:10px 16px;border-bottom:1px solid #ddd;background:#fff}}h1{{font-size:16px;margin:0 0 6px}}
#legend span{{display:inline-flex;align-items:center;margin:2px 12px 2px 0;font-size:12px}}
#legend i{{width:10px;height:10px;border-radius:50%;margin-right:5px;display:inline-block}}
#net{{height:calc(100vh - 90px)}}</style></head><body>
<header><h1>{html.escape(title)}</h1><div id="legend">{legend}</div>
<small>Dot size = how central the thread is. Hover for details, click to open on Reddit.</small></header>
<div id="net"></div><script>
const data = {data};
const net = new vis.Network(document.getElementById('net'),
  {{nodes: new vis.DataSet(data.nodes), edges: new vis.DataSet(data.edges)}},
  {{nodes: {{shape: 'dot', scaling: {{min: 4, max: 34}}}}, edges: {{color: {{opacity: 0.35}}, smooth: false,
    scaling: {{min: 0.5, max: 4}}}}, physics: {{solver: 'forceAtlas2Based', stabilization: {{iterations: 250}}}},
    interaction: {{hover: true, tooltipDelay: 80}}}});
net.on('click', p => {{ if (p.nodes.length) {{ const n = data.nodes.find(x => x.id === p.nodes[0]); window.open(n.url, '_blank'); }} }});
</script></body></html>"""
