# Runtime host setup

The reference host is a dedicated Debian-family Linux x86-64 machine or VM.

## 1. Install dependencies

    sudo tools/amiga/install-runtime-host-debian.sh

## 2. Place the ROM outside the runner workspace

Create an operator-controlled directory, copy a legally obtained A500-compatible ROM there, and restrict permissions to the runner service account. Do not add the ROM to Git, Actions cache, artifacts, container images or repository secrets.

## 3. Configure the service environment

Use `tools/amiga/runtime-host.env.example` as a template. The important variable is `AXIOMICA_KICKSTART_ROM`.

## 4. Register the GitHub runner

Register a self-hosted Linux x64 runner for the AxiomicaOS repository and give it the custom label:

    axiomica-amiga-runtime

Keep the default `self-hosted`, `linux` and `x64` labels because the workflow requires all four.

## 5. Verify provisioning

From a repository checkout under the same service account:

    tools/amiga/check-runtime-host.sh

Expected final line:

    M0.3 RUNTIME HOST READY

## 6. Run qualification

Dispatch the `Amiga runtime qualification` workflow. A host-ready result is not itself qualification; M0.3 becomes runtime PASS only when the emulator evidence verifier succeeds.
