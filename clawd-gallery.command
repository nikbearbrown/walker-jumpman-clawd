#!/bin/zsh
set -eu
CLAWD_GAME_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
CLAWD_ENGINE="/Applications/Godot.app/Contents/MacOS/Godot"
if [[ ! -x "$CLAWD_ENGINE" ]]; then
  CLAWD_ENGINE="$(command -v godot || true)"
fi
if [[ -z "$CLAWD_ENGINE" || ! -x "$CLAWD_ENGINE" ]]; then
  printf 'Install the regular Godot 4 engine before opening this gallery.\n'
  exit 1
fi
exec "$CLAWD_ENGINE" --path "$CLAWD_GAME_DIR/godot" res://gallery/clawd_gallery.tscn
