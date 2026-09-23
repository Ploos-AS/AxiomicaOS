#!/usr/bin/env python3
"""Validate an AxiomicaOS Amiga bring-up container."""

from pathlib import Path
import argparse
import struct
import sys

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("image", type=Path)
    args = p.parse_args()

    data = args.image.read_bytes()
    if len(data) < 32:
        raise SystemExit("image too small")
    magic, version, header_size, load, size, expected, flags, reserved = struct.unpack(
        ">4s7I", data[:32]
    )
    payload = data[header_size:]
    actual = sum(payload) & 0xFFFFFFFF
    if magic != b"AXAM" or version != 1 or header_size != 32:
        raise SystemExit("invalid AXAM header")
    if size != len(payload) or actual != expected:
        raise SystemExit("payload size/checksum mismatch")
    if load != 0x00100000 or flags != 0 or reserved != 0:
        raise SystemExit("unexpected bootstrap metadata")
    print(f"AXAM v{version}: {size} bytes, load=0x{load:08x}, checksum=0x{actual:08x}")

if __name__ == "__main__":
    main()
