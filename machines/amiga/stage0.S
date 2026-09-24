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
.set STACK_SIZE,         8192

axiomica_amiga_stage0:
    move.w  #0x0002,0x00dff180
    move.l  %a1,%a2

    /* Pre-V36 trackdisk DMA buffer must be Chip RAM. */
    move.l  #512,%d0
    move.l  #MEMF_CHIP,%d1
    jsr     _LVOAllocMem(%a6)
    tst.l   %d0
    beq     stage0_fail
    move.l  %d0,%a5

    /* Read and validate the first AXAM sector before allocating the kernel. */
    move.w  #CMD_READ,IO_COMMAND(%a2)
    move.l  #512,IO_LENGTH(%a2)
    move.l  %a5,IO_DATA(%a2)
    move.l  #AXAM_DISK_OFFSET,IO_OFFSET(%a2)
    bsr     stage0_doio
    tst.l   %d0
    bne     stage0_fail_bounce

    cmpi.l  #0x4158414d,(%a5)
    bne     stage0_fail_bounce
    cmpi.l  #1,4(%a5)
    bne     stage0_fail_bounce
    cmpi.l  #AXAM_HEADER_SIZE,8(%a5)
    bne     stage0_fail_bounce
    tst.l   12(%a5)                 /* AXAM v1 relocatable load must be zero */
    bne     stage0_fail_bounce

    move.l  16(%a5),%d6
    beq     stage0_fail_bounce
    cmpi.l  #MAX_PAYLOAD,%d6
    bhi     stage0_fail_bounce
    move.l  20(%a5),%d7             /* expected checksum */

    /* Exact allocation: prefix + payload + reserved bootstrap stack. */
    move.l  %d6,%d0
    add.l   #STACK_SIZE+7,%d0       /* prefix + up to 3 bytes alignment */
    andi.l  #0xfffffffc,%d0
    move.l  %d0,%d5                 /* allocation size, preserved register */
    move.l  #MEMF_ANY,%d1
    jsr     _LVOAllocMem(%a6)
    tst.l   %d0
    beq     stage0_fail_bounce
    move.l  %d0,%a3                 /* allocation base */
    move.l  %d0,%a4
    addq.l  #4,%a4                  /* image base / completion entry */

    /* Save future stack top before A4 advances during copying. */
    move.l  %a3,%d0
    add.l   %d5,%d0
    andi.l  #0xfffffffc,%d0
    move.l  %d0,(%a3)

    /* Copy payload bytes already present in the first sector. */
    lea     32(%a5),%a0
    move.l  %d6,%d1                 /* remaining bytes */
    clr.l   %d3                     /* checksum */
    move.l  %d1,%d2
    cmpi.l  #480,%d2
    bls.s   1f
    move.l  #480,%d2
1:
    move.l  %a0,%a3
    bsr     stage0_copy_bytes
    sub.l   %d2,%d1
    move.l  #AXAM_DISK_OFFSET+512,%d4
    tst.l   %d1
    beq.s   stage0_verify

stage0_read_loop:
    move.w  #CMD_READ,IO_COMMAND(%a2)
    move.l  #512,IO_LENGTH(%a2)
    move.l  %a5,IO_DATA(%a2)
    move.l  %d4,IO_OFFSET(%a2)
    bsr     stage0_doio
    tst.l   %d0
    bne.s   stage0_fail_both
    add.l   #512,%d4
    move.l  %d1,%d2
    cmpi.l  #512,%d2
    bls.s   2f
    move.l  #512,%d2
2:
    move.l  %a5,%a3
    bsr     stage0_copy_bytes
    sub.l   %d2,%d1
    bne.s   stage0_read_loop

stage0_verify:
    cmp.l   %d7,%d3
    bne.s   stage0_fail_both

    /* Disk I/O is complete; release the Chip-RAM bounce buffer. */
    move.l  %a5,%a1
    move.l  #512,%d0
    jsr     _LVOFreeMem(%a6)

    /* A4 now points just past payload. Recover entry from allocation base. */
    move.l  %a4,%a0
    sub.l   %d6,%a0
    moveq   #0,%d0
    rts

stage0_fail_both:
    /* A4 points into the kernel block, so recover its base from size copied. */
    move.l  %a4,%a1
    sub.l   %d6,%a1
    subq.l  #4,%a1
    move.l  %d5,%d0
    jsr     _LVOFreeMem(%a6)
stage0_fail_bounce:
    move.l  %a5,%a1
    move.l  #512,%d0
    jsr     _LVOFreeMem(%a6)
stage0_fail:
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

