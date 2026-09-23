# Amiga runtime CI host

Runtime qualification uses a dedicated self-hosted Linux x64 runner carrying the custom label `axiomica-amiga-runtime`. GitHub Actions routes a job only to a runner matching all labels in `runs-on`.

The host must provide:

- FS-UAE
- Xvfb
- xdotool
- m68k cross compiler/binutils used by Makefile.m68k
- a legally obtained local Kickstart ROM

Set `AXIOMICA_KICKSTART_ROM` in the runner service environment to the local ROM path. The ROM must not be placed in the checkout, GitHub secrets, Actions cache, logs, or uploaded artifacts.

The workflow rebuilds the ADF on the runtime host, runs the static gate, then boots that exact image through the unattended FS-UAE qualification runner. Runtime evidence is uploaded, but the ROM is outside every artifact path.

A runner is not trusted merely because it has the label: host provisioning and ROM provenance remain an operator responsibility.
