#!/usr/bin/env python3
"""Report structural Amiga DD ADF metadata without copying reference content."""

from pathlib import Path
import argparse
import hashlib
import struct

SIZE = 901120
BLOCK = 512
ROOT = 880

def u32(data: bytes, off: int) -> int:
    return struct.unpack_from(">I", data, off)[0]

def block_sum(data: bytes) -> int:
    return sum(struct.unpack(">128I", data)) & 0xFFFFFFFF

def describe(label: str, path: Path) -> list[str]:
    data = path.read_bytes()
    if len(data) != SIZE:
        raise SystemExit(f"{label}: expected {SIZE} bytes, got {len(data)}")
    root = data[ROOT * BLOCK:(ROOT + 1) * BLOCK]
    return [
        f"[{label}]",
        f"sha256={hashlib.sha256(data).hexdigest()}",
        f"dos_type={data[:4].hex()}",
        f"boot_checksum=0x{u32(data,4):08x}",
        f"root_pointer={u32(data,8)}",
        f"root_type={u32(root,0)}",
        f"root_header_key={u32(root,4)}",
        f"root_checksum=0x{u32(root,20):08x}",
        f"root_block_sum=0x{block_sum(root):08x}",
        f"root_secondary_type={u32(root,508)}",
    ]

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("reference", type=Path)
    p.add_argument("candidate", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    lines = describe("reference", args.reference) + [""] + describe("candidate", args.candidate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
