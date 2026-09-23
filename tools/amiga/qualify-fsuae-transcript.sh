#!/bin/sh
set -eu
TRANSCRIPT=${1:?usage: qualify-fsuae-transcript.sh <debugger-transcript>}
TRACE=${2:-build/m68k-amiga/fsuae-runtime.trace}
mkdir -p "$(dirname "$TRACE")"
python3 tools/amiga/fsuae-debugger-adapter.py "$TRANSCRIPT" "$TRACE"
sh tools/amiga/adapter-common.sh "$TRACE" fs-uae
