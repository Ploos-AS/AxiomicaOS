# Amiga floppy bring-up image

M0.3 introduces a deterministic 880 KiB raw floppy image used to develop the first AxiomicaOS Amiga loader.

The image currently acts as a **loader-development container**, not yet as a bootable AmigaDOS disk. It contains no Kickstart, Workbench or other proprietary operating-system material.

## Layout

- bytes 0..1023: reserved stage-0/metadata area
- byte 1024 onward: AXAM payload
- remaining bytes: zero-filled

The temporary metadata magic is `AXDF`. Once native stage-0 code is ready, the first two sectors will contain the actual Amiga boot block while retaining enough metadata for deterministic CI validation.

## Goal

The stage-0 loader must:

1. execute on a 68000 baseline
2. locate and validate the embedded AXAM payload
3. place it at the requested address
4. quiesce hardware needed for safe kernel entry
5. transfer control to `_axiomica_amiga_start`
6. require no AmigaOS API after kernel entry

Boot qualification will be done using legal user/runtime ROM configuration; ROM files are never committed here.
