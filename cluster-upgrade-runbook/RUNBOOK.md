# Upgrade runbook: 1.29 -> 1.30 (one minor version at a time)

## 1. Preflight
- Read the release notes and the deprecated API list for the target version.
- Scan for removed APIs: `kubectl get --raw /metrics | grep apiserver_requested_deprecated_apis`.
- Confirm a fresh etcd snapshot exists (see `etcd-backup-restore`).
- Check PodDisruptionBudgets: `kubectl get pdb -A` (a PDB with 0 allowed disruptions blocks drains).
- Confirm version skew: kubelet may be at most 3 minor versions behind the API server (1.28+), never ahead.

## 2. Control plane
- Upgrade one control-plane node at a time: `kubeadm upgrade plan`, then `kubeadm upgrade apply v1.30.4` on the first node and `kubeadm upgrade node` on the others.
- Upgrade kubelet and kubectl packages, then `systemctl restart kubelet`.
- Gate: `kubectl get nodes` shows all control-plane nodes Ready and API errors are flat.

## 3. Workers (rolling)
- Per node: `kubectl cordon <node>`, `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`, upgrade kubeadm, kubelet, `kubeadm upgrade node`, restart kubelet, `kubectl uncordon <node>`.
- Gate between nodes: workloads healthy, no pending pods.

## 4. Post-upgrade
- Verify `kubectl version` and node versions, run smoke tests, check CNI/CSI/ingress pods.
- Keep the pre-upgrade snapshot until the next maintenance window.

## 5. Rollback
- Kubernetes does not support control plane downgrade: restore etcd from the snapshot onto the old binaries (see `etcd-backup-restore`) or fail over to a standby cluster.
