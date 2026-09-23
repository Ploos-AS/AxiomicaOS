# AXAM: AxiomicaOS Amiga bring-up image

M0.2 introduces a tiny deterministic container around the raw Amiga payload.

This is **not** an ADF and is not presented as a finished end-user boot format. It is an internal contract between future machine-specific loaders and the AxiomicaOS payload.

All multi-byte fields are big-endian.

| Offset | Size | Meaning |
| --- | ---: | --- |
| 0x00 | 4 | ASCII `AXAM` |
| 0x04 | 4 | format version |
| 0x08 | 4 | header size |
| 0x0c | 4 | requested load address |
| 0x10 | 4 | payload length |
| 0x14 | 4 | additive payload checksum |
| 0x18 | 4 | flags, currently zero |
| 0x1c | 4 | reserved |

The initial load address is 0x00100000. The format is intentionally simple so an eventual floppy, ROM, serial or emulator-side loader can validate and load the same payload.

The next milestone is a legal, reproducible loader path that can place this image in RAM and transfer control without redistributing Kickstart or AmigaOS.
