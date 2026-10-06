#!/usr/bin/env python3
"""Static checks on drill.sh: valid bash syntax, strict mode, and backup -> disaster -> restore -> verify order."""
import os
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(["bash", "-n", "drill.sh"], check=True)
s = open("drill.sh").read()
assert "set -euo pipefail" in s
steps = ["snapshot save", "kubectl delete configmap", "snapshot restore", "/etc/kubernetes/manifests/etcd.yaml", "kubectl get configmap drill-marker"]
pos = [s.index(x) for x in steps]
assert pos == sorted(pos), "drill steps out of order"
assert "ca.crt" in s and "server.key" in s, "etcdctl must use TLS client certs"
print("ok: drill.sh parses; %d steps in order" % len(steps))
