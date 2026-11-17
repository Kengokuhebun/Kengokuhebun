"""The interface every data source implements. All methods return Reddit-shaped dicts."""

from __future__ import annotations


class SourceError(RuntimeError):
    """A request failed in a way the caller may route around (e.g. try another source)."""


class BlockedError(SourceError):
    """The source refused us (403 / login required)."""


class PartialResult(SourceError):
    """Got some of what was asked; `missing` lists ids another source could still fill."""

    def __init__(self, message: str, things: list, missing: list[str]):
        super().__init__(message)
        self.things, self.missing = things, missing


class Source:
    name = "base"

    async def start(self) -> None: ...

    async def close(self) -> None: ...

    async def thread(self, post_id: str) -> tuple[dict, list]:
        """Return (post data, top-level comment listing children)."""
        raise NotImplementedError

    async def more_children(self, post_id: str, ids: list[str]) -> list:
        """Expand a 'load more comments' stub. Returns listing children (flat or nested)."""
        raise NotImplementedError

    async def subtree(self, post_id: str, comment_id: str) -> list:
        """Expand a 'continue this thread' stub: the comment and everything under it."""
        raise NotImplementedError

    async def search(self, query: str, subreddit: str | None = None, sort: str = "relevance",
                     time_range: str = "all", limit: int = 100) -> list[dict]:
        raise NotImplementedError

    async def listing(self, subreddit: str, sort: str = "top", time_range: str = "year", limit: int = 100) -> list[dict]:
        raise NotImplementedError

    async def info(self, post_ids: list[str]) -> list[dict]:
        """Metadata for up to 100 posts per call."""
        raise NotImplementedError

    async def posts_with_url(self, url: str) -> list[dict]:
        """Other submissions of the same link (Reddit's 'other discussions')."""
        raise NotImplementedError

    async def crossposts(self, post_id: str) -> list[dict]:
        return []

    async def find_subreddits(self, query: str, limit: int = 15) -> list[dict]:
        raise NotImplementedError


class FallbackSource(Source):
    """Try the primary source; on SourceError or NotImplementedError use the secondary."""

    def __init__(self, primary: Source, secondary: Source):
        self.primary, self.secondary = primary, secondary
        self.name = f"{primary.name}+{secondary.name}"
        self.notes: list[str] = []

    async def start(self) -> None:
        try:
            await self.primary.start()
        except SourceError as exc:
            self.notes.append(f"{self.primary.name} unavailable ({exc}); using {self.secondary.name}")
            await self.secondary.start()

    async def close(self) -> None:
        await self.primary.close()
        await self.secondary.close()

    def __getattr__(self, item):
        primary_fn = getattr(self.primary, item)
        secondary_fn = getattr(self.secondary, item)

        async def call(*args, **kwargs):
            try:
                return await primary_fn(*args, **kwargs)
            except PartialResult as exc:  # keep what the primary found, ask the secondary for the rest
                await self.secondary.start()
                try:
                    rest = await secondary_fn(args[0], exc.missing)
                except (SourceError, NotImplementedError):
                    rest = []
                return exc.things + rest
            except (SourceError, NotImplementedError) as exc:
                note = f"{self.primary.name}.{item} failed ({exc}); used {self.secondary.name}"
                if note not in self.notes:
                    self.notes.append(note)
                await self.secondary.start()
                return await secondary_fn(*args, **kwargs)

        return call

    # Explicit forwards so __getattr__ (which only fires for missing attributes) handles them.
    async def thread(self, *a, **k):
        return await self.__getattr__("thread")(*a, **k)

    async def more_children(self, *a, **k):
        return await self.__getattr__("more_children")(*a, **k)

    async def subtree(self, *a, **k):
        return await self.__getattr__("subtree")(*a, **k)

    async def search(self, *a, **k):
        return await self.__getattr__("search")(*a, **k)

    async def listing(self, *a, **k):
        return await self.__getattr__("listing")(*a, **k)

    async def info(self, *a, **k):
        return await self.__getattr__("info")(*a, **k)

    async def posts_with_url(self, *a, **k):
        return await self.__getattr__("posts_with_url")(*a, **k)

    async def crossposts(self, *a, **k):
        return await self.__getattr__("crossposts")(*a, **k)

    async def find_subreddits(self, *a, **k):
        return await self.__getattr__("find_subreddits")(*a, **k)
