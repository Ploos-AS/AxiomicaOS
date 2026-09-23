#ifndef AXIOMICA_M68K_H
#define AXIOMICA_M68K_H

#include <axiomica/types.h>

enum ax_m68k_cpu {
    AX_M68K_68000 = 0,
    AX_M68K_68010,
    AX_M68K_68020,
    AX_M68K_68030,
    AX_M68K_68040,
    AX_M68K_68060
};

struct ax_m68k_caps {
    enum ax_m68k_cpu cpu;
    ax_u8 has_mmu;
    ax_u8 has_fpu;
    ax_u8 has_split_cache;
};

void ax_m68k_exception_vectors_init(void);
void ax_m68k_idle(void);

#endif
