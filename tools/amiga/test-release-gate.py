#!/usr/bin/env python3
"""Hermetic tests for the M0.3 exact-image release gate."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "tools/amiga/verify-release-gate.py"

def run(image: Path, evidence: Path, expect_ok: bool) -> None:
    p = subprocess.run(
        [sys.executable, str(GATE), str(image), str(evidence)],
        text=True, capture_output=True
    )
    if expect_ok and p.returncode != 0:
        raise SystemExit(f"expected PASS, got {p.returncode}: {p.stdout}{p.stderr}")
    if not expect_ok and p.returncode == 0:
        raise SystemExit("expected release gate rejection, got PASS")

with tempfile.TemporaryDirectory() as td:
    d = Path(td)
    image = d / "qualified.adf"
    image.write_bytes(b"AxiomicaOS M0.3 release-gate fixture\n")
    digest = hashlib.sha256(image.read_bytes()).hexdigest()

    base = {
        "milestone": "M0.3",
        "target": "m68k-amiga-a500",
        "static_pass": True,
        "runtime_pass": True,
        "qualified": True,
        "emulator": "fixture",
        "image_sha256": digest,
        "image_size": image.stat().st_size,
    }

    evidence = d / "evidence.json"

    evidence.write_text(json.dumps(base))
    run(image, evidence, True)

    bad = dict(base)
    bad["image_sha256"] = "0" * 64
    evidence.write_text(json.dumps(bad))
    run(image, evidence, False)

    bad = dict(base)
    bad["target"] = "wrong-target"
    evidence.write_text(json.dumps(bad))
    run(image, evidence, False)

    bad = dict(base)
    bad["runtime_pass"] = False
    bad["qualified"] = False
    evidence.write_text(json.dumps(bad))
    run(image, evidence, False)

    bad = dict(base)
    bad["image_size"] += 1
    evidence.write_text(json.dumps(bad))
    run(image, evidence, False)

print("M0.3 RELEASE GATE TESTS PASS")
