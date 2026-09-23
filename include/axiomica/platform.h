#ifndef AXIOMICA_PLATFORM_H
#define AXIOMICA_PLATFORM_H

void platform_early_init(void);
void platform_console_write(const char *text);
void platform_halt(void) __attribute__((noreturn));

#endif
