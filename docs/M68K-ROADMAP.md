# m68k Platform Roadmap

Motorola 68k is a first-class AxiomicaOS architecture, not a legacy compatibility target.

## Principle

**Same OS, native hardware personality.**

Portable applications use common AxiomicaOS interfaces. Platform-aware software may use explicitly exposed native facilities where doing so adds value. AxiomicaOS should abstract enough to make software portable without abstracting away what makes each machine interesting.

## CPU targets

- MC68000
- MC68010
- MC68020
- MC68030
- MC68040
- MC68060

Memory protection and other facilities are capability-dependent. A 68000-class machine remains a supported design target even though it cannot provide the same isolation guarantees as MMU-equipped systems.

## Initial historical machine families

### Commodore Amiga
- A1000
- A500/A500+
- A600
- A2000
- A3000
- A1200
- A4000
- CDTV
- CD32
- accelerated 68020/030/040/060 systems

Native facilities include the Amiga custom-chip families, blitter, copper, sprites, CIA and Zorro where present.

### Atari
- ST/STF/STE
- Mega ST
- TT030
- Falcon030

Native facilities include Shifter/STE video, YM2149, DMA, Atari Blitter, MFP and Falcon Videl/DSP where present.

### Apple Macintosh 68k
Initial focus spans representative compact Mac, Macintosh II, LC/Centris and Quadra systems.

Native facilities may include VIA, SCC, ADB, SCSI, NuBus and machine-specific video hardware.

### Sharp X68000
- X68000 family
- X68000 XVI
- X68030

Native support should exploit the platform's graphics, sprites, scrolling, FM/ADPCM audio, DMA and other X68000-specific facilities rather than treating the machine as a generic 68k computer.

### NeXT 68k
- NeXT Computer
- NeXTcube
- NeXTstation
- NeXTstation Color

### Sun-3
Representative Sun-3 workstations form the initial Sun m68k target family.

### Apollo Domain
Apollo Domain 68k systems are roadmap targets, subject to sufficient documentation and emulator or hardware qualification capability.

## Architecture layout

    arch/
      m68k/
        cpu/
        mmu/
        exceptions/
        context/
      machines/
        amiga/
        atari/
        mac68k/
        x68000/
        next68k/
        sun3/
        apollo/

CPU architecture code must remain separate from machine/BSP code.

## Portable versus native APIs

Portable software should target common facilities such as graphics, audio, input, storage and IPC.

Platform-specific APIs may expose facilities such as:

- Amiga copper/blitter
- Atari/Falcon DSP and video features
- X68000 sprite/video/audio facilities
- Macintosh bus and machine facilities

Native APIs must be namespaced and capability-discoverable so applications can provide portable fallbacks.

## Qualification policy

A platform is not considered supported merely because it compiles. Each supported machine profile should eventually have reproducible emulator and/or real-hardware boot qualification.

The runtime infrastructure for Amiga, Atari and future Macintosh/m68k targets should be reused where practical.

## Bring-up status

- **M0.1:** architecture/machine separation established.
- **M0.2:** common m68k types/capabilities and bare-metal Amiga BSP scaffold established.
- Next: cross-build qualification, native Amiga early debug output, deterministic boot image and emulator boot qualification.
