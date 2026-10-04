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
ROOT_BLOCK = 880
ROOT_OFFSET = ROOT_BLOCK * SECTOR

def make_empty_ofs_root(name: bytes = b"AxiomicaOS") -> bytes:
    """Create a minimal empty AmigaDOS OFS root block."""
    if len(name) > 30:
        raise ValueError("AmigaDOS volume name too long")
    block = bytearray(SECTOR)
    struct.pack_into(">I", block, 0, 2)       # T_HEADER
    struct.pack_into(">I", block, 12, 72)     # hash table size
    block[432] = len(name)                    # BCPL volume name
    block[433:433 + len(name)] = name
    struct.pack_into(">I", block, 508, 1)     # ST_ROOT

    words = list(struct.unpack(">128I", block))
    words[5] = (-sum(words)) & 0xFFFFFFFF     # checksum word at byte 20
    struct.pack_into(">128I", block, 0, *words)
    if sum(struct.unpack(">128I", block)) & 0xFFFFFFFF:
        raise AssertionError("root block checksum construction failed")
    return bytes(block)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("axam", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--bootblock", type=Path)
    args = p.parse_args()

    payload = args.axam.read_bytes()
    if len(payload) > ADF_SIZE - PAYLOAD_OFFSET:
        raise SystemExit("AXAM payload does not fit on DD floppy image")

    image = bytearray(ADF_SIZE)
    if args.bootblock:
        bootblock = args.bootblock.read_bytes()
        if len(bootblock) != BOOT_BLOCK:
            raise SystemExit("boot block must be exactly 1024 bytes")
        image[:BOOT_BLOCK] = bootblock
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
    if not args.bootblock:
        image[:len(header)] = header
    image[PAYLOAD_OFFSET:PAYLOAD_OFFSET + len(payload)] = payload
    if args.bootblock:
        if PAYLOAD_OFFSET + len(payload) > ROOT_OFFSET:
            raise SystemExit("AXAM payload overlaps AmigaDOS root block")
        image[ROOT_OFFSET:ROOT_OFFSET + SECTOR] = make_empty_ofs_root()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(image)

if __name__ == "__main__":
    main()
