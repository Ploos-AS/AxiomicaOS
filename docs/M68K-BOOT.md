# m68k boot contract

AxiomicaOS does not require a vendor operating system API after entry.

## Goals

- one architecture-level kernel entry contract
- machine BSP owns early hardware state
- no Kickstart, TOS or Macintosh System dependency in the kernel
- boot loaders may be machine-specific
- ROM images and proprietary operating-system files are never stored in this repository

## Initial Amiga path

The first m68k bring-up target is classic Amiga because the project already has emulator qualification infrastructure for that family.

The initial sequence is:

1. machine-specific loader or boot image establishes executable RAM
2. interrupts are masked
3. a private AxiomicaOS stack is established
4. control enters the common kernel
5. Amiga BSP disables unowned DMA/interrupt sources
6. native custom-chip drivers are initialized incrementally

The M0.2 scaffold already contains direct custom-register access and does not invoke AmigaOS APIs.

## Later machines

Atari, Macintosh, X68000, NeXT, Sun-3 and Apollo use the same architectural model with their own BSP and loader.
