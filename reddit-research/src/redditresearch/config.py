"""Paths and user settings. Everything lives in one folder (default ~/.reddit-research)."""

from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULTS = {
    # "auto": your logged-in browser profile if you've run `rr login`, else Arctic Shift.
    # "reddit": browser profile only. "arctic": Arctic Shift archive only.
    "source": "auto",
    "reddit_min_interval": 1.5,  # seconds between Reddit requests (~40/min, well under limits)
    "arctic_min_interval": 1.5,
    "headless": True,
    "browser_channel": "chrome",  # use your installed Chrome; falls back to Playwright's Chromium
}


def home() -> Path:
    path = Path(os.environ.get("RR_HOME", Path.home() / ".reddit-research"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def db_path() -> Path:
    return Path(os.environ.get("RR_DB", home() / "research.db"))


def profile_dir() -> Path:
    return home() / "browser-profile"


def export_dir() -> Path:
    path = home() / "exports"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _settings_file() -> Path:
    return home() / "settings.json"


def load_settings() -> dict:
    settings = dict(DEFAULTS)
    try:
        settings.update(json.loads(_settings_file().read_text(encoding="utf-8")))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return settings


def save_setting(key: str, value) -> dict:
    if key not in DEFAULTS:
        raise KeyError(f"Unknown setting {key!r}. Known: {', '.join(DEFAULTS)}")
    settings = load_settings()
    settings[key] = value
    stored = {k: v for k, v in settings.items() if DEFAULTS.get(k) != v}
    _settings_file().write_text(json.dumps(stored, indent=2), encoding="utf-8")
    return settings
