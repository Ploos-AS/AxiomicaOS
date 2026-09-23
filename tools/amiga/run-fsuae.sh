#!/bin/sh
set -eu
ADF=${1:-build/m68k-amiga/axiomicaos-amiga.adf}
ROM=${AXIOMICA_KICKSTART_ROM:-}
[ -f "$ADF" ] || { echo "missing ADF: $ADF" >&2; exit 2; }
[ -n "$ROM" ] && [ -f "$ROM" ] || { echo "Set AXIOMICA_KICKSTART_ROM to a legal local A500-compatible ROM." >&2; exit 3; }
command -v fs-uae >/dev/null 2>&1 || { echo "fs-uae not found" >&2; exit 4; }
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT INT TERM
sed "s|@AXIOMICA_ADF@|$ADF|" tools/amiga/fs-uae.conf > "$TMP/axiomica.conf"
printf '\nkickstart_file = %s\n' "$ROM" >> "$TMP/axiomica.conf"
echo "M0.3 oracle: dark blue=stage0, red=fail, green=kernel, blue=halt"
exec fs-uae "$TMP/axiomica.conf"
