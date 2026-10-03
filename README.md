# AxiomicaOS

**A modern personal-computer operating system built from first principles.**

AxiomicaOS is an independent operating-system project inspired by the best ideas of classic AmigaOS: responsive multitasking, message-oriented design, a powerful command line, composable system components, and a user-centric desktop.

## M0 — Kernel Foundation

M0 establishes the first executable foundation: Multiboot2 boot, freestanding kernel, serial/VGA output, QEMU qualification, GitHub Actions qualification, and initial architecture documentation.

## Project status

**M0.3 — Amiga boot bring-up: static qualification complete; runtime qualification pending.**

The Amiga/68000 path builds a freestanding kernel, native boot block, AXAM payload and 880 KiB ADF. Static qualification is established in CI. M0.3 is not complete until a controlled A500/68000 FS-UAE runtime host reaches both the kernel-entry and halt oracles and retains the resulting evidence artifact.

See [docs/M0.3-CHECKLIST.md](docs/M0.3-CHECKLIST.md) for the release gates.

## Design principles

- Responsive by default
- Message-oriented architecture
- Composable components
- User control
- CLI and GUI parity
- Protected by default
- Stable interfaces
- Observable failures
- Small trusted core
- No accidental complexity

## Architecture direction

Motorola 68k is a first-class architecture. AxiomicaOS separates CPU architecture code from machine/BSP code and targets native machine personalities while keeping common OS interfaces portable.

Current and roadmap machine families include Amiga, Atari, Macintosh 68k, Sharp X68000, NeXT 68k, Sun-3 and Apollo Domain.

Long-term target: a self-hosting, multi-architecture personal-computer OS with an Amiga-inspired user experience and modern protected architecture.

## License

MIT unless a subdirectory or component states otherwise.
