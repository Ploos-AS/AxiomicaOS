# Stock FS-UAE debugger adapter

Stock FS-UAE includes the UAE console debugger. FS-UAE documents `Mod+D` as the debugger shortcut, and the underlying UAE debugger provides memory inspection commands.

For M0.3 the useful observations are:

    m bfe001
    m dff180

Capture the debugger transcript, then normalize it:

    python3 tools/amiga/fsuae-debugger-adapter.py fsuae-debug.txt runtime.trace
    sh tools/amiga/adapter-common.sh runtime.trace fs-uae

This is the first concrete FS-UAE adapter path. It deliberately parses actual debugger memory output rather than screenshots.

## Automation boundary

Stock FS-UAE's documented debugger is interactive. The remaining automation work is a PTY/input driver that enters the debugger after boot, submits the two memory-dump commands, captures their output and exits cleanly. Until that driver is qualified, this adapter is transcript-driven and M0.3 remains runtime-pending.
