# Amiga M0.3 runtime qualification

AxiomicaOS uses native Amiga `COLOR00` writes as the first deterministic runtime oracle. This avoids depending on serial hardware, a filesystem, AmigaOS, or a text renderer during earliest bring-up.

## Observable states

| Colour value | Meaning |
| --- | --- |
| `0x002` | stage-0 entered |
| `0xF00` | stage-0 failed |
| `0x0F0` | AxiomicaOS kernel entered |
| `0x00F` | kernel reached platform halt |

A successful current M0.3 run should therefore progress through stage-0 and end at the kernel halt marker.

## Qualification matrix

The first required profile is:

- machine: Amiga 500 class
- CPU: 68000
- chipset: OCS/ECS-compatible baseline
- floppy: generated `axiomicaos-amiga.adf`
- ROM: legal runtime/user-provided configuration; never stored in this repository

After A500/68000 passes, repeat on A500+/ECS and A1200/68020 as regression profiles. Amiberry and FellowNG can be added after the reference path is deterministic.

A build or valid boot-block checksum is not a runtime PASS. PASS requires observed execution reaching the AxiomicaOS kernel marker in an emulator or on hardware.

## Machine-readable oracle

In addition to COLOR00, the kernel writes a fixed byte to CIA-A PRA during bring-up: 0xA5 when platform initialization is reached and 0x5A immediately before the kernel halt loop. This gives emulator/debugger integrations a simple memory-mapped state to inspect without OCR or framebuffer analysis.

The CIA oracle is a bring-up mechanism, not a permanent userspace ABI. It may move to a dedicated debug device once the driver model exists.
