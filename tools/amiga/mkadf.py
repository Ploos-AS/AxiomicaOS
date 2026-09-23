#!/usr/bin/env python3
"""Build a deterministic raw Amiga bring-up floppy image.

This M0.3 image is deliberately self-describing and contains no proprietary
ROM or operating-system material. The stage-0 boot code will be added next.
"""

from pathlib import Path
import argparse
import struct

ADF_SIZE = 901120
SECTOR = 512
BOOT_BLOCK = 1024
MAGIC = b"AXDF"
VERSION = 1
PAYLOAD_OFFSET = BOOT_BLOCK

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("axam", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()

    payload = args.axam.read_bytes()
    if len(payload) > ADF_SIZE - PAYLOAD_OFFSET:
        raise SystemExit("AXAM payload does not fit on DD floppy image")

    image = bytearray(ADF_SIZE)
    header = struct.pack(
        ">4s7I",
        MAGIC,
        VERSION,
        PAYLOAD_OFFSET,
        len(payload),
        sum(payload) & 0xFFFFFFFF,
        SECTOR,
        0,
        0,
    )
    image[:len(header)] = header
    image[PAYLOAD_OFFSET:PAYLOAD_OFFSET + len(payload)] = payload
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(image)

if __name__ == "__main__":
    main()
