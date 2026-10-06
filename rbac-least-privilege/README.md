# rbac-least-privilege

A namespaced read-only Role bound to a ServiceAccount, with a script that lints the RBAC for common over-grants.

## Goal
Show a minimal RBAC set for a workload that only reads pods and config, and how to check that no one widened it.

## Run it
```
pip install pyyaml
python3 rbac-least-privilege/verify.py
```
Expected: `ok: 1 roles, 1 bindings, least privilege`.

## What it proves
- `rbac.yaml` grants `get`, `list`, `watch` on `pods` and `configmaps`, and `get` on `pods/log`, in the `orders` namespace only.
- The ServiceAccount sets `automountServiceAccountToken: false`, so a pod does not receive a token unless it opts in.
- `verify.py` fails on wildcards, any rule touching `secrets`, the verbs `escalate`, `bind` and `impersonate`, a `cluster-admin` roleRef, a dangling roleRef or subject, and any ClusterRoleBinding.

## Trade-offs
- The linter only reads `Role` and `RoleBinding`; ClusterRoles are not inspected.
- Not run end to end: no `kubectl auth can-i` check against a live cluster.
- Opting out of token mounting means a pod that calls the API must set it explicitly.

## When not to use it
- To audit a live cluster: use a tool that reads the actual bindings, not a single manifest file.
