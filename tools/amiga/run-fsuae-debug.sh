#!/bin/sh
# Launch stock FS-UAE with debugger stdin/stdout attached to named FIFOs.
# Activation of Mod+D is still external; once activated, commands are fed via stdin.
set -eu
ADF=${1:-build/m68k-amiga/axiomicaos-amiga.adf}
ROM=${AXIOMICA_KICKSTART_ROM:-}
OUT=${2:-build/m68k-amiga/fsuae-debug.txt}
[ -f "$ADF" ] || { echo "missing ADF: $ADF" >&2; exit 2; }
[ -n "$ROM" ] && [ -f "$ROM" ] || { echo "set AXIOMICA_KICKSTART_ROM" >&2; exit 3; }
command -v fs-uae >/dev/null 2>&1 || { echo "fs-uae not found" >&2; exit 4; }
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT INT TERM
sed "s|@AXIOMICA_ADF@|$ADF|" tools/amiga/fs-uae.conf > "$TMP/run.conf"
printf '\nkickstart_file = %s\n' "$ROM" >> "$TMP/run.conf"
mkfifo "$TMP/in"
# Open the FIFO read/write in this shell. Opening a write-only FIFO before a
# reader exists can block forever, which previously made unattended CI hang.
exec 3<>"$TMP/in"
fs-uae --stdout "$TMP/run.conf" <"$TMP/in" >"$OUT" 2>&1 &
PID=$!
echo "FS-UAE pid=$PID; activate console debugger with Mod+D."
sleep "${AXIOMICA_DEBUG_DELAY:-8}"
if ! printf 'm bfe001 1\nm dff180 1\nm bfe001 1\nm dff180 1\nq\n' >&3; then
  echo "failed to send debugger oracle commands to FS-UAE" >&2
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  exit 5
fi
set +e
wait "$PID"
status=$?
set -e
if [ "$status" -ne 0 ]; then
  exec 3>&-
  echo "FS-UAE exited unsuccessfully: $status" >&2
  exit "$status"
fi
exec 3>&-
python3 tools/amiga/fsuae-debugger-adapter.py "$OUT" "${OUT%.txt}.trace"
sh tools/amiga/adapter-common.sh "${OUT%.txt}.trace" fs-uae
