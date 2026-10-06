# karpenter-cluster-autoscaler

A Karpenter v1 NodePool and an AWS EC2NodeClass for an Orders cluster, with a script that checks they are consistent.

## Goal
Show how Karpenter decides what nodes to launch, how it limits cost, and how it removes nodes, in one small config.

## Run it
```
pip install pyyaml
python3 karpenter-cluster-autoscaler/verify.py
```
Expected: `ok: NodePool limits, consolidation and class reference are consistent`.

## What it proves
- `nodepool.yaml` allows spot and on-demand capacity, `c` and `m` instance categories and `amd64`.
- The pool caps the total at 100 CPU and 400Gi memory, consolidates with `WhenEmptyOrUnderutilized` after 1 minute, and replaces nodes after 720 h.
- The `nodeClassRef` points at the `orders-default` EC2NodeClass, which selects subnets and security groups by the tag `karpenter.sh/discovery: orders`.

## Trade-offs
- Not run end to end: applying it needs an EKS cluster with Karpenter installed; `verify.py` only reads the YAML.
- `al2023@latest` makes node images float; pin an AMI version for production.
- Aggressive consolidation can churn pods that lack a PodDisruptionBudget.

## When not to use it
- Outside AWS, or on a small fixed-size cluster where Cluster Autoscaler or no autoscaling is enough.
