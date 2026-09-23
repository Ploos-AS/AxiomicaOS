CC ?= gcc
AS := $(CC)
LD ?= ld

CFLAGS := -m32 -ffreestanding -fno-pie -fno-stack-protector -Wall -Wextra -Werror -O2
LDFLAGS := -m elf_i386 -nostdlib -T linker.ld

BUILD := build
KERNEL := $(BUILD)/axiomicaos.kernel
ISO := $(BUILD)/axiomicaos.iso

.PHONY: all clean iso run

all: iso

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/boot.o: kernel/boot.S | $(BUILD)
	$(AS) -m32 -c $< -o $@

$(BUILD)/kernel.o: kernel/kernel.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(KERNEL): $(BUILD)/boot.o $(BUILD)/kernel.o linker.ld
	$(LD) $(LDFLAGS) -o $@ $(BUILD)/boot.o $(BUILD)/kernel.o

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
