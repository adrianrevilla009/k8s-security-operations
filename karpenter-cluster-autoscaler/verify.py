#!/usr/bin/env python3
"""Check the Karpenter NodePool has a ceiling, consolidation, expiry and a resolvable EC2NodeClass."""
import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))
docs = {d["kind"]: d for d in yaml.safe_load_all(open("nodepool.yaml"))}
pool, cls = docs["NodePool"], docs["EC2NodeClass"]
assert pool["spec"]["limits"]["cpu"], "NodePool needs a cpu limit (cost ceiling)"
assert pool["spec"]["disruption"]["consolidationPolicy"] == "WhenEmptyOrUnderutilized"
assert pool["spec"]["template"]["spec"]["expireAfter"].endswith("h")
ref = pool["spec"]["template"]["spec"]["nodeClassRef"]
assert ref["kind"] == "EC2NodeClass" and ref["name"] == cls["metadata"]["name"], "dangling nodeClassRef"
caps = [r for r in pool["spec"]["template"]["spec"]["requirements"] if r["key"] == "karpenter.sh/capacity-type"]
assert caps and "on-demand" in caps[0]["values"], "keep an on-demand fallback for spot interruptions"
assert cls["spec"]["subnetSelectorTerms"] and cls["spec"]["securityGroupSelectorTerms"]
print("ok: NodePool limits, consolidation and class reference are consistent")
