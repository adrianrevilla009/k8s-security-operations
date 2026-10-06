#!/usr/bin/env python3
"""Check LimitRange consistency (min <= request <= default <= max) and quota headroom."""
import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))

UNITS = {"m": 1, "Mi": 1, "Gi": 1024}


def q(v, cpu):
    v = str(v)
    if cpu:
        return int(v[:-1]) if v.endswith("m") else int(float(v) * 1000)
    return int(v[:-2]) * UNITS[v[-2:]]


docs = {d["kind"]: d for d in yaml.safe_load_all(open("quota.yaml"))}
lim = docs["LimitRange"]["spec"]["limits"][0]
for res, cpu in (("cpu", True), ("memory", False)):
    mn, req, dflt, mx = (q(lim[k][res], cpu) for k in ("min", "defaultRequest", "default", "max"))
    assert mn <= req <= dflt <= mx, res + ": min <= defaultRequest <= default <= max violated"
hard = docs["ResourceQuota"]["spec"]["hard"]
pods = int(hard["pods"])
assert pods * q(lim["defaultRequest"]["cpu"], True) <= q(hard["requests.cpu"], True), "defaults exhaust cpu quota"
assert pods * q(lim["default"]["memory"], False) <= q(hard["limits.memory"], False), "defaults exhaust memory quota"
assert q(hard["requests.cpu"], True) <= q(hard["limits.cpu"], True)
print("ok: limit range ordered; %d default-sized pods fit the quota" % pods)
