# Amiga bootstrap handoff ABI

Stage-0 transfers control to the relocatable kernel with:

- A0: base address of the loaded kernel image
- A1: end of the reserved kernel region, used as the initial downward-growing stack top
- interrupts disabled

The kernel entry aligns A1 to four bytes and installs it as SP before calling C code. This removes the previous absolute reference to a 16 KiB BSS stack and keeps the entry path position-independent.

This ABI is private to the M0 bootstrap and may be replaced by a structured boot-information block later.
