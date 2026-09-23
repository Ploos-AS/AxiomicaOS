#!/usr/bin/env python3
"""Create a 1024-byte Amiga boot block containing AxiomicaOS stage-0."""

from pathlib import Path
import argparse
import struct

SIZE = 1024
CODE_OFFSET = 12

def amiga_checksum(block: bytes) -> int:
    total = 0
    for off in range(0, SIZE, 4):
        value = struct.unpack_from(">I", block, off)[0]
        old = total
        total = (total + value) & 0xFFFFFFFF
        if total < old:
            total = (total + 1) & 0xFFFFFFFF
    return (~total) & 0xFFFFFFFF

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("stage0", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    code = args.stage0.read_bytes()
    if len(code) > SIZE - CODE_OFFSET:
        raise SystemExit(f"stage-0 too large: {len(code)} > {SIZE-CODE_OFFSET}")
    block = bytearray(SIZE)
    block[0:4] = b"DOS\0"
    # checksum at 4..7 is zero while calculated; root block remains zero.
    block[CODE_OFFSET:CODE_OFFSET + len(code)] = code
    # Executable stage-0 must begin exactly where the ROM boot convention
    # transfers control after the 12-byte DOS/checksum/root header.
    if not code:
        raise SystemExit("empty stage-0")
    struct.pack_into(">I", block, 4, amiga_checksum(block))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(block)
    print(f"boot block: {len(code)} bytes stage-0, checksum=0x{struct.unpack_from('>I', block, 4)[0]:08x}")

if __name__ == "__main__":
    main()
