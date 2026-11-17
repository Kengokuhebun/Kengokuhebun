"""A fake Reddit that behaves like the real JSON API, including 'more' and 'continue this thread' stubs."""

from __future__ import annotations

from redditresearch.sources.base import Source, SourceError


def c(cid, body, parent, author="user", score=1, replies=None, op=False):
    return {"kind": "t1", "data": {
        "id": cid, "name": f"t1_{cid}", "body": body, "parent_id": parent, "author": author, "score": score,
        "created_utc": 1_760_000_000, "is_submitter": op, "permalink": f"/r/test/comments/x/_/{cid}/",
        "replies": {"kind": "Listing", "data": {"children": replies}} if replies else ""}}


def more(ids, parent, count=None):
    return {"kind": "more", "data": {"children": ids, "parent_id": parent, "count": count or len(ids), "id": ids[0] if ids else "_"}}


def post(pid, title, selftext="", sub="beyondthebump", num_comments=10, url=None, score=50):
    return {"id": pid, "name": f"t3_{pid}", "title": title, "selftext": selftext, "subreddit": sub,
            "num_comments": num_comments, "score": score, "author": "op_" + pid, "created_utc": 1_760_000_000,
            "permalink": f"/r/{sub}/comments/{pid}/slug/", "url": url or f"https://www.reddit.com/r/{sub}/comments/{pid}/slug/",
            "is_self": url is None}


class FakeReddit(Source):
    name = "fake"

    def __init__(self):
        self.calls: list[tuple] = []
        # Thread aaa111: has a 'load more' stub and a 'continue this thread' stub, links to bbb222.
        self.posts = {
            "aaa111": post("aaa111", "Postpartum hair loss is making me panic", "Clumps in the shower drain at 4 months pp",
                           num_comments=7),
            "bbb222": post("bbb222", "Rosemary oil for postpartum shedding?", "Has anyone tried rosemary oil or biotin?",
                           num_comments=3),
            "ccc333": post("ccc333", "Best stroller for city living", "Looking for a compact stroller", num_comments=2),
            "ddd444": post("ddd444", "Minoxidil after pregnancy hair loss", "Scared of the dread shed", sub="FemaleHairLoss",
                           num_comments=2),
        }
        self.trees = {
            "aaa111": [
                c("c1", "I tried biotin for three months and it did absolutely nothing for my shedding.", "t3_aaa111",
                  "alice", 40, replies=[
                      c("c2", "Same here, biotin just gave me acne.", "t1_c1", "bob", 12, replies=[
                          more([], "t1_c2"),  # continue this thread -> subtree(aaa111, c2)
                      ]),
                  ]),
                c("c3", "This thread helped me a lot: https://www.reddit.com/r/beyondthebump/comments/bbb222/rosemary/",
                  "t3_aaa111", "carol", 25),
                more(["c4", "c5"], "t3_aaa111"),
            ],
            "bbb222": [
                c("c10", "Rosemary oil is so messy, it gets everywhere and I never know if it reaches my scalp.",
                  "t3_bbb222", "alice", 30),
                c("c11", "I bought this dropper bottle https://www.amazon.com/dp/B0ABCDEF12 and it helped.",
                  "t3_bbb222", "bob", 8),
                c("c12", "Biotin did nothing for me either, and my shedding kept going.", "t3_bbb222", "dave", 5),
            ],
            "ccc333": [c("c20", "Get the lightest one you can fold with one hand.", "t3_ccc333", "erin", 3)],
            "ddd444": [
                c("c30", "Minoxidil terrified me because of the dread shed.", "t3_ddd444", "alice", 9),
                c("c31", "Same dropper https://www.amazon.com/dp/B0ABCDEF12 works for minoxidil too", "t3_ddd444", "bob", 4),
            ],
        }
        self.more = {
            "c4": c("c4", "Collagen powder was a waste of money for me.", "t3_aaa111", "frank", 7),
            "c5": c("c5", "Mine grew back around 9 months, it does get better.", "t3_aaa111", "gina", 15),
        }
        self.sub = {("aaa111", "c2"): [c("c2", "Same here, biotin just gave me acne.", "t1_c1", "bob", 12, replies=[
            c("c6", "The 2am shower panic is real, I cried looking at the drain.", "t1_c2", "hana", 6)])]}

    async def thread(self, post_id):
        self.calls.append(("thread", post_id))
        if post_id not in self.posts:
            raise SourceError("not found")
        return self.posts[post_id], self.trees[post_id]

    async def more_children(self, post_id, ids):
        self.calls.append(("more", post_id, tuple(ids)))
        return [self.more[i] for i in ids if i in self.more]  # flat, like /api/morechildren

    async def subtree(self, post_id, comment_id):
        self.calls.append(("subtree", post_id, comment_id))
        return self.sub.get((post_id, comment_id), [])

    async def search(self, query, subreddit=None, sort="relevance", time_range="all", limit=100):
        self.calls.append(("search", query, subreddit))
        words = query.lower().split()
        return [p for p in self.posts.values()
                if any(w in (p["title"] + " " + p["selftext"]).lower() for w in words)
                and (subreddit is None or p["subreddit"].lower() == subreddit.lower())][:limit]

    async def listing(self, subreddit, sort="top", time_range="year", limit=100):
        return [p for p in self.posts.values() if p["subreddit"] == subreddit][:limit]

    async def info(self, post_ids):
        self.calls.append(("info", tuple(post_ids)))
        return [self.posts[p] for p in post_ids if p in self.posts]

    async def posts_with_url(self, url):
        return []

    async def crossposts(self, post_id):
        return []

    async def find_subreddits(self, query, limit=15):
        return [{"name": "beyondthebump", "subscribers": 1, "description": ""}]
