# resource-quotas-limitranges

A ResourceQuota and a LimitRange for the `orders` namespace, with a script that checks the numbers fit together.

## Goal
Show how a LimitRange gives every container defaults and bounds, and how a quota caps the namespace total, without the defaults making the quota impossible to use.

## Run it
```
pip install pyyaml
python3 resource-quotas-limitranges/verify.py
```
Expected: `ok: limit range ordered; 20 default-sized pods fit the quota`.

## What it proves
- In `quota.yaml` the container limits are ordered: min 50m/64Mi, default request 100m/128Mi, default limit 500m/512Mi, max 2 CPU/2Gi.
- The quota allows 20 pods, 4 CPU and 8Gi of requests, and 8 CPU and 16Gi of limits.
- 20 pods at the default request use 2 CPU, within the 4 CPU quota; 20 pods at the default memory limit use 10Gi, within 16Gi.

## Trade-offs
- The check models one container per pod and only the Container limit type.
- Not run end to end: no pod was rejected by a live API server.
- Fixed defaults suit small services; a mixed workload needs more than one LimitRange profile or per-team namespaces.

## When not to use it
- For clusters where teams set their own requests from measured usage, a vertical autoscaler may fit better than fixed defaults.
