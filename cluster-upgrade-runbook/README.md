# cluster-upgrade-runbook

A written kubeadm upgrade runbook from 1.29 to 1.30 and a kind config for a three-node practice cluster.

## Goal
Give an ordered, gated procedure for a one-minor-version upgrade, and a pinned cluster to rehearse on.

## Run it
```
pip install pyyaml
python3 cluster-upgrade-runbook/verify.py
```
Expected: `ok: runbook phases ordered, drill cluster pinned to kindest/node:v1.29.8`.

## What it proves
- `RUNBOOK.md` has five phases in order: Preflight, Control plane, Workers, Post-upgrade, Rollback.
- Worker steps run cordon, then drain, then uncordon, with a health gate between nodes; preflight includes a PDB check and a fresh etcd snapshot.
- `kind-config.yaml` defines one control plane and two workers, all on `kindest/node:v1.29.8`.

## Trade-offs
- `verify.py` only checks the document structure and the pin; the commands in the runbook were not run.
- kind nodes are not upgraded with kubeadm in place, so the drill cluster can practise drains but not the full package upgrade.
- The runbook assumes kubeadm; managed services upgrade differently.

## When not to use it
- On EKS, GKE or AKS, follow the provider's upgrade flow instead of kubeadm steps.
