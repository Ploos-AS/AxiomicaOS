#!/usr/bin/env python3
"""Extract an AROS m68k ROM from an unpacked nightly tree without guessing silently."""

from pathlib import Path
import argparse
import shutil

p=argparse.ArgumentParser()
p.add_argument("root",type=Path)
p.add_argument("output",type=Path)
a=p.parse_args()

candidates=[]
for path in a.root.rglob("*"):
    if not path.is_file():
        continue
    name=path.name.lower()
    size=path.stat().st_size
    if ("rom" in name or "kick" in name) and size in (262144,524288,1048576):
        candidates.append(path)

if len(candidates) != 1:
    print("AROS ROM discovery candidates:")
    for x in candidates: print(f"  {x} ({x.stat().st_size} bytes)")
    raise SystemExit(f"expected exactly one plausible AROS ROM, found {len(candidates)}")

a.output.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile(candidates[0],a.output)
print(f"AROS ROM READY: {a.output} size={a.output.stat().st_size}")
