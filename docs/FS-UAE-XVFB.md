# Unattended FS-UAE qualification

On Linux/X11 the M0.3 reference adapter can be wrapped in Xvfb. The runner launches a virtual display, starts stock FS-UAE, waits for its window, injects the dedicated debugger action, and relies on the existing debugger runner to capture and verify the native oracle.

Required host tools: FS-UAE, Xvfb, xdotool and coreutils timeout.

    AXIOMICA_KICKSTART_ROM=/legal/local/rom \
      tools/amiga/qualify-fsuae-xvfb.sh

The ROM remains external. The runner is fail-closed: missing dependencies, missing ROM/ADF, early emulator exit, activation timeout, runtime timeout, missing oracle or verifier failure all produce a non-zero exit status.

This establishes the unattended adapter design. Runtime qualification is not claimed until this runner has completed successfully against a real emulator invocation.
