#!/usr/bin/env python3
"""Drive an interactive FS-UAE/UAE debugger attached to this terminal.

The emulator must already have entered the console debugger (Mod+D). This
driver sends only read-only memory commands and records the transcript.
"""

import argparse, os, select, sys, time
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("output",type=Path)
p.add_argument("--timeout",type=float,default=5.0)
a=p.parse_args()

if not sys.stdin.isatty():
    raise SystemExit("stdin is not a TTY; attach this driver to the FS-UAE debugger terminal")

fd=sys.stdin.fileno()
commands=(b"m bfe001 1\n", b"m dff180 1\n")
buf=bytearray()
for cmd in commands:
    os.write(fd,cmd)
    deadline=time.monotonic()+a.timeout
    while time.monotonic()<deadline:
        ready,_,_=select.select([fd],[],[],0.1)
        if not ready: continue
        chunk=os.read(fd,4096)
        if not chunk: break
        buf.extend(chunk)
        # UAE debugger prompt normally ends in '>'.
        if b">" in chunk: break

a.output.write_bytes(bytes(buf))
if not buf:
    raise SystemExit("no debugger output captured")
print(f"captured {len(buf)} bytes to {a.output}",file=sys.stderr)
