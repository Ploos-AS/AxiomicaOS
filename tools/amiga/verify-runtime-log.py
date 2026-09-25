#!/usr/bin/env python3
"""Verify the ordered M0.3 Amiga runtime oracle sequence."""
from pathlib import Path
import argparse, re

p=argparse.ArgumentParser()
p.add_argument("log",type=Path)
a=p.parse_args()
text=a.log.read_text(errors="replace")

values=[]
for m in re.finditer(r"(?im)^\s*bfe001\s*=\s*([0-9a-f]{2})\b", text):
    values.append(m.group(1).lower())

if "a5" not in values:
    raise SystemExit("RUNTIME FAIL: kernel-entry oracle 0xA5 not observed")
try:
    entry=values.index("a5")
except ValueError:
    raise SystemExit("RUNTIME FAIL: kernel-entry oracle missing")
if "5a" not in values[entry+1:]:
    raise SystemExit("RUNTIME FAIL: kernel-halt oracle 0x5A not observed after entry")

print("M0.3 RUNTIME PASS: ordered CIA entry 0xA5 -> halt 0x5A observed")
