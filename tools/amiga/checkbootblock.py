#!/usr/bin/env python3
from pathlib import Path
import argparse, struct

def folded_sum(data: bytes) -> int:
    total = 0
    for off in range(0, 1024, 4):
        value = struct.unpack_from(">I", data, off)[0]
        old = total
        total = (total + value) & 0xffffffff
        if total < old:
            total = (total + 1) & 0xffffffff
    return total

p=argparse.ArgumentParser(); p.add_argument("image",type=Path); a=p.parse_args()
d=a.image.read_bytes()
if len(d)!=1024: raise SystemExit("boot block must be 1024 bytes")
if d[:4]!=b"DOS\0": raise SystemExit("missing DOS\\0 boot signature")
if folded_sum(d)!=0xffffffff: raise SystemExit("invalid Amiga boot-block checksum")
print("valid Amiga boot block")
