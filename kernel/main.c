#include <stdint.h>
#include <axiomica/platform.h>

void kmain(uint32_t boot_magic, uint32_t boot_info)
{
    (void)boot_info;
    platform_early_init();

    platform_console_write("AxiomicaOS M0.1\n");
    platform_console_write("Architecture-independent kernel entry online.\n");
    platform_console_write("Multiboot2 magic: ");
    platform_console_write(boot_magic == 0x36D76289u ? "valid\n" : "invalid\n");
    platform_console_write("Same OS, native hardware personality.\n");

    platform_halt();
}
