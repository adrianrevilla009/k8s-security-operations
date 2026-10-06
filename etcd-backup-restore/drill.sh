#!/usr/bin/env bash
# etcd backup and restore drill on a kind control-plane node (docker exec, no host etcdctl needed).
# Usage: ./drill.sh   (requires a kind cluster named "etcd-drill": kind create cluster --name etcd-drill)
set -euo pipefail

NODE=etcd-drill-control-plane
CERTS=/etc/kubernetes/pki/etcd
SNAP=/var/lib/etcd-snapshot.db
ETCDCTL="etcdctl --endpoints=https://127.0.0.1:2379 --cacert=$CERTS/ca.crt --cert=$CERTS/server.crt --key=$CERTS/server.key"

kubectl create configmap drill-marker --from-literal=state=before-backup
# 1. Backup (etcdctl ships in the etcd static pod image, so run it there)
kubectl -n kube-system exec etcd-$NODE -- sh -c "$ETCDCTL snapshot save /var/lib/etcd/snap.db"
docker exec $NODE cp /var/lib/etcd/snap.db $SNAP
# 2. Disaster
kubectl delete configmap drill-marker
# 3. Restore into a new data dir, then point the static pod at it
docker exec $NODE sh -c "etcdutl snapshot restore $SNAP --data-dir /var/lib/etcd-restored"
docker exec $NODE sed -i 's#path: /var/lib/etcd$#path: /var/lib/etcd-restored#' /etc/kubernetes/manifests/etcd.yaml
sleep 30
# 4. Verify the deleted object is back
kubectl get configmap drill-marker -o jsonpath='{.data.state}{"\n"}'
