# storage-csi-snapshots

CSI snapshot manifests: a class, a source PVC, a VolumeSnapshot and a second PVC restored from it.

## Goal
Show the object chain for snapshotting a volume and restoring it into a new claim.

## Run it
```
pip install pyyaml
python3 storage-csi-snapshots/verify.py
```
Expected: `ok: snapshot chain consistent (class -> snapshot -> source, restore -> snapshot)`.

## What it proves
- `snapshots.yaml` links `VolumeSnapshotClass` `csi-hostpath-snapclass` to `VolumeSnapshot` `orders-data-snap`, which reads PVC `orders-data` (1Gi).
- `orders-data-restored` uses that snapshot as its `dataSource`, with the same storage class and the same 1Gi size.
- `verify.py` fails if a link is missing, the storage classes differ, or the restored size is smaller.

## Trade-offs
- Not run end to end: it needs the external-snapshotter CRDs (v8.0.1) and the csi-driver-host-path driver (v1.14.0) on a cluster such as kind; neither was installed here.
- The class uses `deletionPolicy: Delete`, so deleting a snapshot also removes the stored data.
- A host-path snapshot lives on the same node as the volume, so it is not a backup.

## When not to use it
- As the only protection for data; copy backups to separate storage.
- With a storage driver that does not support snapshots.
