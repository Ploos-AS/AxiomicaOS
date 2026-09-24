/*
 * AxiomicaOS Amiga stage-0 loader, 68000 baseline.
 *
 * ROM/Exec is used only as the initial disk transport. Once the complete
 * AXAM payload has been validated and copied, control is transferred to the
 * freestanding AxiomicaOS entry point.
 */

    .text
    .globl axiomica_amiga_stage0
    .type axiomica_amiga_stage0,@function

.set _LVODoIO,    -456
.set _LVOAllocMem, -198
.set _LVOFreeMem,  -210
.set IO_ERROR,   31
.set IO_COMMAND, 28
.set IO_LENGTH,  36
.set IO_DATA,    40
.set IO_OFFSET,  44
.set CMD_READ,   2

.set AXAM_DISK_OFFSET, 1024
.set AXAM_HEADER_SIZE, 32
.set MAX_PAYLOAD,      0x00070000
.set MEMF_ANY,          0
.set MEMF_CHIP,         2

axiomica_amiga_stage0:
    /*
     * Amiga boot-block ABI enters executable code at byte 12 of the
     * 1024-byte block. A6 carries SysBase and A1 the boot I/O request.
     */
    /* Native visual marker: stage-0 has gained control. */
    move.w  #0x0002,0x00dff180
    move.l  %a1,%a2
    /* Allocate one contiguous block for kernel + 512-byte disk scratch.
     * Stage-0 must not assume a physical RAM address on classic Amiga.
     */
    /* Kernel may live in any public RAM, but pre-V36 trackdisk requires
     * io_Data in Chip RAM. Keep the DMA bounce sector separate.
     */
    move.l  #MAX_PAYLOAD+4,%d0
    move.l  #MEMF_ANY,%d1
    jsr     _LVOAllocMem(%a6)
    tst.l   %d0
    beq     stage0_fail
    move.l  %d0,%a3                 /* kernel allocation base */
    move.l  %d0,%a4
    addq.l  #4,%a4                  /* private handoff prefix */

    move.l  #512,%d0
    move.l  #MEMF_CHIP,%d1
    jsr     _LVOAllocMem(%a6)
    tst.l   %d0
    beq     stage0_fail_kernel
    move.l  %d0,%a5                 /* trackdisk DMA bounce sector */
    move.l  %a5,%a0

    /* Read the first AXAM sector. */
    move.w  #CMD_READ,IO_COMMAND(%a2)
    move.l  #512,IO_LENGTH(%a2)
    move.l  %a0,IO_DATA(%a2)
    move.l  #AXAM_DISK_OFFSET,IO_OFFSET(%a2)
    bsr     stage0_doio
    tst.l   %d0
    bne     stage0_fail_both

    cmpi.l  #0x4158414d,(%a0)       /* AXAM */
    bne     stage0_fail_both
    cmpi.l  #1,4(%a0)
    bne     stage0_fail_both
    cmpi.l  #AXAM_HEADER_SIZE,8(%a0)
    bne     stage0_fail_both
    /* AXAM v1 load-address field is advisory for this relocatable stage-0. */

    move.l  16(%a0),%d6             /* payload bytes */
    beq     stage0_fail_both
    cmpi.l  #MAX_PAYLOAD,%d6
    bhi     stage0_fail_both
    move.l  20(%a0),%d7             /* expected additive checksum */

    /*
     * The payload starts 32 bytes into the first AXAM sector. Copy those
     * bytes, then read following disk sectors into the bounce buffer.
     */
    lea     32(%a0),%a3
    move.l  %d6,%d5
    move.l  #AXAM_DISK_OFFSET+512,%d4
    clr.l   %d3                     /* checksum */

    move.l  %d5,%d2
    cmpi.l  #480,%d2
    bls.s   1f
    move.l  #480,%d2
1:
    bsr     stage0_copy_bytes
    sub.l   %d2,%d5
    beq.s   stage0_verify

stage0_read_loop:
    move.l  %a5,%a0
    move.w  #CMD_READ,IO_COMMAND(%a2)
    move.l  #512,IO_LENGTH(%a2)
    move.l  %a0,IO_DATA(%a2)
    move.l  %d4,IO_OFFSET(%a2)
    bsr     stage0_doio
    tst.l   %d0
    bne.s   stage0_fail_both

    add.l   #512,%d4
    move.l  %d5,%d2
    cmpi.l  #512,%d2
    bls.s   2f
    move.l  #512,%d2
2:
    move.l  %a0,%a3
    bsr     stage0_copy_bytes
    sub.l   %d2,%d5
    bne.s   stage0_read_loop

stage0_verify:
    cmp.l   %d7,%d3
    bne.s   stage0_fail_both

    /* Firmware/Exec dependency ends here. */
    /*
     * Amiga bootblock success ABI requires D0=0 and A0=completion entry.
     * Strap frees boot resources and closes trackdisk before invoking A0.
     */
    move.l  %a4,%a0
    move.l  %a3,%d0
    add.l   #MAX_PAYLOAD+4,%d0
    move.l  %d0,-4(%a4)            /* private future stack top */
    moveq   #0,%d0
    rts

stage0_fail_both:
    move.l  %a5,%a1
    move.l  #512,%d0
    jsr     _LVOFreeMem(%a6)
stage0_fail_kernel:
    move.l  %a3,%a1
    move.l  #MAX_PAYLOAD+4,%d0
    jsr     _LVOFreeMem(%a6)
stage0_fail:
    /* Red makes loader failure distinguishable from kernel entry. */
    move.w  #0x0f00,0x00dff180
    moveq   #-1,%d0
    rts

/* Return D0=0 on success, -1 on I/O error. Preserves our A2 request pointer. */
stage0_doio:
    move.l  %a2,%a1
    jsr     _LVODoIO(%a6)
    tst.b   IO_ERROR(%a2)
    bne.s   3f
    moveq   #0,%d0
    rts
3:
    moveq   #-1,%d0
    rts

/*
 * Copy D2 bytes A3 -> A4 and accumulate unsigned byte values in D3.
 * D2 is preserved so the caller can update its remaining byte count.
 */
stage0_copy_bytes:
    move.l  %d2,%d1
    beq.s   5f
4:
    moveq   #0,%d0
    move.b  (%a3)+,%d0
    move.b  %d0,(%a4)+
    add.l   %d0,%d3
    subq.l  #1,%d1
    bne.s   4b
5:
    rts

