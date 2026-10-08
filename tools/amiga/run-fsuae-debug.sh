#!/bin/sh
# Launch stock FS-UAE with its console debugger attached to a pseudo-terminal.
# console_debugger requires FS-UAE to run from a terminal; a plain FIFO is not a TTY.
set -eu
ADF=${1:-build/m68k-amiga/axiomicaos-amiga.adf}
ROM=${AXIOMICA_KICKSTART_ROM:-}
EXT_ROM=${AXIOMICA_KICKSTART_EXT_ROM:-}
OUT=${2:-build/m68k-amiga/fsuae-debug.txt}
FIRMWARE=${AXIOMICA_RUNTIME_FIRMWARE:-kickstart}
[ -f "$ADF" ] || { echo "missing ADF: $ADF" >&2; exit 2; }
[ -n "$ROM" ] && [ -f "$ROM" ] || { echo "set AXIOMICA_KICKSTART_ROM" >&2; exit 3; }
command -v fs-uae >/dev/null 2>&1 || { echo "fs-uae not found" >&2; exit 4; }
command -v script >/dev/null 2>&1 || { echo "script(1) from util-linux required" >&2; exit 5; }

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT INT TERM
sed "s|@AXIOMICA_ADF@|$ADF|" tools/amiga/fs-uae.conf > "$TMP/run.conf"
printf '\nkickstart_file = %s\n' "$ROM" >> "$TMP/run.conf"
if [ -n "$EXT_ROM" ]; then
  [ -f "$EXT_ROM" ] || { echo "missing extended ROM: $EXT_ROM" >&2; exit 3; }
  printf 'kickstart_ext_file = %s\n' "$EXT_ROM" >> "$TMP/run.conf"
fi
mkfifo "$TMP/in"
exec 3<>"$TMP/in"

# util-linux script(1) supplies a real PTY while preserving automated stdin and
# a deterministic transcript for the debugger adapter.
script -qefc "fs-uae --stdout '$TMP/run.conf'" "$OUT" <"$TMP/in" >/dev/null 2>&1 &
PID=$!
echo "FS-UAE PTY pid=$PID; activate console debugger action."

if [ -n "${AXIOMICA_DEBUG_READY_FILE:-}" ]; then
  while [ ! -f "$AXIOMICA_DEBUG_READY_FILE" ]; do
    kill -0 "$PID" 2>/dev/null || break
    sleep 0.1
  done
else
  sleep "${AXIOMICA_DEBUG_DELAY:-12}"
fi
if ! printf 'r\nm bfe001 1\nm dff180 1\ndm\ns "AxiomicaOS" 000000 1000000\ns "AXAM" 000000 1000000\ns "AXS0" 000000 1000000\ns "AXCT" 000000 1000000\ns "AXBB" 000000 1000000\ns "AXOR" 000000 1000000\nq\n' >&3; then
  echo "failed to send debugger RAM-oracle discovery commands to FS-UAE PTY" >&2
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  exit 6
fi
set +e
wait "$PID"
status=$?
set -e
exec 3>&-
if [ "$status" -ne 0 ]; then
  echo "FS-UAE PTY exited unsuccessfully: $status" >&2
  exit "$status"
fi
python3 tools/amiga/fsuae-debugger-adapter.py "$OUT" "${OUT%.txt}.trace"
sh tools/amiga/adapter-common.sh "${OUT%.txt}.trace" fs-uae "$ADF" "$FIRMWARE"
