# Amiga bootstrap handoff ABI

M0.3 uses the native Amiga boot-block completion convention rather than jumping
directly from stage-0 into the kernel.

## Boot-block completion

On successful loading and validation, stage-0 returns to the ROM/strap code with:

- `D0 = 0`
- `A0 = image_base`, which is also `_axiomica_amiga_start`
- the generated kernel image guarantees that the completion entry is at offset zero

The ROM/strap code may then release its boot resources and close the boot device
before invoking the completion entry. The kernel therefore does **not** depend on
the boot-time `A1` I/O-request value surviving the handoff.

## Private bootstrap prefix and stack

The loader allocates one block containing:

1. a 4-byte private prefix,
2. the exact AXAM payload,
3. an 8 KiB bootstrap stack.

The private word immediately before the image (`image_base - 4`) contains the
aligned top of that reserved stack. The completion entry finds its own image base
PC-relatively, reads this value, installs it as `SP`, disables interrupts, and
then calls the architecture-independent `kmain`.

The 512-byte trackdisk bounce buffer is a separate `MEMF_CHIP` allocation and
is released after the payload checksum succeeds, before stage-0 returns success.

## Scope

This is a private M0.3 bootstrap ABI. A later milestone may replace the prefix
with a versioned boot-information structure, but runtime qualification must first
prove this minimal contract on the A500/68000 profile.
