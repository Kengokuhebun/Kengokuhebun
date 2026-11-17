"""Pick a data source from settings."""

from __future__ import annotations

from .. import config
from .arctic import ArcticShiftSource
from .base import BlockedError, FallbackSource, Source, SourceError


def build_source(settings: dict | None = None) -> Source:
    settings = settings or config.load_settings()
    choice = settings.get("source", "auto")
    arctic = ArcticShiftSource(min_interval=settings["arctic_min_interval"])
    if choice == "arctic":
        return arctic
    profile = config.profile_dir()
    if choice == "auto" and not (profile / "Default").exists() and not (profile / "Local State").exists():
        return arctic  # never logged in -> archive only
    try:
        from .reddit_browser import RedditBrowserSource
    except ImportError:
        return arctic
    reddit = RedditBrowserSource(profile, headless=settings["headless"], channel=settings["browser_channel"],
                                 min_interval=settings["reddit_min_interval"])
    return reddit if choice == "reddit" else FallbackSource(reddit, arctic)


__all__ = ["build_source", "Source", "SourceError", "BlockedError", "FallbackSource", "ArcticShiftSource"]
