/*
 * Minimal m68k exception-vector scaffold.
 *
 * Real vector installation is machine/boot-environment dependent and will be
 * enabled once each BSP owns its vector table and early memory map.
 */

    .text
    .globl ax_m68k_default_exception
ax_m68k_default_exception:
1:
    nop
    bra.s 1b
