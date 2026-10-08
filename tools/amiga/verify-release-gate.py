#!/usr/bin/env python3
"""Verify that M0.3 runtime evidence qualifies the exact release image."""

from pathlib import Path
import argparse
import hashlib
import json

p = argparse.ArgumentParser()
p.add_argument("image", type=Path)
p.add_argument("evidence", type=Path)
p.add_argument("--firmware", choices=("kickstart","aros"))
a = p.parse_args()

if not a.image.is_file():
    raise SystemExit("RELEASE GATE FAIL: qualification image missing")
if not a.evidence.is_file():
    raise SystemExit("RELEASE GATE FAIL: runtime evidence missing")

data = a.image.read_bytes()
actual_sha = hashlib.sha256(data).hexdigest()
actual_size = len(data)

try:
    result = json.loads(a.evidence.read_text())
except (OSError, json.JSONDecodeError) as exc:
    raise SystemExit(f"RELEASE GATE FAIL: invalid runtime evidence: {exc}")

required = {
    "milestone": "M0.3",
    "target": "m68k-amiga-a500",
    "static_pass": True,
    "runtime_pass": True,
    "qualified": True,
}
if a.firmware is not None:
    required["firmware"] = a.firmware

for key, expected in required.items():
    if result.get(key) != expected:
        raise SystemExit(f"RELEASE GATE FAIL: {key} is not {expected!r}")

if result.get("image_sha256") != actual_sha:
    raise SystemExit("RELEASE GATE FAIL: ADF SHA-256 does not match runtime evidence")
if result.get("image_size") != actual_size:
    raise SystemExit("RELEASE GATE FAIL: ADF size does not match runtime evidence")

print(f"M0.3 RELEASE GATE PASS: qualified image sha256={actual_sha} size={actual_size}")
