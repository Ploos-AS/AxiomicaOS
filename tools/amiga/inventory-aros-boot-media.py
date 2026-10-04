#!/usr/bin/env python3
"""Inventory AROS nightly files relevant to Amiga boot-media qualification."""

from pathlib import Path
import argparse
import hashlib

INTERESTING_SUFFIXES = {".adf", ".adz", ".hdf", ".img", ".rom", ".bin", ".device"}
INTERESTING_NAMES = {"boot", "bootblock", "bootloader", "trackdisk"}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def interesting(path: Path) -> bool:
    low = path.name.lower()
    return (
        path.suffix.lower() in INTERESTING_SUFFIXES
        or any(token in low for token in INTERESTING_NAMES)
    )

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("root", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()

    root = args.root.resolve()
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and interesting(path):
            rows.append((str(path.relative_to(root)), path.stat().st_size, digest(path)))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        f.write("# AROS Amiga boot-media inventory\n")
        f.write(f"# root={root}\n")
        for rel, size, sha in rows:
            f.write(f"{size:10d}  {sha}  {rel}\n")

    print(f"AROS boot-media inventory: {len(rows)} candidates -> {args.output}")

if __name__ == "__main__":
    main()
