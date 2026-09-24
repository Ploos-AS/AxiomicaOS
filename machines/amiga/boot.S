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
     * Strap invokes this completion entry after freeing boot resources.
     * Stage-0 stored the future stack-top immediately before this image.
     */
    lea     _axiomica_amiga_start(%pc),%a0
    move.l  -4(%a0),%a1
    andi.l  #0xfffffffc,%a1
    move.l  %a1,%sp

    clr.l   -(%sp)
    clr.l   -(%sp)
    jsr     kmain

1:
    nop
    bra.s   1b

