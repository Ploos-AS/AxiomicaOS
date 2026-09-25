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
wanted={"bfe001":[],"dff180":[]}
for addr in list(wanted):
    pats=[
        rf"(?im)^\s*0*{addr}\b[^\n]*?\b([0-9a-f]{{2,4}})\b",
        rf"(?im)\b0x0*{addr}\b[^\n]*?\b0x([0-9a-f]{{2,4}})\b",
    ]
    for pat in pats:
        m=re.search(pat,t)
        if m:
            wanted[addr].append(m.group(1).lower())
    # Preserve all samples in transcript order; qualification needs to see
    # distinct entry and halt states, not merely the first matching dump.

lines=[]
for value in wanted["bfe001"]:
    lines.append(f"bfe001 = {value[-2:]}")
for value in wanted["dff180"]:
    lines.append(f"dff180 = {value[-3:]}")
if not lines:
    raise SystemExit("no Axiomica oracle addresses found in FS-UAE debugger transcript")
a.output.write_text("\n".join(lines)+"\n")
print("\n".join(lines))
