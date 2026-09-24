#!/bin/sh
# Unattended Linux/X11 qualification wrapper for the stock FS-UAE adapter.
set -eu
ADF=${1:-build/m68k-amiga/axiomicaos-amiga.adf}
ROM=${AXIOMICA_KICKSTART_ROM:-}
TIMEOUT=${AXIOMICA_RUNTIME_TIMEOUT:-30}
for x in Xvfb xdotool fs-uae timeout; do
  command -v "$x" >/dev/null 2>&1 || { echo "missing dependency: $x" >&2; exit 2; }
done
[ -f "$ADF" ] || { echo "missing ADF: $ADF" >&2; exit 3; }
[ -n "$ROM" ] && [ -f "$ROM" ] || { echo "set AXIOMICA_KICKSTART_ROM" >&2; exit 4; }

TMP=$(mktemp -d)
trap 'kill "${XVFB_PID:-}" "${EMU_PID:-}" 2>/dev/null || true; rm -rf "$TMP"' EXIT INT TERM
export DISPLAY=${AXIOMICA_DISPLAY:-:99}
Xvfb "$DISPLAY" -screen 0 1024x768x24 >"$TMP/xvfb.log" 2>&1 &
XVFB_PID=$!
sleep 1

OUT="$TMP/fsuae-debug.txt"
tools/amiga/run-fsuae-debug.sh "$ADF" "$OUT" &
EMU_PID=$!

deadline=$(( $(date +%s) + TIMEOUT ))
while [ $(date +%s) -lt "$deadline" ]; do
  if xdotool search --name "${AXIOMICA_FS_UAE_WINDOW:-FS-UAE}" >/dev/null 2>&1; then
    tools/amiga/activate-fsuae-debugger-x11.sh && break
  fi
  kill -0 "$EMU_PID" 2>/dev/null || { echo "FS-UAE exited before debugger activation" >&2; exit 5; }
  sleep 1
done

if [ $(date +%s) -ge "$deadline" ]; then
  echo "runtime timeout waiting for FS-UAE window/debugger" >&2
  exit 6
fi

# The emulator is a child of this shell. Poll it with a hard deadline rather
# than trying to wait from a nested shell, which cannot reap our child.
end=$(( $(date +%s) + TIMEOUT ))
while kill -0 "$EMU_PID" 2>/dev/null && [ $(date +%s) -lt "$end" ]; do
  sleep 1
done
if kill -0 "$EMU_PID" 2>/dev/null; then
  echo "runtime timeout" >&2
  kill "$EMU_PID" 2>/dev/null || true
  wait "$EMU_PID" 2>/dev/null || true
  exit 7
fi
wait "$EMU_PID"
