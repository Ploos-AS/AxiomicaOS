#!/bin/sh
# Activate FS-UAE's documented Mod+D console-debugger shortcut on Linux.
# The default Mod key is Alt on non-macOS platforms. FS-UAE may replace its
# X11 window while booting, so never rely on a stale window id.
set -eu
command -v xdotool >/dev/null 2>&1 || { echo "xdotool required" >&2; exit 2; }
TITLE=${AXIOMICA_FS_UAE_WINDOW:-FS-UAE}
TRIES=${AXIOMICA_FS_UAE_FOCUS_TRIES:-10}

find_window() {
    xdotool search --name "$TITLE" 2>/dev/null | tail -n1
}

i=0
while [ "$i" -lt "$TRIES" ]; do
    i=$((i + 1))
    ID=$(find_window)
    if [ -n "$ID" ] &&
       xdotool windowfocus --sync "$ID" 2>/dev/null &&
       xdotool key --window "$ID" Alt_L+d 2>/dev/null; then
        echo "FS-UAE documented Alt+D debugger shortcut sent to window $ID (attempt $i)"
        exit 0
    fi
    sleep 0.5
done

echo "unable to activate FS-UAE debugger after $TRIES fresh-window attempts" >&2
exit 3
