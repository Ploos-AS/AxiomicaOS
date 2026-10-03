#!/bin/sh
# Shared runtime-adapter result handling.
set -eu
LOG=$1
EMU=$2
IMAGE=${3:-}
VERIFIED="${LOG}.verified"
RESULT="${LOG%.*}.qualification.json"

[ -n "$IMAGE" ] || { echo "qualification image argument required" >&2; exit 4; }
[ -f "$IMAGE" ] || { echo "qualification image missing: $IMAGE" >&2; exit 4; }

python3 tools/amiga/verify-runtime-log.py "$LOG" | tee "$VERIFIED"
python3 tools/amiga/qualification-result.py \
  --static \
  --runtime-log "$VERIFIED" \
  --image "$IMAGE" \
  --emulator "$EMU" > "$RESULT"
cat "$RESULT"
