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
matches=[]
for addr in wanted:
    pats=[
        rf"(?im)^\s*0*{addr}\b[^\n]*?\b([0-9a-f]{{2,4}})\b",
        rf"(?im)\b0x0*{addr}\b[^\n]*?\b0x([0-9a-f]{{2,4}})\b",
    ]
    for pat in pats:
        for m in re.finditer(pat,t):
            matches.append((m.start(),addr,m.group(1).lower()))

# De-duplicate alternate regex hits while retaining transcript order.
seen=set()
lines=[]
for pos,addr,value in sorted(matches):
    key=(pos,addr,value)
    if key in seen:
        continue
    seen.add(key)
    width=2 if addr=="bfe001" else 3
    lines.append(f"{addr} = {value[-width:]}")
if not lines:
    raise SystemExit("no Axiomica oracle addresses found in FS-UAE debugger transcript")
a.output.write_text("\n".join(lines)+"\n")
print("\n".join(lines))
