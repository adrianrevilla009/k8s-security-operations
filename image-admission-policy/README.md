# image-admission-policy

A ValidatingAdmissionPolicy and binding that only admit pods with images from approved registries and a pinned tag, plus a Python mirror of the rules.

## Goal
Show how to enforce an image policy with the built-in CEL admission policy, without installing a webhook.

## Run it
```
pip install pyyaml
python3 image-admission-policy/verify.py
```
Expected: `ok: policy wired; 5 sample images classified as expected`.

## What it proves
- `policy.yaml` requires every container image to start with `registry.example.com/orders/` or `registry.k8s.io/`.
- It also requires a digest (`@sha256:`) or a tag that is not `latest`; an image with no tag is rejected.
- The binding uses `Deny` and `Audit`, applies only to namespaces labelled `image-policy: enforced`, and the policy sets `failurePolicy: Fail`.

## Trade-offs
- The CEL expressions were never evaluated by an API server; `verify.py` re-implements them in Python and tests five sample images, so a CEL syntax error would not be caught.
- Only `spec.containers` is checked, not init or ephemeral containers.
- Requires Kubernetes with ValidatingAdmissionPolicy GA (1.30 or later).

## When not to use it
- For signature verification or vulnerability gates, use an engine that checks signatures or scan results.
