# AxiomicaOS m68k architecture

This directory contains CPU-family code shared by m68k machines.

Machine-specific code belongs under machines/, not here.

Planned CPU coverage: MC68000, 68010, 68020, 68030, 68040 and 68060. MMU, cache and exception features are capability-driven so a 68000 machine remains useful without pretending to provide protection it cannot implement.
