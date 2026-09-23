/*
 * AxiomicaOS bare-metal Amiga entry scaffold.
 *
 * This is intentionally independent of Kickstart/AmigaOS APIs. A loader or
 * ROM-capable boot stage will establish RAM and stack before entering here.
 */

    .text
    .globl _axiomica_amiga_start
    .extern kmain

_axiomica_amiga_start:
    move.w  #0x2700,%sr
    lea     axiomica_amiga_stack_top,%sp

    clr.l   -(%sp)
    clr.l   -(%sp)
    jsr     kmain

1:
    nop
    bra.s   1b

    .bss
    .align  4
axiomica_amiga_stack:
    .space  16384
axiomica_amiga_stack_top:
