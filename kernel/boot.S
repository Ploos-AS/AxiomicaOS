.set MB2_MAGIC, 0xE85250D6
.set MB2_ARCH, 0
.set MB2_HEADER_LEN, (mb2_end - mb2_start)
.set MB2_CHECKSUM, -(MB2_MAGIC + MB2_ARCH + MB2_HEADER_LEN)

.section .multiboot
.align 8
mb2_start:
    .long MB2_MAGIC
    .long MB2_ARCH
    .long MB2_HEADER_LEN
    .long MB2_CHECKSUM
    .short 0
    .short 0
    .long 8
mb2_end:

.section .bss
.align 16
stack_bottom:
    .skip 16384
stack_top:

.section .text
.global _start
.type _start, @function
.extern kmain

_start:
    cli
    mov $stack_top, %esp
    xor %ebp, %ebp
    push %ebx
    push %eax
    call kmain

1:
    cli
    hlt
    jmp 1b
