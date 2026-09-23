#include <axiomica/platform.h>
#include "hardware.h"

/*
 * First bare-metal Amiga BSP scaffold.
 *
 * This code deliberately does not call Kickstart or AmigaOS. The boot path
 * will eventually enter AxiomicaOS directly with machine state described by
 * our own boot contract.
 */

void platform_early_init(void)
{
    /* Disable custom-chip DMA and interrupts until handlers exist. */
    AMIGA_DMACON = 0x7FFFu;
    AMIGA_INTENA = 0x7FFFu;
    AMIGA_INTREQ = 0x7FFFu;

    /* Visible proof of native custom-chip access: dark blue background. */
    AMIGA_COLOR00 = AMIGA_COLOR_KERNEL;
    AMIGA_CIAA_PRA = 0xA5u;
}

void platform_console_write(const char *text)
{
    /*
     * M0.2 will provide a native early debug transport. Keep the interface
     * functional now without depending on firmware/OS services.
     */
    (void)text;
}

void platform_halt(void)
{
    AMIGA_COLOR00 = AMIGA_COLOR_HALTED;
    AMIGA_CIAA_PRA = 0x5Au;
    for (;;) {
        __asm__ volatile ("nop");
    }
}
