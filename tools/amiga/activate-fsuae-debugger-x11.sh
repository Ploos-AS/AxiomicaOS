#!/bin/sh
# Inject the configured debugger hotkey into the FS-UAE window on X11.
# Use direct X focus rather than EWMH activation so this also works on bare Xvfb.
set -eu
command -v xdotool >/dev/null 2>&1 || { echo "xdotool required" >&2; exit 2; }
TITLE=${AXIOMICA_FS_UAE_WINDOW:-FS-UAE}
ID=$(xdotool search --name "$TITLE" 2>/dev/null | head -n1)
[ -n "$ID" ] || { echo "FS-UAE window not found" >&2; exit 3; }
xdotool windowfocus --sync "$ID"
xdotool key --clearmodifiers --window "$ID" F10
echo "FS-UAE debugger hotkey sent to window $ID"
