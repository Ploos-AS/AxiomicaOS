#!/usr/bin/env python3
"""Parse stock FS-UAE/UAE debugger output into Axiomica runtime evidence.

Stock FS-UAE exposes the UAE console debugger (Mod+D). Its debugger supports
memory dumps with 'm <address> [lines]'. This adapter parses captured debugger
transcripts; process automation/PTY driving is intentionally separate.
"""

from pathlib import Path
import argparse, re

p=argparse.ArgumentParser()
p.add_argument("transcript",type=Path)
p.add_argument("output",type=Path)
a=p.parse_args()
t=a.transcript.read_text(errors="replace")

# Accept common UAE memory-dump renderings and normalize only our two oracle
# addresses. Do not infer success from unrelated text.
wanted={"bfe001":None,"dff180":None}
for addr in list(wanted):
    pats=[
        rf"(?im)^\s*0*{addr}\b[^\n]*?\b([0-9a-f]{{2,4}})\b",
        rf"(?im)\b0x0*{addr}\b[^\n]*?\b0x([0-9a-f]{{2,4}})\b",
    ]
    for pat in pats:
        m=re.search(pat,t)
        if m:
            wanted[addr]=m.group(1).lower()
            break

lines=[]
if wanted["bfe001"] is not None:
    lines.append(f"bfe001 = {wanted['bfe001'][-2:]}")
if wanted["dff180"] is not None:
    lines.append(f"dff180 = {wanted['dff180'][-3:]}")
if not lines:
    raise SystemExit("no Axiomica oracle addresses found in FS-UAE debugger transcript")
a.output.write_text("\n".join(lines)+"\n")
print("\n".join(lines))
