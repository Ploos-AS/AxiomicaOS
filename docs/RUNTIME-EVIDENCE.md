# Runtime evidence

AxiomicaOS keeps runtime evidence separate from build success.

Emulator adapters should emit a plain-text trace containing observed machine addresses and values. `verify-runtime-log.py` converts that trace into the canonical M0.3 runtime PASS/FAIL result.

Examples of acceptable observations include CIA-A PRA at `0xBFE001` and COLOR00 at `0xDFF180`. The adapter is responsible for obtaining these from the emulator without modifying the ADF or kernel.

This design lets FS-UAE, Amiberry, FellowNG and later real-hardware probes share one qualification verifier.
