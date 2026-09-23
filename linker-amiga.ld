ENTRY(_axiomica_amiga_start)

SECTIONS
{
    . = 0x00100000;

    .text : ALIGN(4)
    {
        *(.text*)
    }

    .rodata : ALIGN(4) { *(.rodata*) }
    .data : ALIGN(4) { *(.data*) }
    .bss : ALIGN(4) { *(COMMON) *(.bss*) }

    /DISCARD/ : { *(.comment) *(.note*) }
}
