#!/bin/sh
# Activate FS-UAE's documented console-debugger shortcut on X11.
# console_debugger = 1 must be enabled and FS-UAE must run from a terminal/PTY.
set -eu
command -v xdotool >/dev/null 2>&1 || { echo "xdotool required" >&2; exit 2; }
TITLE=${AXIOMICA_FS_UAE_WINDOW:-FS-UAE}
ID=$(xdotool search --name "$TITLE" 2>/dev/null | head -n1)
[ -n "$ID" ] || { echo "FS-UAE window not found" >&2; exit 3; }
xdotool windowfocus --sync "$ID"
# FS-UAE treats F12 as its modifier key; hold it while sending D.
xdotool keydown --window "$ID" F12
sleep 0.2
xdotool key --window "$ID" d
sleep 0.2
xdotool keyup --window "$ID" F12
echo "FS-UAE documented F12+D debugger shortcut sent to window $ID"
