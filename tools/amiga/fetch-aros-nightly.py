#!/usr/bin/env python3
"""Download and unpack the official AROS amiga-m68k nightly boot archive."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import argparse
import subprocess

INDEX="https://www.aros.org/cgi-bin/files?lang=en&type=nightly2"

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href=dict(attrs).get("href")
            if href: self.links.append(href)

p=argparse.ArgumentParser()
p.add_argument("output",type=Path)
a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)

req=Request(INDEX,headers={"User-Agent":"AxiomicaOS-CI/1.0"})
html=urlopen(req,timeout=30).read().decode("utf-8","replace")
parser=Links(); parser.feed(html)
links=[urljoin(INDEX,x) for x in parser.links if "amiga-m68k-boot" in x.lower()]
if not links:
    raise SystemExit("AROS nightly index contains no amiga-m68k boot download")
# Prefer the boot floppy: it is much smaller than the full ISO and contains the boot ROM payload.
links.sort(key=lambda x: (0 if "floppy" in x.lower() else 1, x))
url=links[0]
archive=a.output/"aros-nightly"
print(f"Fetching official AROS nightly: {url}")
req=Request(url,headers={"User-Agent":"AxiomicaOS-CI/1.0"})
archive.write_bytes(urlopen(req,timeout=60).read())
subprocess.run(["7z","x","-y",f"-o{a.output}",str(archive)],check=True)
print("AROS NIGHTLY READY")
