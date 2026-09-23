# Amiga stage-0 loader

The first native loader is deliberately split from the AxiomicaOS kernel.

Classic Amiga ROM firmware is allowed to perform the initial floppy boot and provide the boot I/O request. Stage-0 may use that firmware/Exec environment solely to read the AxiomicaOS image. The dependency ends before control is transferred to the kernel.

This avoids redistributing Kickstart while still supporting the normal hardware boot path on machines that already contain a legal ROM.

## M0.3 stage-0 contract

The initial 68000-compatible assembly scaffold:

- receives the ROM boot environment
- uses the boot trackdisk I/O request
- reads the AXAM header from byte 1024
- validates magic, format version, header size, load address and payload bounds
- returns failure cleanly while the full payload-copy/checksum path is under construction

The kernel remains freestanding and has no Exec, trackdisk or AmigaOS ABI dependency.

## Next qualification gate

Stage-0 becomes boot-capable only after it can read the complete AXAM payload, validate its checksum, place the raw kernel at 0x00100000 and jump to the kernel entry point. Until then, generated ADF files remain development images rather than claimed bootable releases.

## Payload transfer implemented

Stage-0 now copies the initial payload bytes from the AXAM header sector, reads all following sectors through the boot I/O request, computes the AXAM additive checksum while copying, rejects a mismatch, and jumps to the requested 0x00100000 entry address only after successful validation.

The remaining M0.3 work is to encode stage-0 as the actual Amiga boot block with a valid boot-block checksum and integrate it into the generated ADF. Only after emulator qualification will the ADF be marked bootable/supported.
