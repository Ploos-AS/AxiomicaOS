#!/bin/sh
# Shared runtime-adapter result handling.
set -eu
LOG=$1
EMU=$2
VERIFIED="${LOG}.verified"
RESULT="${LOG%.*}.qualification.json"

python3 tools/amiga/verify-runtime-log.py "$LOG" | tee "$VERIFIED"
python3 tools/amiga/qualification-result.py \
  --static \
  --runtime-log "$VERIFIED" \
  --emulator "$EMU" > "$RESULT"
cat "$RESULT"
