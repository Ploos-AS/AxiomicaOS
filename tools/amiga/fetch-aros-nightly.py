#!/usr/bin/env python3
"""Download and unpack the latest official AROS amiga-m68k nightly from SourceForge."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import argparse
import re
import subprocess

FILES="https://sourceforge.net/projects/aros/files/nightly2/"

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href=dict(attrs).get("href")
            if href: self.links.append(href)

def get(url):
    req=Request(url,headers={"User-Agent":"AxiomicaOS-CI/1.0"})
    return urlopen(req,timeout=60).read()

p=argparse.ArgumentParser()
p.add_argument("output",type=Path)
a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)

# SourceForge directory pages expose dated nightly2 directories. Select the
# newest date rather than following a generic "latest" redirect for another arch.
html=get(FILES).decode("utf-8","replace")
dates=sorted(set(re.findall(r"/nightly2/(20[0-9]{6})/",html)),reverse=True)
if not dates:
    raise SystemExit("SourceForge nightly2 index contains no dated builds")

chosen=None
for date in dates[:14]:
    directory=urljoin(FILES,f"{date}/Binaries/")
    page=get(directory).decode("utf-8","replace")
    iso_name=f"AROS-{date}-amiga-m68k-boot-iso.zip"
    floppy_name=f"AROS-{date}-amiga-m68k-boot-floppy.zip"
    if iso_name in page and floppy_name in page:
        chosen=(date,directory,iso_name,floppy_name)
        break
if chosen is None:
    raise SystemExit("no recent official amiga-m68k boot ISO nightly found")

date,directory,name,floppy_name=chosen
url=urljoin(directory,name+"/download")
archive=a.output/name
print(f"Fetching official AROS nightly {date} from SourceForge")
archive.write_bytes(get(url))
subprocess.run(["7z","x","-y",f"-o{a.output}",str(archive)],check=True)

floppy_url=urljoin(directory,floppy_name+"/download")
floppy_archive=a.output/floppy_name
print(f"Fetching official AROS boot floppy {date} from SourceForge")
floppy_archive.write_bytes(get(floppy_url))
floppy_root=a.output/"boot-floppy"
floppy_root.mkdir(exist_ok=True)
subprocess.run(["7z","x","-y",f"-o{floppy_root}",str(floppy_archive)],check=True)

# The boot ZIP contains the ISO; the ROM payload lives inside that ISO.
isos=list(a.output.rglob("*.iso"))
if len(isos) != 1:
    raise SystemExit(f"expected exactly one AROS boot ISO, found {len(isos)}")
iso_root=a.output/"iso"
iso_root.mkdir(exist_ok=True)
subprocess.run(["7z","x","-y",f"-o{iso_root}",str(isos[0])],check=True)
print("AROS NIGHTLY READY")
