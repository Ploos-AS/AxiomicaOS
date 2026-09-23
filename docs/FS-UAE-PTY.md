# FS-UAE interactive debugger capture

The first automation layer for stock FS-UAE is intentionally conservative.

1. Boot the generated ADF with `run-fsuae.sh`.
2. Enter the UAE debugger using FS-UAE's debugger shortcut.
3. Attach `fsuae-pty.py` to that debugger terminal.
4. The driver issues read-only memory dumps for CIA-A PRA and COLOR00.
5. Feed the captured transcript to `qualify-fsuae-transcript.sh`.

The driver never writes emulated memory and never changes the ADF.

This is a stepping stone toward a fully unattended launcher. A runtime PASS still requires a real captured transcript from a running emulator; synthetic traces are not qualification evidence.
