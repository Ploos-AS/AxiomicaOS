# Building AxiomicaOS for m68k

The first cross-build target is the classic Amiga BSP.

## Toolchain

The current bootstrap uses the Debian/Ubuntu `m68k-linux-gnu` GCC/binutils cross toolchain only as a freestanding compiler and linker. AxiomicaOS does not use Linux APIs or a hosted C runtime.

    make -f Makefile.m68k m68k-amiga

Outputs:

- `build/m68k-amiga/axiomicaos-amiga.elf`
- `build/m68k-amiga/axiomicaos-amiga.bin`

The binary is a raw bring-up payload, not yet a user-bootable Amiga disk image.

## Qualification stages

1. cross-compile all common kernel and Amiga BSP sources
2. verify a freestanding ELF with no hosted runtime dependencies
3. define a deterministic loader/image format
4. add early debug output visible to the emulator harness
5. boot under the AxiomicaOS Amiga runtime qualification path
6. qualify representative 68000 and later CPU/chipset profiles

No proprietary Kickstart or AmigaOS image is committed to this repository.
