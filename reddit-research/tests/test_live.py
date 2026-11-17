"""Hits the real Arctic Shift archive. Run with: pytest -m live"""

import asyncio

import pytest

from redditresearch.fetcher import fetch_full_thread
from redditresearch.sources.arctic import ArcticShiftSource
from redditresearch.store import Store


@pytest.mark.live
def test_arctic_full_thread(tmp_path):
    async def go():
        src = ArcticShiftSource()
        try:
            return await fetch_full_thread(src, "1w4szr6")
        finally:
            await src.close()

    post, comments, stats = asyncio.run(go())
    store = Store(tmp_path / "live.db")
    saved = store.save_thread(post, comments, "arctic")
    assert saved["comments"] > 500 and saved["coverage"] > 0.9
    assert all(c["path"] for c in comments)
