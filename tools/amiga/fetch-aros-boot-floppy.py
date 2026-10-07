#!/usr/bin/env python3
"""Discover and fetch an official AROS m68k boot floppy from SourceForge."""
from pathlib import Path
from urllib.request import Request, urlopen
import argparse
import re
import subprocess

BASE = "https://sourceforge.net/projects/aros/files/nightly2/"

def get(url):
    req = Request(url, headers={"User-Agent": "AxiomicaOS-CI/1.0"})
    return urlopen(req, timeout=60).read()

p = argparse.ArgumentParser()
p.add_argument("nightly", type=Path)
a = p.parse_args()
isos = list(a.nightly.glob("AROS-*-amiga-m68k-boot-iso.zip"))
if len(isos) != 1:
    raise SystemExit(f"expected one AROS boot ISO archive, found {len(isos)}")
match = re.fullmatch(r"AROS-(20[0-9]{6})-amiga-m68k-boot-iso\.zip", isos[0].name)
if not match:
    raise SystemExit("cannot determine nightly date")
iso_date = match.group(1)

# SourceForge does not guarantee every artifact is published every day.
# Prefer the ISO date, then inspect earlier published nightly directories.
index = get(BASE).decode("utf-8", "replace")
dates = sorted(set(re.findall(r"/nightly2/(20[0-9]{6})/", index)), reverse=True)
candidates = [iso_date] + [d for d in dates if d < iso_date][:30]
chosen = None
for date in candidates:
    directory = f"{BASE}{date}/Binaries/"
    try:
        page = get(directory).decode("utf-8", "replace")
    except Exception as exc:
        print(f"Skipping {date}: {exc}", flush=True)
        continue
    names = sorted(set(re.findall(r"AROS-[0-9]{8}-amiga-m68k-boot-floppy\\.zip", page)))
    if names:
        chosen = (date, names[0])
        break
if chosen is None:
    raise SystemExit("No official amiga-m68k boot-floppy ZIP found in recent SourceForge nightly listings")

date, name = chosen
print(f"AROS boot floppy selected: {date}/{name}; ISO date={iso_date}", flush=True)
archive = a.nightly / name
archive.write_bytes(get(f"{BASE}{date}/Binaries/{name}/download"))
root = a.nightly / "boot-floppy"
root.mkdir(exist_ok=True)
subprocess.run(["7z", "x", "-y", f"-o{root}", str(archive)], check=True)
adfs = list(root.rglob("*.adf"))
if len(adfs) != 1:
    raise SystemExit(f"expected exactly one AROS boot-floppy ADF, found {len(adfs)}")
out = a.nightly / "aros-boot-control.adf"
out.write_bytes(adfs[0].read_bytes())
print(f"AROS BOOT FLOPPY READY {out} size={out.stat().st_size}", flush=True)
