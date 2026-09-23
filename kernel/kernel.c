#include <stdint.h>

#define VGA_MEMORY ((volatile uint16_t *)0xB8000)
#define VGA_WIDTH 80
#define VGA_HEIGHT 25
#define VGA_ATTRIBUTE 0x07

static volatile uint16_t *const vga = VGA_MEMORY;
static uint16_t cursor;

static void vga_putc(char c)
{
    if (c == '\n') {
        cursor = (uint16_t)(((cursor / VGA_WIDTH) + 1) * VGA_WIDTH);
        return;
    }
    vga[cursor++] = (uint16_t)VGA_ATTRIBUTE << 8 | (uint8_t)c;
    if (cursor >= VGA_WIDTH * VGA_HEIGHT) cursor = 0;
}

static void vga_write(const char *s)
{
    while (*s) vga_putc(*s++);
}

static void serial_init(void)
{
    volatile uint8_t *p = (volatile uint8_t *)0x3F8;
    p[1] = 0x00;
    p[3] = 0x80;
    p[0] = 0x03;
    p[1] = 0x00;
    p[3] = 0x03;
    p[2] = 0xC7;
    p[4] = 0x0B;
}

static void serial_putc(char c)
{
    volatile uint8_t *status = (volatile uint8_t *)0x3FD;
    volatile uint8_t *data = (volatile uint8_t *)0x3F8;
    while ((*status & 0x20u) == 0u) {}
    *data = (uint8_t)c;
}

static void serial_write(const char *s)
{
    while (*s) serial_putc(*s++);
}

void kmain(uint32_t multiboot_magic, uint32_t multiboot_info)
{
    (void)multiboot_info;
    serial_init();

    vga_write("AxiomicaOS M0\n");
    vga_write("Kernel foundation online.\n");

    serial_write("AxiomicaOS M0\n");
    serial_write("Kernel foundation online.\n");
    serial_write("Multiboot2 magic: ");
    serial_write(multiboot_magic == 0x36D76289u ? "valid\n" : "invalid\n");
    serial_write("Built from first principles.\n");

    for (;;) __asm__ volatile ("hlt");
}
