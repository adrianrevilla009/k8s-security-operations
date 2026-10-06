# pod-security-admission

Three namespaces labelled with Pod Security Admission levels, one compliant pod, one violating pod, and an offline checker.

## Goal
Show how PSA labels select a security level per namespace, and what a pod must declare to pass the `restricted` profile.

## Run it
```
pip install pyyaml
python3 pod-security-admission/verify.py
```
Expected: `ok: levels ['baseline', 'privileged', 'restricted'] - violating pod has 6 violations`.

## What it proves
- `namespaces.yaml` enforces `restricted` in `orders-restricted`, `baseline` in `orders-baseline` and `privileged` in `orders-system`; the first two also warn and audit at `restricted`.
- `compliant-pod.yaml` passes the checker's mini `restricted` evaluator: non-root, RuntimeDefault seccomp, no privilege escalation, all capabilities dropped.
- `violating-pod.yaml` (host network, privileged) trips 6 rules in the same evaluator.

## Trade-offs
- The evaluator in `verify.py` re-implements only part of the `restricted` profile (it ignores volumes, host ports and others); the real admission controller is stricter.
- Not run end to end: the pods were never applied to a cluster, so no real admission response was captured.
- Pinning `enforce-version: v1.30` stops behaviour changing on upgrade but needs a manual bump.

## When not to use it
- For a namespace that truly needs privileged workloads (CNI, node agents), use a policy engine with exceptions rather than loosening a shared level.
