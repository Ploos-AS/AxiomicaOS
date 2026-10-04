#!/usr/bin/env python3
"""Add a diagnostic marker to unused bytes of an Amiga boot block and repair checksum."""
from pathlib import Path
import argparse, struct

SIZE = 1024

def checksum(block: bytes) -> int:
    total = 0
    for off in range(0, SIZE, 4):
        value = struct.unpack_from(">I", block, off)[0]
        old = total
        total = (total + value) & 0xffffffff
        if total < old:
            total = (total + 1) & 0xffffffff
    return (~total) & 0xffffffff

p = argparse.ArgumentParser()
p.add_argument("source", type=Path)
p.add_argument("output", type=Path)
p.add_argument("--marker", default="AXCT")
args = p.parse_args()
data = bytearray(args.source.read_bytes())
marker = args.marker.encode("ascii")
boot = data[:SIZE]
# Use a zero-filled longword in the boot block so executable bytes are untouched.
slot = next((off for off in range(SIZE - len(marker), 12, -4)
             if boot[off:off+len(marker)] == b"\0" * len(marker)), None)
if slot is None:
    raise SystemExit("no zero-filled boot-block slot for marker")
boot[slot:slot+len(marker)] = marker
struct.pack_into(">I", boot, 4, 0)
struct.pack_into(">I", boot, 4, checksum(boot))
data[:SIZE] = boot
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_bytes(data)
print(f"control marker {args.marker} at boot-block offset {slot}, checksum=0x{struct.unpack_from('>I', boot, 4)[0]:08x}")
