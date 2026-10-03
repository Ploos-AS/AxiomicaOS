#!/bin/sh
set -eu

fail=0

ok() { echo "OK: $1"; }
bad() { echo "MISSING: $1" >&2; fail=1; }
need() {
  if command -v "$1" >/dev/null 2>&1; then
    ok "$1"
  else
    bad "$1"
  fi
}

echo "AxiomicaOS M0.3 runtime host preflight"
echo "-------------------------------------"

for x in fs-uae Xvfb xdotool python3 timeout m68k-linux-gnu-gcc m68k-linux-gnu-ld m68k-linux-gnu-objcopy; do
  need "$x"
done

if [ -z "${AXIOMICA_KICKSTART_ROM:-}" ]; then
  bad "AXIOMICA_KICKSTART_ROM"
elif [ ! -f "$AXIOMICA_KICKSTART_ROM" ]; then
  echo "INVALID: AXIOMICA_KICKSTART_ROM is not a regular file" >&2
  fail=1
elif [ ! -r "$AXIOMICA_KICKSTART_ROM" ]; then
  echo "UNREADABLE: AXIOMICA_KICKSTART_ROM" >&2
  fail=1
elif [ ! -s "$AXIOMICA_KICKSTART_ROM" ]; then
  echo "INVALID: AXIOMICA_KICKSTART_ROM is empty" >&2
  fail=1
else
  size=$(wc -c < "$AXIOMICA_KICKSTART_ROM" | tr -d ' ')
  case "$size" in
    262144|524288|1048576)
      ok "external ROM is readable and has a plausible size (contents/path hidden)"
      ;;
    *)
      echo "WARNING: external ROM has unusual size; FS-UAE will be authoritative" >&2
      ok "external ROM is readable (contents/path hidden)"
      ;;
  esac
fi

if [ "$fail" -ne 0 ]; then
  echo "M0.3 RUNTIME HOST NOT READY" >&2
  exit 1
fi

echo "M0.3 RUNTIME HOST READY"
