#!/usr/bin/env bash
# Installs Ads Launcher as a desktop app on Linux.
#  - installs Node.js 22 for your user if you don't have Node 20+ (no sudo)
#  - builds the app
#  - asks for your Meta token once and saves it in .env.local (only you can read it)
#  - adds an "Ads Launcher" icon to your app menu and desktop
#
# Run from anywhere:  bash path/to/ads-launcher/scripts/install-linux.sh
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${ADS_LAUNCHER_PORT:-3737}"
BIN_DIR="$HOME/.local/bin"
APPS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/ads-launcher"
LAUNCHER="$BIN_DIR/ads-launcher"

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }

# 1. Node.js -------------------------------------------------------------------
need_node=1
if command -v node >/dev/null; then
  major="$(node -p 'process.versions.node.split(".")[0]')"
  [ "$major" -ge 20 ] && need_node=0
fi
if [ "$need_node" = 1 ]; then
  say "Installing Node.js 22 for your user (via nvm, no sudo needed)"
  export NVM_DIR="$HOME/.nvm"
  if [ ! -s "$NVM_DIR/nvm.sh" ]; then
    command -v curl >/dev/null || { echo "Please install curl first: sudo apt install -y curl"; exit 1; }
    curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  fi
  set +u # nvm is not compatible with "set -u"
  # shellcheck disable=SC1091
  . "$NVM_DIR/nvm.sh"
  nvm install 22
  nvm use 22 >/dev/null
  set -u
fi
NODE_BIN_DIR="$(dirname "$(command -v node)")"
say "Using Node $(node -v) from $NODE_BIN_DIR"

# 2. Build -----------------------------------------------------------------------
say "Installing dependencies and building (takes a minute or two)"
cd "$APP_DIR"
npm ci --no-audit --no-fund
npm run build

# 3. Meta token --------------------------------------------------------------------
if [ ! -f "$APP_DIR/.env.local" ]; then
  cp "$APP_DIR/.env.example" "$APP_DIR/.env.local"
  chmod 600 "$APP_DIR/.env.local"
  if [ -t 0 ]; then
    say "Paste your Meta System User token (nothing shows while you paste), then press Enter."
    echo "    Leave it empty to add it later in $APP_DIR/.env.local"
    read -r -s TOKEN || TOKEN=""
    echo
    if [ -n "$TOKEN" ]; then
      # Write without echoing the token anywhere else.
      awk -v t="$TOKEN" '/^META_ACCESS_TOKEN=/{print "META_ACCESS_TOKEN=" t; next} {print}' \
        "$APP_DIR/.env.local" > "$APP_DIR/.env.local.tmp" && mv "$APP_DIR/.env.local.tmp" "$APP_DIR/.env.local"
      chmod 600 "$APP_DIR/.env.local"
      echo "    Saved."
    fi
    unset TOKEN
  fi
else
  say "Keeping your existing .env.local"
fi

# 4. Launcher command ----------------------------------------------------------
mkdir -p "$BIN_DIR" "$APPS_DIR" "$STATE_DIR"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
# Ads Launcher: starts the local server if needed, then opens the browser.
#   ads-launcher          open the app
#   ads-launcher stop     stop the background server
#   ads-launcher update   pull the latest version and rebuild
#   ads-launcher log      show the server log
APP_DIR="$APP_DIR"
PORT="$PORT"
STATE_DIR="$STATE_DIR"
export PATH="$NODE_BIN_DIR:\$PATH"
URL="http://localhost:\$PORT"

up() { (exec 3<>"/dev/tcp/127.0.0.1/\$PORT") 2>/dev/null; }
stop() {
  if [ -f "\$STATE_DIR/server.pid" ]; then kill "\$(cat "\$STATE_DIR/server.pid")" 2>/dev/null || true; rm -f "\$STATE_DIR/server.pid"; fi
}

case "\${1:-open}" in
  stop) stop; echo "Stopped."; exit 0 ;;
  log) tail -n 100 "\$STATE_DIR/server.log"; exit 0 ;;
  update)
    stop
    cd "\$APP_DIR" && git pull --ff-only && npm ci --no-audit --no-fund && npm run build && echo "Updated." ; exit \$? ;;
esac

if ! up; then
  cd "\$APP_DIR" || exit 1
  # Listen on this computer only, never on the network.
  nohup "$NODE_BIN_DIR/node" node_modules/next/dist/bin/next start -p "\$PORT" -H 127.0.0.1 >> "\$STATE_DIR/server.log" 2>&1 &
  echo \$! > "\$STATE_DIR/server.pid"
  for _ in \$(seq 1 60); do up && break; sleep 0.5; done
fi

if command -v xdg-open >/dev/null; then xdg-open "\$URL" >/dev/null 2>&1 &
else echo "Open \$URL in your browser"; fi
EOF
chmod +x "$LAUNCHER"

# 5. Menu and desktop icon -------------------------------------------------------
cp "$APP_DIR/scripts/icon.svg" "$STATE_DIR/icon.svg"
DESKTOP_FILE="$APPS_DIR/ads-launcher.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Ads Launcher
Comment=Bulk-launch Meta ads (everything created paused)
Exec=$LAUNCHER
Icon=$STATE_DIR/icon.svg
Terminal=false
Categories=Office;Network;
EOF
chmod +x "$DESKTOP_FILE"
command -v update-desktop-database >/dev/null && update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true

DESKTOP_DIR="$(command -v xdg-user-dir >/dev/null && xdg-user-dir DESKTOP || echo "$HOME/Desktop")"
if [ -d "$DESKTOP_DIR" ]; then
  cp "$DESKTOP_FILE" "$DESKTOP_DIR/ads-launcher.desktop"
  chmod +x "$DESKTOP_DIR/ads-launcher.desktop"
  # GNOME: mark the desktop icon as trusted so it opens on double-click.
  command -v gio >/dev/null && gio set "$DESKTOP_DIR/ads-launcher.desktop" metadata::trusted true 2>/dev/null || true
fi

say "Done"
echo "  Click 'Ads Launcher' in your app menu or on your desktop."
echo "  Or run: $LAUNCHER"
echo "  The app runs only on this computer, at http://localhost:$PORT"
echo "  Your token is in $APP_DIR/.env.local (only your user can read it)."
case ":$PATH:" in *":$BIN_DIR:"*) ;; *) echo "  Tip: add $BIN_DIR to your PATH to type 'ads-launcher' in a terminal.";; esac
