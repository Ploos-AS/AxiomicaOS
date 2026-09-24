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
    if data[:4] == b"DOS\0":
        offset = 1024
        payload = data[offset:]
        if payload[:4] != b"AXAM":
            raise SystemExit("bootable ADF does not contain AXAM at byte 1024")
        _, version, header_size, load, size, expected, flags, reserved = struct.unpack(">4s7I", payload[:32])
        body = payload[header_size:header_size + size]
        if version != 1 or header_size != 32 or load != 0 or flags != 0 or reserved != 0:
            raise SystemExit("invalid embedded AXAM metadata")
        if (sum(body) & 0xFFFFFFFF) != expected:
            raise SystemExit("embedded AXAM checksum mismatch")
        print(f"boot-block ADF: {size} byte AXAM payload at offset {offset}")
    else:
        magic, version, offset, size, expected, sector, flags, reserved = struct.unpack(">4s7I", data[:32])
        payload = data[offset:offset + size]
        if magic != b"AXDF" or version != 1 or sector != 512:
            raise SystemExit("invalid AXDF metadata")
        if flags != 0 or reserved != 0 or offset < 1024 or offset + size > len(data):
            raise SystemExit("invalid AXDF layout")
        if (sum(payload) & 0xFFFFFFFF) != expected or payload[:4] != b"AXAM":
            raise SystemExit("invalid AXDF payload")
        print(f"AXDF v{version}: {size} byte AXAM payload at offset {offset}")

if __name__ == "__main__":
    main()
