#!/usr/bin/env python3
"""Check the snapshot chain: class -> snapshot -> source PVC, and restore PVC -> snapshot, with size and class matching."""
import os
import yaml

os.chdir(os.path.dirname(os.path.abspath(__file__)))
docs = list(yaml.safe_load_all(open("snapshots.yaml")))
by = {(d["kind"], d["metadata"]["name"]): d for d in docs}
snap = by[("VolumeSnapshot", "orders-data-snap")]
assert ("VolumeSnapshotClass", snap["spec"]["volumeSnapshotClassName"]) in by, "snapshot class missing"
src = by[("PersistentVolumeClaim", snap["spec"]["source"]["persistentVolumeClaimName"])]
restored = by[("PersistentVolumeClaim", "orders-data-restored")]
ds = restored["spec"]["dataSource"]
assert ds["kind"] == "VolumeSnapshot" and ds["name"] == snap["metadata"]["name"]
assert restored["spec"]["storageClassName"] == src["spec"]["storageClassName"], "restore must use the same storage class"
size = lambda p: int(p["spec"]["resources"]["requests"]["storage"][:-2])
assert size(restored) >= size(src), "restored volume must be at least as large as the source"
print("ok: snapshot chain consistent (class -> snapshot -> source, restore -> snapshot)")
