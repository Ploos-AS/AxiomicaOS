#ifndef AXIOMICA_AMIGA_HARDWARE_H
#define AXIOMICA_AMIGA_HARDWARE_H

#include <axiomica/types.h>

/* Classic Amiga custom register block. */
#define AMIGA_CUSTOM_BASE 0x00DFF000u

#define AMIGA_REG16(offset)     (*(volatile ax_u16 *)(AMIGA_CUSTOM_BASE + (offset)))

#define AMIGA_DMACONR AMIGA_REG16(0x002)
#define AMIGA_VPOSR   AMIGA_REG16(0x004)
#define AMIGA_VHPOSR  AMIGA_REG16(0x006)
#define AMIGA_INTENAR AMIGA_REG16(0x01C)
#define AMIGA_INTREQR AMIGA_REG16(0x01E)
#define AMIGA_DMACON  AMIGA_REG16(0x096)
#define AMIGA_INTENA  AMIGA_REG16(0x09A)
#define AMIGA_INTREQ  AMIGA_REG16(0x09C)
#define AMIGA_COLOR00 AMIGA_REG16(0x180)

/* CIA-A parallel port data register: useful as a machine-visible oracle. */
#define AMIGA_CIAA_PRA (*(volatile ax_u8 *)0x00BFE001u)

/* Relocatable RAM oracle for unattended emulator qualification. */
#define AXIOMICA_AMIGA_ORACLE_MAGIC 0x41584F52u /* AXOR */
struct axiomica_amiga_oracle {
    ax_u32 magic;
    ax_u32 image_base;
    volatile ax_u8 state;
    ax_u8 reserved[3];
};
extern volatile struct axiomica_amiga_oracle axiomica_amiga_oracle;

/* Deterministic native proof-of-life colours for emulator/hardware tests. */
#define AMIGA_COLOR_BOOTING 0x0002u
#define AMIGA_COLOR_KERNEL  0x00F0u
#define AMIGA_COLOR_HALTED  0x000Fu

#endif
