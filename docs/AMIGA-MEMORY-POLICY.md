# Amiga stage-0 memory policy

The A500/A2000 hardware map reserves 0x100000-0x1fffff and classic Amiga system RAM is dynamically managed by Exec. Stage-0 therefore must not treat 0x100000 as universally writable RAM.

For the bootstrap phase, stage-0 asks Exec for one contiguous block containing the kernel image plus a 512-byte disk scratch area. After the AXAM payload is copied and verified, execution jumps to the beginning of that allocated block.

This is intentionally a bootstrap dependency only: after transfer to AxiomicaOS, Exec is no longer part of the kernel runtime.

The first A500 profile currently caps the payload at 448 KiB so it can be tested on constrained configurations. A later loader format should carry relocation information or a position-independent kernel contract instead of treating the AXAM v1 load-address field as authoritative.
