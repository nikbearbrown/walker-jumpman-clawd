#!/bin/zsh
# Compatibility alias for links in the inherited starter documentation.
set -eu
CLAWD_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
exec "$CLAWD_DIR/walker-jumpman-clawd.command"
