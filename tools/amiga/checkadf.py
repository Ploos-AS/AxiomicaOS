#!/usr/bin/env python3
"""Validate the deterministic AxiomicaOS Amiga floppy container."""

from pathlib import Path
import argparse
import struct

ADF_SIZE = 901120

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("image", type=Path)
    args = p.parse_args()
    data = args.image.read_bytes()
    if len(data) != ADF_SIZE:
        raise SystemExit("unexpected ADF size")
    magic, version, offset, size, expected, sector, flags, reserved = struct.unpack(
        ">4s7I", data[:32]
    )
    payload = data[offset:offset + size]
    if magic != b"AXDF" or version != 1 or sector != 512:
        raise SystemExit("invalid AXDF metadata")
    if flags != 0 or reserved != 0 or offset < 1024 or offset + size > len(data):
        raise SystemExit("invalid AXDF layout")
    if (sum(payload) & 0xFFFFFFFF) != expected:
        raise SystemExit("AXDF payload checksum mismatch")
    if payload[:4] != b"AXAM":
        raise SystemExit("AXDF does not contain an AXAM payload")
    print(f"AXDF v{version}: {size} byte AXAM payload at offset {offset}")

if __name__ == "__main__":
    main()
