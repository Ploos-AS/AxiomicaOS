#!/usr/bin/env python3
"""Discover the paired AROS m68k base and extended ROM images deterministically."""

from pathlib import Path
import argparse
import shutil

p=argparse.ArgumentParser()
p.add_argument("root",type=Path)
p.add_argument("base_output",type=Path)
p.add_argument("ext_output",type=Path)
a=p.parse_args()

base_names={"aros-amiga-m68k-rom.bin","aros.rom.bin","aros.rom"}
ext_names={"aros-amiga-m68k-ext.bin","aros-ext.bin","aros.ext.rom"}

files=[x for x in a.root.rglob("*") if x.is_file()]
bases=[x for x in files if x.name.lower() in base_names and x.stat().st_size==524288]
exts=[x for x in files if x.name.lower() in ext_names and x.stat().st_size==524288]

# Nightly layouts can rename the base image. Retain the old conservative
# fallback, but never use it for the extended ROM.
if not bases:
    bases=[x for x in files
           if ("rom" in x.name.lower() or "kick" in x.name.lower())
           and "ext" not in x.name.lower()
           and x.stat().st_size==524288]

if len(bases)!=1 or len(exts)!=1:
    print("AROS m68k ROM discovery candidates:")
    for x in files:
        n=x.name.lower()
        if ("rom" in n or "kick" in n or "ext" in n) and x.stat().st_size in (262144,524288,1048576):
            print(f"  {x} ({x.stat().st_size} bytes)")
    raise SystemExit(f"expected one base and one extended AROS ROM, found base={len(bases)} ext={len(exts)}")

for src,dst,label in ((bases[0],a.base_output,"BASE"),(exts[0],a.ext_output,"EXT")):
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,dst)
    print(f"AROS ROM {label} READY: {dst} size={dst.stat().st_size}")
