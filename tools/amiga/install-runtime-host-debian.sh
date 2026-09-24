#!/bin/sh
# Provision dependencies for the dedicated Axiomica Amiga runtime runner.
# ROM and GitHub runner registration are intentionally outside this script.
set -eu
[ "$(id -u)" -eq 0 ] || { echo "run as root" >&2; exit 2; }
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
  fs-uae xvfb xdotool python3 coreutils \
  gcc-m68k-linux-gnu binutils-m68k-linux-gnu \
  ca-certificates git
apt-get clean
rm -rf /var/lib/apt/lists/*
echo "Dependencies installed."
echo "Next: configure the GitHub self-hosted runner and AXIOMICA_KICKSTART_ROM."
