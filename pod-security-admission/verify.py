#!/usr/bin/env python3
"""Offline PSA check: namespace labels plus a mini 'restricted' profile evaluator."""
import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    return list(yaml.safe_load_all(open(p)))


def restricted_violations(pod):
    spec, out = pod["spec"], []
    psc = spec.get("securityContext", {})
    if spec.get("hostNetwork"):
        out.append("hostNetwork")
    for c in spec["containers"]:
        sc = c.get("securityContext", {})
        n = c["name"]
        if sc.get("privileged"):
            out.append(n + ": privileged")
        if sc.get("allowPrivilegeEscalation") is not False:
            out.append(n + ": allowPrivilegeEscalation not false")
        if "ALL" not in sc.get("capabilities", {}).get("drop", []):
            out.append(n + ": capabilities.drop lacks ALL")
        if not (sc.get("runAsNonRoot") or psc.get("runAsNonRoot")):
            out.append(n + ": runAsNonRoot missing")
        if not (sc.get("seccompProfile") or psc.get("seccompProfile")):
            out.append(n + ": seccompProfile missing")
    return out


pre = "pod-security.kubernetes.io/enforce"
levels = {d["metadata"]["name"]: d["metadata"]["labels"].get(pre) for d in load("namespaces.yaml")}
assert levels == {"orders-restricted": "restricted", "orders-baseline": "baseline", "orders-system": "privileged"}, levels
assert not restricted_violations(load("compliant-pod.yaml")[0]), "compliant pod must pass"
bad = restricted_violations(load("violating-pod.yaml")[0])
assert len(bad) >= 4, bad
print("ok: levels", sorted(levels.values()), "- violating pod has", len(bad), "violations")
