#!/bin/sh
set -eu
fail=0
need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1" >&2; fail=1; }; }
for x in fs-uae Xvfb xdotool python3 timeout m68k-linux-gnu-gcc m68k-linux-gnu-ld m68k-linux-gnu-objcopy; do need "$x"; done
if [ -z "${AXIOMICA_KICKSTART_ROM:-}" ]; then
  echo "MISSING: AXIOMICA_KICKSTART_ROM" >&2; fail=1
elif [ ! -r "$AXIOMICA_KICKSTART_ROM" ]; then
  echo "UNREADABLE: AXIOMICA_KICKSTART_ROM" >&2; fail=1
else
  echo "OK: external ROM is readable (path and contents intentionally not printed)"
fi
[ "$fail" -eq 0 ] || exit 1
echo "M0.3 RUNTIME HOST READY"
