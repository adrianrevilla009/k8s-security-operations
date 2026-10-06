# falco-runtime-security

A Falco rules file, `orders_rules.yaml`, with two rules for the `orders` namespace and a structural checker.

## Goal
Show how Falco macros, lists and rules combine to detect suspicious behaviour inside containers.

## Run it
```
pip install pyyaml
python3 falco-runtime-security/verify.py
```
Expected: `ok: 2 rules, 3 macros, 1 lists`.

## What it proves
- `Shell Spawned in Orders Container` (WARNING) fires when a shell binary (`bash`, `sh`, `zsh`, `dash`, `ash`) starts with a TTY in the `orders` namespace.
- `Read Sensitive File in Orders Container` (CRITICAL) fires when `/etc/shadow`, `/etc/sudoers` or `/root/.ssh/authorized_keys` is opened for reading there.
- Both rules build on macros (`container_started`, `open_read_in_container`, `shell_binaries`) and the `sensitive_files` list; `verify.py` checks every rule has desc, condition, output and a valid priority, uses a macro, and references a list that exists.

## Trade-offs
- Not run end to end: Falco is not installed here, so the rules were never loaded and the condition syntax is not validated by Falco itself (`falco --validate` would do that).
- The `proc.tty != 0` filter ignores non-interactive shells, such as `kubectl exec` without `-t`.
- Rules need a Falco driver on every node and tuning for noise.

## When not to use it
- For preventing the action: Falco only alerts; use admission policy or seccomp to block.
