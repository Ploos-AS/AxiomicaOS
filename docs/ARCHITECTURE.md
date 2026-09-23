# AxiomicaOS Architecture

## M0

Firmware/bootloader -> Multiboot2 -> boot.S/stack -> kmain() -> serial/VGA.

The current bootstrap executes in 32-bit protected mode. This is staging architecture only; later milestones will transition to protected x86-64 execution.

## Planned direction

Applications -> GUI/CLI/SDK -> system services -> IPC/VFS/device interfaces -> kernel -> hardware.

The kernel should remain small; filesystems, networking, graphics, input, audio, package management and desktop services should remain outside the trusted core where practical.
