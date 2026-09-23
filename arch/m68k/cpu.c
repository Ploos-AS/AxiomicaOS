#include <axiomica/m68k.h>

void ax_m68k_idle(void)
{
    /*
     * Keep the generic kernel independent of the exact m68k CPU.
     * A later CPU backend may use STOP when interrupt state is ready.
     */
    for (;;) {
        __asm__ volatile ("nop");
    }
}
