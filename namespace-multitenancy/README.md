# namespace-multitenancy

Two tenant namespaces (`tenant-a`, `tenant-b`), each with a NetworkPolicy, ResourceQuota, baseline Pod Security level and a namespace-scoped admin binding.

## Goal
Show the minimum building blocks of soft multi-tenancy on one cluster, and a script that makes sure every tenant keeps all of them.

## Run it
```
pip install pyyaml
python3 namespace-multitenancy/verify.py
```
Expected: `ok: 2 tenants isolated (netpol + quota + scoped admin)`.

## What it proves
- In `tenants.yaml` each NetworkPolicy selects all pods and allows ingress only from pods in its own namespace; egress goes to the same namespace and to `kube-system` on UDP 53 (DNS).
- Each tenant has a quota of 10 pods, 2 CPU and 4Gi of memory requests.
- Each RoleBinding gives the built-in `admin` ClusterRole to one group (`tenant-a-admins`, `tenant-b-admins`) in its own namespace only; no ClusterRoleBinding exists.

## Trade-offs
- Namespaces share a kernel and control plane; this is isolation by policy, not a hard boundary.
- NetworkPolicy needs a CNI that enforces it; kind's default CNI does not.
- Not run end to end: no traffic was tested between the namespaces.

## When not to use it
- For mutually untrusted tenants, use separate clusters or virtual clusters.
