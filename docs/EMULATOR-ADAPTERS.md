# Emulator adapters

Adapters are deliberately thin. Their only emulator-specific responsibility is to boot the unmodified ADF and obtain observations of the runtime oracle.

The common verifier owns PASS/FAIL semantics.

An adapter trace should normalize observations as:

    bfe001 = a5
    dff180 = 0f0
    bfe001 = 5a
    dff180 = 00f

`trace-oracle.py` can append normalized observations when an emulator integration obtains values in another form. `adapter-common.sh` then verifies the trace and emits the qualification result.

## Reference order

1. FS-UAE
2. Amiberry
3. FellowNG
4. real-hardware probe

An adapter is not considered implemented merely because a launch script exists; it must actually obtain the oracle from the running machine.
