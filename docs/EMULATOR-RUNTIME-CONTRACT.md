# Emulator runtime automation contract

An emulator adapter qualifies M0.3 by booting the exact CI-produced ADF and
observing native machine state without modifying the kernel or disk image.

## Required machine-readable oracle

Runtime PASS requires both CIA-A PRA observations at `0xBFE001`:

- `0xA5` — the AxiomicaOS kernel entry point was reached.
- `0x5A` — the kernel reached the M0.3 halt point.

Both phases are required. Observing only the final value is not sufficient
evidence that the adapter captured the complete qualification sequence.

## Visual corroboration

`COLOR00` at `0xDFF180` remains a useful human-visible diagnostic:

- `0x002` — stage-0 entered.
- `0x0F0` — kernel entered.
- `0x00F` — kernel halt.
- `0xF00` — stage-0 failure.

COLOR00 is corroborating/debug evidence only and cannot by itself produce a
runtime PASS.

Failure, timeout, missing oracle phases, parser failure, emulator process
failure, or missing persisted evidence must not be converted into PASS.

Adapters may use an emulator debugger, monitor, trace facility, or a small
external harness. FS-UAE is the reference path; Amiberry and FellowNG can
implement the same machine-readable oracle later.
