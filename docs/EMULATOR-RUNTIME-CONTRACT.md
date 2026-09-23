# Emulator runtime automation contract

An emulator adapter qualifies M0.3 by booting the exact CI-produced ADF and observing native machine state.

Required terminal condition:

- CIA-A PRA at 0xBFE001 equals 0x5A
- COLOR00 at 0xDFF180 equals 0x00F

Failure/timeout must not be converted into PASS.

Adapters may use an emulator debugger, monitor, trace facility, or a small external harness. They must not patch the kernel or disk image during qualification.

This contract intentionally separates AxiomicaOS from a particular emulator. FS-UAE is the reference path; Amiberry and FellowNG can implement the same oracle later.
