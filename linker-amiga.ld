ENTRY(_axiomica_amiga_start)

SECTIONS
{
    . = 0;

    .text : ALIGN(4)
    {
        KEEP(*(.text.entry))
        *(.text*)
    }

    .rodata : ALIGN(4) { *(.rodata*) }
    .data : ALIGN(4) { *(.data*) }
    .bss : ALIGN(4) { *(COMMON) *(.bss*) }

    /DISCARD/ : { *(.comment) *(.note*) }
}
