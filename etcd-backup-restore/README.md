# etcd-backup-restore

`drill.sh`, a script that backs up etcd on a kind control-plane node, deletes an object, restores, and checks the object returns.

## Goal
Practise the etcd snapshot and restore cycle on a throwaway cluster before needing it for real.

## Run it
```
python3 etcd-backup-restore/verify.py
kind create cluster --name etcd-drill
./etcd-backup-restore/drill.sh
```
Expected from the first command: `ok: drill.sh parses; 5 steps in order`. The last command should print `before-backup` if the restore worked.

## What it proves
- `drill.sh` creates a ConfigMap `drill-marker`, runs `etcdctl snapshot save` inside the etcd static pod with the TLS certs from `/etc/kubernetes/pki/etcd`, then deletes the ConfigMap.
- It restores with `etcdutl snapshot restore` into `/var/lib/etcd-restored`, edits `/etc/kubernetes/manifests/etcd.yaml` to use that directory, waits 30 s and reads the ConfigMap again.
- `verify.py` checks bash syntax, `set -euo pipefail`, TLS flags and the order of those steps.

## Trade-offs
- Not run end to end: only the static check ran here; the live drill needs a kind cluster and was not executed.
- The snapshot stays on the same node; a real backup must be copied off the host.
- The fixed `sleep 30` may be too short on a slow machine, and the `sed` edit assumes the manifest's etcd data path ends the line.

## When not to use it
- On managed control planes (EKS, GKE, AKS), where etcd is not reachable; use the provider's backup tools.
