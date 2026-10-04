#!/usr/bin/env python3
"""Fetch the official AROS amiga-m68k boot-floppy matching an extracted nightly."""
from pathlib import Path
from urllib.request import Request, urlopen
import argparse, re, subprocess

BASE = "https://sourceforge.net/projects/aros/files/nightly2/"

def get(url):
    req = Request(url, headers={"User-Agent": "AxiomicaOS-CI/1.0"})
    return urlopen(req, timeout=60).read()

p = argparse.ArgumentParser()
p.add_argument("nightly", type=Path)
a = p.parse_args()

isos = list(a.nightly.glob("AROS-*-amiga-m68k-boot-iso.zip"))
if len(isos) != 1:
    raise SystemExit(f"expected one downloaded AROS boot ISO archive, found {len(isos)}")
m = re.fullmatch(r"AROS-(20[0-9]{6})-amiga-m68k-boot-iso\.zip", isos[0].name)
if not m:
    raise SystemExit("cannot derive nightly date from AROS ISO archive")
date = m.group(1)
name = f"AROS-{date}-amiga-m68k-boot-floppy.zip"
url = f"{BASE}{date}/Binaries/{name}/download"
archive = a.nightly / name
print(f"Fetching official AROS m68k boot floppy {date}")
archive.write_bytes(get(url))
root = a.nightly / "boot-floppy"
root.mkdir(exist_ok=True)
subprocess.run(["7z", "x", "-y", f"-o{root}", str(archive)], check=True)
adfs = list(root.rglob("*.adf"))
if len(adfs) != 1:
    raise SystemExit(f"expected exactly one boot-floppy ADF, found {len(adfs)}")
out = a.nightly / "aros-boot-control.adf"
out.write_bytes(adfs[0].read_bytes())
print(f"AROS BOOT FLOPPY READY {out} size={out.stat().st_size}")
