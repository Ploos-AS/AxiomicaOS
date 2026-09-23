#!/usr/bin/env python3
"""Combine static and runtime evidence without overstating qualification."""

from pathlib import Path
import argparse, json

p=argparse.ArgumentParser()
p.add_argument("--static",action="store_true")
p.add_argument("--runtime-log",type=Path)
p.add_argument("--emulator",default="unknown")
a=p.parse_args()

runtime=False
if a.runtime_log and a.runtime_log.exists():
    t=a.runtime_log.read_text(errors="replace")
    runtime="M0.3 RUNTIME PASS" in t

result={
  "milestone":"M0.3",
  "target":"m68k-amiga-a500",
  "static_pass":bool(a.static),
  "runtime_pass":runtime,
  "emulator":a.emulator,
}
print(json.dumps(result,sort_keys=True))
if not a.static: raise SystemExit(2)
