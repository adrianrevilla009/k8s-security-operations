#!/usr/bin/env python3
"""Every tenant namespace must carry isolation, quota and a scoped admin binding."""
import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))
docs = list(yaml.safe_load_all(open("tenants.yaml")))
tenants = [d["metadata"]["name"] for d in docs if d["kind"] == "Namespace"]
assert len(tenants) >= 2


def in_ns(kind, ns):
    return [d for d in docs if d["kind"] == kind and d["metadata"].get("namespace") == ns]


for ns in tenants:
    pol = in_ns("NetworkPolicy", ns)
    assert pol and pol[0]["spec"]["podSelector"] == {}, ns + ": no namespace-wide NetworkPolicy"
    for rule in pol[0]["spec"]["ingress"]:
        for src in rule["from"]:
            assert "namespaceSelector" not in src, ns + ": ingress from other namespaces"
    assert in_ns("ResourceQuota", ns), ns + ": no quota"
    rbs = in_ns("RoleBinding", ns)
    assert rbs and all(s["name"].startswith(ns) for r in rbs for s in r["subjects"]), ns + ": binding not tenant scoped"
assert not [d for d in docs if d["kind"] == "ClusterRoleBinding"], "no cluster-wide bindings"
print("ok: %d tenants isolated (netpol + quota + scoped admin)" % len(tenants))
