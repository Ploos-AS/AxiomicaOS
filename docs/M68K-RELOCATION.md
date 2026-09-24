# m68k relocatable bootstrap kernel

The initial Amiga kernel image is now built as position-independent 68000 code and linked at relative base zero. GCC's m68k backend supports position-independent generation; `-mpcrel` selects direct PC-relative addressing on 68000 and implies PIC. GCC documents that this mode is limited to 16-bit PC-relative offsets, which is acceptable for the deliberately tiny M0 bootstrap but is not the long-term kernel memory model.

The build also rejects absolute `R_68K_32` relocations in the final bootstrap ELF.

This lets stage-0 copy the image into an Exec-allocated block instead of relying on physical address 0x100000. As the kernel grows, AXAM v2 should replace this bootstrap constraint with an explicit relocation/load contract.
