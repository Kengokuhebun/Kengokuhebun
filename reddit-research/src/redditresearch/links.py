"""Find links inside posts and comments: other Reddit threads, product pages, brand sites."""

from __future__ import annotations

import re
from urllib.parse import urlparse

REDDIT_THREAD_RE = re.compile(
    r"(?:https?://)?(?:(?:www|old|new|np|m|i)\.)?reddit\.com/(?:r/[A-Za-z0-9_]+/)?comments/([a-z0-9]{4,16})"
    r"(?:/[^/\s)\]>]*/?([a-z0-9]{4,16})?)?",
    re.IGNORECASE,
)
REDD_IT_RE = re.compile(r"(?:https?://)?redd\.it/([a-z0-9]{4,16})", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)\]>\"'<]+", re.IGNORECASE)
ASIN_RE = re.compile(r"/(?:dp|gp/product|gp/aw/d|product)/([A-Z0-9]{10})(?:[/?]|$)", re.IGNORECASE)

# Domains that say nothing about a product or brand when two threads share them.
GENERIC_DOMAINS = {
    "reddit.com", "redd.it", "redditmedia.com", "redditstatic.com", "imgur.com", "i.imgur.com", "giphy.com",
    "youtube.com", "youtu.be", "google.com", "goo.gl", "bit.ly", "t.co", "x.com", "twitter.com",
    "facebook.com", "instagram.com", "tiktok.com", "wikipedia.org", "en.wikipedia.org", "amazon.com",
    "amzn.to", "a.co", "ncbi.nlm.nih.gov", "pubmed.ncbi.nlm.nih.gov", "nih.gov", "mayoclinic.org",
    "webmd.com", "healthline.com", "clevelandclinic.org", "medium.com", "substack.com", "github.com",
    "preview.redd.it", "i.redd.it", "v.redd.it", "archive.org", "web.archive.org", "pinterest.com",
}


def domain_of(url: str) -> str:
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def product_key(url: str) -> str | None:
    """A stable key for 'the same product' across threads, or None if the URL isn't product-like."""
    dom = domain_of(url)
    if not dom:
        return None
    path = urlparse(url).path
    if "amazon." in dom:
        m = ASIN_RE.search(path + "/")
        return f"amazon:{m.group(1).upper()}" if m else None
    m = re.search(r"/products/([A-Za-z0-9\-_.]+)", path)  # Shopify-style stores
    if m:
        return f"shop:{dom}/{m.group(1).lower()}"
    if dom in ("youtube.com", "youtu.be"):
        vid = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", url)
        return f"youtube:{vid.group(1)}" if vid else None
    return None


def brand_domain(url: str) -> str | None:
    dom = domain_of(url)
    if not dom or dom in GENERIC_DOMAINS or any(dom.endswith("." + g) for g in GENERIC_DOMAINS):
        return None
    if "reddit" in dom or "redd.it" in dom or "amazon." in dom:
        return None
    return dom


def extract(text: str | None) -> list[dict]:
    """All links in a chunk of markdown/plain text, classified."""
    if not text:
        return []
    found: dict[tuple, dict] = {}
    for m in REDDIT_THREAD_RE.finditer(text):
        post_id = m.group(1).lower()
        found[("reddit", post_id)] = {"kind": "reddit_thread", "target_post_id": post_id, "url": m.group(0)}
    for m in REDD_IT_RE.finditer(text):
        post_id = m.group(1).lower()
        found[("reddit", post_id)] = {"kind": "reddit_thread", "target_post_id": post_id, "url": m.group(0)}
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip(".,;:!?*")
        dom = domain_of(url)
        if not dom or "reddit.com" in dom or dom == "redd.it":
            continue
        found[("url", url)] = {
            "kind": "external",
            "url": url,
            "domain": dom,
            "product_key": product_key(url),
            "brand_domain": brand_domain(url),
        }
    return list(found.values())
