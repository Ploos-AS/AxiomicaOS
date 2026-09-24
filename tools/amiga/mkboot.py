#!/usr/bin/env python3
"""Create the deterministic AxiomicaOS Amiga bring-up container."""

from pathlib import Path
import argparse
import struct

MAGIC = b"AXAM"
VERSION = 1
LOAD_ADDRESS = 0  # AXAM v1: zero means relocatable/bootstrap-selected
HEADER_SIZE = 32

def checksum(data: bytes) -> int:
    return sum(data) & 0xFFFFFFFF

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("payload", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()

    payload = args.payload.read_bytes()
    header = struct.pack(
        ">4s7I",
        MAGIC,
        VERSION,
        HEADER_SIZE,
        LOAD_ADDRESS,
        len(payload),
        checksum(payload),
        0,
        0,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(header + payload)

if __name__ == "__main__":
    main()
