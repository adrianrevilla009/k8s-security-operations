# k8s-security-operations

Ten small Kubernetes hardening and operations examples (admission, RBAC, quotas, tenancy, runtime detection, upgrades, backups, autoscaling, snapshots), each with a check you can run without a cluster. They use a tiny Orders domain.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`pod-security-admission`](./pod-security-admission) | Pod Security Admission labels for three namespaces, plus a compliant and a violating pod | `python3 pod-security-admission/verify.py` |
| [`rbac-least-privilege`](./rbac-least-privilege) | A read-only Role for one ServiceAccount, with a linter for wildcards, secrets and escalation verbs | `python3 rbac-least-privilege/verify.py` |
| [`resource-quotas-limitranges`](./resource-quotas-limitranges) | A ResourceQuota and LimitRange whose numbers are checked for consistency | `python3 resource-quotas-limitranges/verify.py` |
| [`namespace-multitenancy`](./namespace-multitenancy) | Two tenant namespaces with NetworkPolicy, quota and a scoped admin binding | `python3 namespace-multitenancy/verify.py` |
| [`falco-runtime-security`](./falco-runtime-security) | Two Falco rules for the orders namespace (shell spawned, sensitive file read) | `python3 falco-runtime-security/verify.py` |
| [`image-admission-policy`](./image-admission-policy) | A ValidatingAdmissionPolicy (CEL) that restricts image registries and tags | `python3 image-admission-policy/verify.py` |
| [`cluster-upgrade-runbook`](./cluster-upgrade-runbook) | A kubeadm 1.29 to 1.30 runbook and a pinned kind config for a drill cluster | `python3 cluster-upgrade-runbook/verify.py` |
| [`etcd-backup-restore`](./etcd-backup-restore) | A backup, delete, restore, verify drill script for a kind control plane | `python3 etcd-backup-restore/verify.py` (static); `./etcd-backup-restore/drill.sh` (live) |
| [`karpenter-cluster-autoscaler`](./karpenter-cluster-autoscaler) | A Karpenter NodePool and EC2NodeClass with a cost ceiling and consolidation | `python3 karpenter-cluster-autoscaler/verify.py` |
| [`storage-csi-snapshots`](./storage-csi-snapshots) | A CSI VolumeSnapshot taken from a PVC and restored into a new PVC | `python3 storage-csi-snapshots/verify.py` |

## Prerequisites

- Python 3 with PyYAML (`pip install pyyaml`) for every `verify.py`.
- Bash, for the syntax check of `etcd-backup-restore/drill.sh`.
- Only for a live run of the etcd drill: Docker, kind and kubectl.
- Not needed for the checks: Falco, Karpenter, an AWS account or a CSI driver.

## How to read it

Start with `pod-security-admission`, then `rbac-least-privilege`; they show the pattern used everywhere: a manifest plus a script that checks its rules. The checks are offline and read the YAML; none of the manifests were applied to a live cluster, and the etcd drill was only syntax-checked.
