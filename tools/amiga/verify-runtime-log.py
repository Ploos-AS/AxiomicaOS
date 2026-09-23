#!/usr/bin/env python3
"""Verify an emulator/debugger trace against the M0.3 runtime contract."""

from pathlib import Path
import argparse, re

p=argparse.ArgumentParser()
p.add_argument("log",type=Path)
a=p.parse_args()
text=a.log.read_text(errors="replace")

def seen(address, value):
    patterns=[
        rf"(?i){address}.*(?:=|:|\s){value}\b",
        rf"(?i)0x{address}.*(?:=|:|\s)0x{value}\b",
    ]
    return any(re.search(x,text) for x in patterns)

kernel=seen("bfe001","a5") or seen("dff180","0f0")
halt=seen("bfe001","5a") or seen("dff180","00f")
if not kernel:
    raise SystemExit("RUNTIME FAIL: kernel-entry oracle not observed")
if not halt:
    raise SystemExit("RUNTIME FAIL: halt oracle not observed")
print("M0.3 RUNTIME PASS: kernel entry and halt oracle observed")
