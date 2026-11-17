"""One shared app object (store + source + researcher), used by both the CLI and the MCP server."""

from __future__ import annotations

from . import config
from .research import Researcher
from .sources import build_source
from .store import Store


class App:
    def __init__(self, settings: dict | None = None, db_path=None):
        self.settings = settings or config.load_settings()
        self.store = Store(db_path or config.db_path())
        self._source = None
        self._researcher = None

    @property
    def source(self):
        if self._source is None:
            self._source = build_source(self.settings)
        return self._source

    @property
    def researcher(self) -> Researcher:
        if self._researcher is None:
            self._researcher = Researcher(self.store, self.source)
        return self._researcher

    async def close(self) -> None:
        if self._source is not None:
            await self._source.close()
        self.store.close()
