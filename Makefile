CC ?= gcc
AS := $(CC)
LD ?= ld

CPPFLAGS := -Iinclude
CFLAGS := -m32 -ffreestanding -fno-pie -fno-stack-protector -Wall -Wextra -Werror -O2
LDFLAGS := -m elf_i386 -nostdlib -T linker.ld

BUILD := build
KERNEL := $(BUILD)/axiomicaos.kernel
ISO := $(BUILD)/axiomicaos.iso
OBJECTS := $(BUILD)/boot.o $(BUILD)/main.o $(BUILD)/platform.o

.PHONY: all clean iso run

all: iso

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/boot.o: arch/x86/boot.S | $(BUILD)
	$(AS) -m32 -c $< -o $@

$(BUILD)/main.o: kernel/main.c include/axiomica/platform.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD)/platform.o: machines/pc/platform.c include/axiomica/platform.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(KERNEL): $(OBJECTS) linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJECTS)

iso: $(KERNEL)
	rm -rf $(BUILD)/iso
	mkdir -p $(BUILD)/iso/boot/grub
	cp $(KERNEL) $(BUILD)/iso/boot/axiomicaos.kernel
	cp iso/boot/grub/grub.cfg $(BUILD)/iso/boot/grub/grub.cfg
	grub-mkrescue -o $(ISO) $(BUILD)/iso >/dev/null

run: iso
	qemu-system-i386 -cdrom $(ISO) -serial stdio -display none -no-reboot -no-shutdown

clean:
	rm -rf $(BUILD)
