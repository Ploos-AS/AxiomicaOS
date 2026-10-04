#!/bin/sh
# Activate FS-UAE's documented Mod+D console-debugger shortcut on Linux.
# The default Mod key is Alt on non-macOS platforms.
set -eu
command -v xdotool >/dev/null 2>&1 || { echo "xdotool required" >&2; exit 2; }
TITLE=${AXIOMICA_FS_UAE_WINDOW:-FS-UAE}
ID=$(xdotool search --name "$TITLE" 2>/dev/null | head -n1)
[ -n "$ID" ] || { echo "FS-UAE window not found" >&2; exit 3; }
xdotool windowfocus --sync "$ID"
xdotool keydown --window "$ID" Alt_L
sleep 0.2
xdotool key --window "$ID" d
sleep 0.2
xdotool keyup --window "$ID" Alt_L
echo "FS-UAE documented Alt+D debugger shortcut sent to window $ID"
