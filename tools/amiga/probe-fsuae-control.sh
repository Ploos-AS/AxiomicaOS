#!/bin/sh
# Run the same FS-UAE/AROS harness against a known AROS reference ADF.
# This is a transport/boot-path control, not an AxiomicaOS qualification.
set -eu
ADF=${1:?reference ADF required}
OUT=${2:-build/m68k-amiga/aros-control-debug.txt}
AXIOMICA_DEBUG_READY_FILE= \
AXIOMICA_DEBUG_DELAY="${AXIOMICA_DEBUG_DELAY:-12}" \
sh tools/amiga/run-fsuae-debug.sh "$ADF" "$OUT" || true
test -s "$OUT" || { echo "AROS control produced no debugger transcript" >&2; exit 1; }
echo "AROS control transcript retained: $OUT"
