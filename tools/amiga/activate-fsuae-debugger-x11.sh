#!/bin/sh
# Inject FS-UAE's debugger shortcut into the emulator window on X11.
# FS-UAE uses its modifier key (F12 by default) + D for the console debugger.
# Direct X focus keeps this working on bare Xvfb without a window manager.
set -eu
command -v xdotool >/dev/null 2>&1 || { echo "xdotool required" >&2; exit 2; }
TITLE=${AXIOMICA_FS_UAE_WINDOW:-FS-UAE}
ID=$(xdotool search --name "$TITLE" 2>/dev/null | head -n1)
[ -n "$ID" ] || { echo "FS-UAE window not found" >&2; exit 3; }
xdotool windowfocus --sync "$ID"
xdotool keydown --window "$ID" F12
xdotool key --window "$ID" d
xdotool keyup --window "$ID" F12
echo "FS-UAE debugger Mod+D sent to window $ID"
