ENTRY(axiomica_amiga_stage0)
SECTIONS
{
    . = 0;
    .text : { *(.text*) *(.rodata*) }
    /DISCARD/ : { *(.data*) *(.bss*) *(COMMON) *(.comment) *(.note*) }
}
