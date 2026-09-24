# AXAM: AxiomicaOS Amiga bring-up image

M0.3 uses a tiny deterministic container around the raw Amiga payload.

This is **not** an ADF and is not presented as a finished end-user boot format. It is an internal contract between future machine-specific loaders and the AxiomicaOS payload.

All multi-byte fields are big-endian.

| Offset | Size | Meaning |
| --- | ---: | --- |
| 0x00 | 4 | ASCII `AXAM` |
| 0x04 | 4 | format version |
| 0x08 | 4 | header size |
| 0x0c | 4 | load address (`0` = relocatable/bootstrap-selected) |
| 0x10 | 4 | payload length |
| 0x14 | 4 | additive payload checksum |
| 0x18 | 4 | flags, currently zero |
| 0x1c | 4 | reserved |

AXAM v1 uses a load-address value of `0` for the M0.3 Amiga path. This means the bootstrap selects the RAM location dynamically; it must not assume a fixed physical address. The current stage-0 validates the header first, allocates exactly the payload plus its private prefix and bootstrap stack, then copies and checksums the payload. The format remains intentionally simple so later floppy, ROM, serial or emulator-side loaders can validate the same payload.

The next milestone is a legal, reproducible loader path that can place this image in RAM and transfer control without redistributing Kickstart or AmigaOS.
