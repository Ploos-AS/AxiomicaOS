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

    /*
     * Stage-0 enters with A0 = base of the allocated image and A1 = end of
     * its allocation. Use the tail of that allocation as the bootstrap stack;
     * no absolute/BSS address is required.
     */
    move.l  %a1,%sp
    andi.l  #0xfffffffc,%sp

    clr.l   -(%sp)
    clr.l   -(%sp)
    jsr     kmain

1:
    nop
    bra.s   1b

