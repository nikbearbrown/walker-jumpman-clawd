#!/bin/zsh
# Professor Bear's independent Clawd iteration; the starter is unchanged.
set -eu
WALKER_GAME_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
WALKER_ENGINE="/Applications/Godot.app/Contents/MacOS/Godot"
if [[ ! -x "$WALKER_ENGINE" ]]; then
  WALKER_ENGINE="$(command -v godot || true)"
fi
if [[ -z "$WALKER_ENGINE" || ! -x "$WALKER_ENGINE" ]]; then
  printf 'Godot was not found. Install the regular Godot 4 engine in Applications.\n'
  exit 1
fi
exec "$WALKER_ENGINE" --path "$WALKER_GAME_DIR/godot"
