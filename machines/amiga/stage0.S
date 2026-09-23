/*
 * AxiomicaOS Amiga stage-0 boot block.
 *
 * The Amiga ROM boot process enters a boot block with ExecBase in A6 and a
 * boot I/O request in A1. Stage-0 uses the ROM-provided device I/O only to
 * fetch the remaining sectors, then transfers to the freestanding kernel.
 * No AmigaOS service is required after kernel entry.
 *
 * M0.3 keeps this loader intentionally tiny and 68000-compatible.
 */

    .text
    .globl axiomica_amiga_stage0
    .type axiomica_amiga_stage0,@function

/* Exec LVOs used only by stage-0. */
.set _LVODoIO, -456

/* IORequest offsets used by trackdisk.device. */
.set IO_COMMAND, 28
.set IO_ACTUAL, 32
.set IO_LENGTH, 36
.set IO_DATA, 40
.set IO_OFFSET, 44

.set CMD_READ, 2
.set PAYLOAD_DISK_OFFSET, 1024
.set LOAD_ADDRESS, 0x00100000
.set MAX_PAYLOAD, 0x000C0000

axiomica_amiga_stage0:
    move.l  %a1,%a2
    lea     stage0_sector_buffer,%a0

    /* Read first payload sector containing the AXAM header. */
    move.w  #CMD_READ,IO_COMMAND(%a2)
    move.l  #512,IO_LENGTH(%a2)
    move.l  %a0,IO_DATA(%a2)
    move.l  #PAYLOAD_DISK_OFFSET,IO_OFFSET(%a2)
    move.l  %a2,%a1
    jsr     _LVODoIO(%a6)
    tst.b   31(%a2)
    bne.s   stage0_fail

    /* AXAM magic and fixed header fields. */
    cmpi.l  #0x4158414d,(%a0)
    bne.s   stage0_fail
    cmpi.l  #1,4(%a0)
    bne.s   stage0_fail
    cmpi.l  #32,8(%a0)
    bne.s   stage0_fail
    cmpi.l  #LOAD_ADDRESS,12(%a0)
    bne.s   stage0_fail

    move.l  16(%a0),%d6
    beq.s   stage0_fail
    cmpi.l  #MAX_PAYLOAD,%d6
    bhi.s   stage0_fail

    /*
     * Read the raw kernel payload, skipping the 32-byte AXAM header.
     * Trackdisk reads are sector based, so M0.3 uses a bounce buffer path;
     * the complete copy/checksum loop is the next qualification step.
     */
    moveq   #0,%d0
    rts

stage0_fail:
    moveq   #-1,%d0
    rts

    .bss
    .align 4
stage0_sector_buffer:
    .space 512
