#!/usr/bin/env python3
"""Lint RBAC manifests: no wildcards, no secrets, no escalation verbs, bindings resolve."""
import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))

docs = list(yaml.safe_load_all(open("rbac.yaml")))
kinds = {}
for d in docs:
    kinds.setdefault(d["kind"], {})[d["metadata"]["name"]] = d
errs = []
for name, role in kinds.get("Role", {}).items():
    for r in role["rules"]:
        flat = r["verbs"] + r["resources"] + r["apiGroups"]
        if "*" in flat:
            errs.append(name + ": wildcard")
        if "secrets" in r["resources"]:
            errs.append(name + ": reads secrets")
        if set(r["verbs"]) & {"escalate", "bind", "impersonate"}:
            errs.append(name + ": escalation verb")
for name, rb in kinds.get("RoleBinding", {}).items():
    if rb["roleRef"]["name"] not in kinds["Role"]:
        errs.append(name + ": dangling roleRef")
    if rb["roleRef"]["kind"] == "ClusterRole" and rb["roleRef"]["name"] == "cluster-admin":
        errs.append(name + ": cluster-admin")
    for s in rb["subjects"]:
        if s["kind"] == "ServiceAccount" and s["name"] not in kinds["ServiceAccount"]:
            errs.append(name + ": unknown subject " + s["name"])
assert "ClusterRoleBinding" not in kinds, "no cluster-wide bindings"
assert not errs, errs
print("ok: %d roles, %d bindings, least privilege" % (len(kinds["Role"]), len(kinds["RoleBinding"])))
