#!/usr/bin/env bash
# macOS / Linux installer for reddit-research. Run from this folder:  bash install.sh
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv (free Python installer from Astral)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "Installing the rr command..."
uv tool install --force --python 3.12 "$here"
uv tool update-shell >/dev/null || true
export PATH="$HOME/.local/bin:$PATH"

if ! { [ -d "/Applications/Google Chrome.app" ] || command -v google-chrome >/dev/null 2>&1; }; then
  echo "Google Chrome not found; downloading a private Chromium for the tool..."
  rr setup-browser
  rr set browser_channel chromium
fi

if command -v claude >/dev/null 2>&1; then
  echo "Registering the MCP server with Claude Code (all projects)..."
  claude mcp remove reddit-research --scope user >/dev/null 2>&1 || true
  claude mcp add reddit-research --scope user -- rr serve
  mkdir -p "$HOME/.claude/skills/reddit-research"
  cp "$here/.claude/skills/reddit-research/SKILL.md" "$HOME/.claude/skills/reddit-research/"
  echo "Installed the research playbook skill."
else
  echo "Claude Code CLI not found. See README.md for Claude Desktop setup."
fi

echo
echo "Next: sign the tool's browser into Reddit (one time):  rr login"
echo "Then check everything:                                rr doctor"
