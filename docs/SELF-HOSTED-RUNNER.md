# Self-hosted Amiga runtime runner

Use a dedicated Linux x86-64 host for the `axiomica-amiga-runtime` label.

## Host contract

The runner must pass:

    tools/amiga/check-runtime-host.sh

The check deliberately does not print the ROM path, hash or contents.

## Security boundary

Treat pull-request code as untrusted. The ROM-bearing runtime runner should execute trusted branch/repository workflows only. Do not expose this runner to arbitrary fork PR jobs.

Keep the ROM outside the GitHub Actions workspace and configure `AXIOMICA_KICKSTART_ROM` in the runner service environment. Runtime artifacts may contain Axiomica-generated images and evidence only.

## Qualification

A green host check means only that the host is provisioned. It is not a runtime PASS. Runtime PASS still requires the generated ADF to reach the native kernel oracle under FS-UAE.
