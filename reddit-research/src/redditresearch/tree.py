"""Turn Reddit-shaped comment listings (Reddit JSON and Arctic Shift share the format) into flat rows.

A listing mixes real comments (kind "t1") with two kinds of "more" stubs:
  * load-more stubs: kind "more" with a non-empty `children` id list -> /api/morechildren
  * continue-this-thread stubs: kind "more" with empty `children` -> re-fetch the subtree under parent_id
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .util import strip_prefix


@dataclass
class Parsed:
    comments: list[dict] = field(default_factory=list)
    more_ids: list[str] = field(default_factory=list)
    continue_parents: list[str] = field(default_factory=list)


def comment_row(data: dict, post_id: str) -> dict:
    cid = data.get("id") or strip_prefix(data.get("name"))
    permalink = data.get("permalink") or f"/comments/{post_id}/_/{cid}/"
    return {
        "id": cid,
        "post_id": post_id,
        "parent_id": data.get("parent_id"),  # fullname: t3_<post> for top level, t1_<comment> otherwise
        "author": data.get("author") or "[deleted]",
        "score": _int(data.get("score")),
        "body": data.get("body") or "",
        "created_utc": _int(data.get("created_utc")),
        "is_submitter": 1 if data.get("is_submitter") else 0,
        "controversiality": _int(data.get("controversiality")),
        "permalink": "https://www.reddit.com" + permalink if permalink.startswith("/") else permalink,
    }


def flatten(children: list, post_id: str, seen: set[str], out: Parsed | None = None) -> Parsed:
    """Walk a listing (nested `replies` or flat morechildren output). Skips ids already in `seen`."""
    out = out or Parsed()
    for child in children or []:
        kind = child.get("kind")
        data = child.get("data") or {}
        if kind == "more":
            ids = [i for i in (data.get("children") or []) if i and i not in seen]
            if ids:
                out.more_ids.extend(ids)
            elif data.get("parent_id", "").startswith("t1_"):
                out.continue_parents.append(strip_prefix(data["parent_id"]))
            continue
        if kind != "t1":
            continue
        row = comment_row(data, post_id)
        if row["id"] and row["id"] not in seen:
            seen.add(row["id"])
            out.comments.append(row)
        replies = data.get("replies")
        if isinstance(replies, dict):
            flatten((replies.get("data") or {}).get("children") or [], post_id, seen, out)
    return out


def assign_paths(comments: list[dict], post_id: str) -> None:
    """Compute depth and a sortable materialized path from parent links (robust across fetch batches)."""
    by_id = {c["id"]: c for c in comments}
    cache: dict[str, tuple[str, int]] = {}

    def resolve(cid: str, guard: int = 0) -> tuple[str, int]:
        if cid in cache:
            return cache[cid]
        c = by_id[cid]
        parent = c.get("parent_id") or f"t3_{post_id}"
        pid = strip_prefix(parent)
        if parent.startswith("t1_") and pid in by_id and guard < 500:
            ppath, pdepth = resolve(pid, guard + 1)
            result = (f"{ppath}/{cid}", pdepth + 1)
        else:
            # Top-level, or orphan whose parent we never saw: treat as a root.
            result = (cid, 0)
        cache[cid] = result
        return result

    for c in comments:
        c["path"], c["depth"] = resolve(c["id"])


def _int(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
