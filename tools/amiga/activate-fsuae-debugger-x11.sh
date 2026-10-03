#!/bin/sh
# Activate the FS-UAE console debugger through the explicit input mapping in
# fs-uae.conf: keyboard_key_f10 = action_debugger.
# Direct X focus keeps this working on bare Xvfb without a window manager.
set -eu
command -v xdotool >/dev/null 2>&1 || { echo "xdotool required" >&2; exit 2; }
TITLE=${AXIOMICA_FS_UAE_WINDOW:-FS-UAE}
ID=$(xdotool search --name "$TITLE" 2>/dev/null | head -n1)
[ -n "$ID" ] || { echo "FS-UAE window not found" >&2; exit 3; }
xdotool windowfocus --sync "$ID"
xdotool key --clearmodifiers --window "$ID" F10
echo "FS-UAE mapped action_debugger key sent to window $ID"
