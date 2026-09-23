#!/usr/bin/env python3
"""Normalize emulator memory/register observations into Axiomica runtime evidence."""

import argparse
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("--cia",help="observed CIA-A PRA value")
p.add_argument("--color",help="observed COLOR00 value")
p.add_argument("--append",type=Path,required=True)
a=p.parse_args()

lines=[]
if a.cia is not None:
    lines.append(f"bfe001 = {int(a.cia,0):02x}")
if a.color is not None:
    lines.append(f"dff180 = {int(a.color,0):03x}")
if not lines:
    raise SystemExit("no oracle observation supplied")
with a.append.open("a") as f:
    for line in lines: f.write(line+"\n")
print("\n".join(lines))
