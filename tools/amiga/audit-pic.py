#!/usr/bin/env python3
"""Fail if the final M0.3 m68k ELF is not a relocation-free flat-image candidate."""
from pathlib import Path
import argparse, subprocess, re
p=argparse.ArgumentParser(); p.add_argument("elf",type=Path); a=p.parse_args()
prefix="m68k-linux-gnu-"
def run(*args):
    return subprocess.check_output([prefix+args[0],*args[1:]],text=True,stderr=subprocess.STDOUT)
hdr=run("readelf","-h",str(a.elf))
if "Motorola 68000" not in hdr and "MC68000" not in hdr:
    raise SystemExit("PIC AUDIT FAIL: unexpected ELF machine")
rel=run("readelf","-rW",str(a.elf))
# A flat binary cannot carry runtime ELF relocations. PC-relative references
# must already be resolved by the static linker.
if re.search(r"\bR_68K_",rel):
    print(rel)
    raise SystemExit("PIC AUDIT FAIL: final ELF still contains relocations")
syms=run("nm","-u",str(a.elf)).strip()
if syms:
    print(syms)
    raise SystemExit("PIC AUDIT FAIL: undefined symbols remain")
print("M0.3 PIC AUDIT PASS: m68k ELF has no runtime relocations or undefined symbols")
