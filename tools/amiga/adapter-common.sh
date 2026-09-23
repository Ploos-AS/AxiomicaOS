#!/bin/sh
# Shared runtime-adapter result handling.
set -eu
LOG=$1
EMU=$2
python3 tools/amiga/verify-runtime-log.py "$LOG" | tee "${LOG}.verified"
python3 tools/amiga/qualification-result.py --static --runtime-log "${LOG}.verified" --emulator "$EMU"
