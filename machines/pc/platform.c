#include <stdint.h>
#include <axiomica/platform.h>

#define VGA_MEMORY ((volatile uint16_t *)0xB8000)
#define VGA_WIDTH 80
#define VGA_HEIGHT 25
#define VGA_ATTRIBUTE 0x07

static volatile uint16_t *const vga = VGA_MEMORY;
static uint16_t cursor;

static inline void outb(uint16_t port, uint8_t value)
{
    __asm__ volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}

static inline uint8_t inb(uint16_t port)
{
    uint8_t value;
    __asm__ volatile ("inb %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}

static void vga_putc(char c)
{
    if (c == '\n') {
        cursor = (uint16_t)(((cursor / VGA_WIDTH) + 1) * VGA_WIDTH);
        return;
    }

    vga[cursor++] = ((uint16_t)VGA_ATTRIBUTE << 8) | (uint8_t)c;
    if (cursor >= VGA_WIDTH * VGA_HEIGHT) cursor = 0;
}

static void serial_putc(char c)
{
    while ((inb(0x3FD) & 0x20u) == 0u) {}
    outb(0x3F8, (uint8_t)c);
}

void platform_early_init(void)
{
    outb(0x3F9, 0x00);
    outb(0x3FB, 0x80);
    outb(0x3F8, 0x03);
    outb(0x3F9, 0x00);
    outb(0x3FB, 0x03);
    outb(0x3FA, 0xC7);
    outb(0x3FC, 0x0B);
}

void platform_console_write(const char *text)
{
    while (*text) {
        vga_putc(*text);
        if (*text == '\n') serial_putc('\r');
        serial_putc(*text++);
    }
}

void platform_halt(void)
{
    for (;;) {
        __asm__ volatile ("cli; hlt");
    }
}
