#!/usr/bin/env python3
"""Combine static and runtime evidence without overstating qualification."""

from pathlib import Path
import argparse, hashlib, json

p=argparse.ArgumentParser()
p.add_argument("--static",action="store_true")
p.add_argument("--runtime-log",type=Path)
p.add_argument("--image",type=Path)
p.add_argument("--emulator",default="unknown")
p.add_argument("--firmware",default="unknown")
a=p.parse_args()

runtime=False
if a.runtime_log and a.runtime_log.exists():
    t=a.runtime_log.read_text(errors="replace")
    runtime="M0.3 RUNTIME PASS" in t

image_sha256=None
image_size=None
if a.image is not None:
    if not a.image.is_file():
        raise SystemExit("qualification image missing")
    data=a.image.read_bytes()
    image_sha256=hashlib.sha256(data).hexdigest()
    image_size=len(data)

result={
  "milestone":"M0.3",
  "target":"m68k-amiga-a500",
  "static_pass":bool(a.static),
  "runtime_pass":runtime,
  "qualified":bool(a.static and runtime),
  "emulator":a.emulator,
  "firmware":a.firmware,
  "image_sha256":image_sha256,
  "image_size":image_size,
}
print(json.dumps(result,sort_keys=True))
if not a.static: raise SystemExit(2)
if a.runtime_log is not None and not runtime: raise SystemExit(3)
if a.runtime_log is not None and a.image is None: raise SystemExit(4)
