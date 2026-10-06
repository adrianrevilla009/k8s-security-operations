#!/usr/bin/env python3
"""Check the policy/binding wiring and mirror the two CEL rules in Python against sample images."""
import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))
docs = {d["kind"]: d for d in yaml.safe_load_all(open("policy.yaml"))}
pol, bind = docs["ValidatingAdmissionPolicy"], docs["ValidatingAdmissionPolicyBinding"]
assert bind["spec"]["policyName"] == pol["metadata"]["name"]
assert "Deny" in bind["spec"]["validationActions"] and pol["spec"]["failurePolicy"] == "Fail"
exprs = [v["expression"] for v in pol["spec"]["validations"]]
assert any("startsWith('registry.example.com/orders/')" in e for e in exprs)
assert any("':latest'" in e or "endsWith(':latest')" in e for e in exprs)


def allowed(img):
    """Python mirror of the CEL expressions in policy.yaml."""
    from_ok = img.startswith("registry.example.com/orders/") or img.startswith("registry.k8s.io/")
    pinned = "@sha256:" in img or (":" in img and not img.endswith(":latest"))
    return from_ok and pinned


cases = {
    "registry.example.com/orders/api:1.4.2": True,
    "registry.k8s.io/pause:3.9": True,
    "registry.example.com/orders/api:latest": False,
    "docker.io/library/nginx:1.27": False,
    "registry.example.com/orders/api": False,
}
for img, want in cases.items():
    assert allowed(img) == want, img
print("ok: policy wired; %d sample images classified as expected" % len(cases))
