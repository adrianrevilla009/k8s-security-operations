#!/usr/bin/env python3
"""Check the runbook has its ordered phases and key commands, and the kind drill config is pinned."""
import os
import re
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))
text = open("RUNBOOK.md").read()
heads = re.findall(r"^## \d+\. (\w[\w-]*)", text, re.M)
assert heads == ["Preflight", "Control", "Workers", "Post-upgrade", "Rollback"], heads
for cmd in ("kubectl cordon", "kubectl drain", "kubectl uncordon", "kubeadm upgrade plan", "kubeadm upgrade apply", "kubectl get pdb"):
    assert cmd in text, "missing " + cmd
assert text.index("kubectl cordon") < text.index("kubectl drain") < text.index("kubectl uncordon")
cfg = yaml.safe_load(open("kind-config.yaml"))
images = {n["image"] for n in cfg["nodes"]}
assert len(images) == 1 and all(re.search(r":v\d+\.\d+\.\d+$", i) for i in images), images
print("ok: runbook phases ordered, drill cluster pinned to", images.pop())
