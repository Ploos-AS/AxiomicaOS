# FS-UAE qualification

M0.3 uses FS-UAE as the first reference emulator path for the Amiga A500/68000 target.

Build with `make -f Makefile.m68k m68k-amiga`, then run `AXIOMICA_KICKSTART_ROM=/path/to/rom tools/amiga/run-fsuae.sh`.

The ROM is an external legal qualification dependency and is never committed or included in CI artifacts.

A runtime PASS requires observed execution reaching the kernel marker; merely opening FS-UAE or recognizing the floppy is insufficient. The next harness revision should automate observation of the final native proof-of-life state.
