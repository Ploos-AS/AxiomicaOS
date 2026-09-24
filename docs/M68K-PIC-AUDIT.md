# Final m68k PIC audit

The M0.3 Amiga payload is converted from ELF to a raw flat binary. Therefore no ELF relocation records may remain for a runtime loader to process.

The build now checks the final linked ELF, not just selected object relocations. It rejects:

- any remaining `R_68K_*` relocation
- any undefined symbol
- an unexpected ELF machine type

PC-relative references such as `R_68K_PC16` are valid while linking, but they must be fully resolved before the flat binary is emitted. GNU binutils defines the m68k direct and PC-relative relocation families separately.

A passing audit means the image is structurally suitable for relocation as a flat PC-relative bootstrap image; it is not a substitute for runtime qualification.
