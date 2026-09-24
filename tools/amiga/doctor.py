#!/usr/bin/env python3
"""Report M0.3 qualification readiness without claiming runtime success."""

from pathlib import Path
import json, shutil, os

tools=["fs-uae","Xvfb","xdotool","python3","timeout",
       "m68k-linux-gnu-gcc","m68k-linux-gnu-ld","m68k-linux-gnu-objcopy"]
checks={x: bool(shutil.which(x)) for x in tools}
rom=os.environ.get("AXIOMICA_KICKSTART_ROM")
checks["external_rom"]=bool(rom and Path(rom).is_file() and os.access(rom,os.R_OK))
adf=Path("build/m68k-amiga/axiomicaos-amiga.adf")
checks["built_adf"]=adf.is_file() and adf.stat().st_size==901120
ready=all(checks[x] for x in tools) and checks["external_rom"]
print(json.dumps({"milestone":"M0.3","runtime_host_ready":ready,"checks":checks},indent=2,sort_keys=True))
raise SystemExit(0 if ready else 1)
