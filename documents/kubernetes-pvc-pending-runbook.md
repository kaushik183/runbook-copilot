# Kubernetes PVC Pending Runbook

## Background
Only a few workloads use persistent volumes (search-indexer cache, Prometheus, some batch jobs). Storage class `gp3` uses EBS volumes, which exist in a single availability zone.

## Symptom: PVC stuck in Pending
1. `kubectl describe pvc <name> -n <ns>` and read the events.
2. **"waiting for first consumer"**: normal for `WaitForFirstConsumer` storage classes; the volume is created when a pod is scheduled.
3. **Provisioning errors**: check the EBS CSI driver pods and the IAM permissions of its service account.
4. **Quota or limits**: check the AWS EBS volume quota for the region.

## Symptom: pod Pending with "volume node affinity conflict"
The EBS volume is in a different availability zone from the nodes that have capacity. Either add capacity in that zone or restore the data into a new volume in another zone from the latest snapshot.

## Rules
Do not delete a PVC to "unstick" it unless you are sure the data is not needed. Deleting the PVC deletes the volume with reclaim policy `Delete`.
