# Alert Playbook: Disk Usage

**Alerts:** `NodeDiskUsageHigh` (above 80%), `PVCUsageHigh` (above 85%), `RDSFreeStorageLow` (below 15%).

## What to do by type

### Node disks
Usually logs or scratch files written to local disk, or many old images. See the node disk pressure runbook. Replace the node if usage keeps growing.

### Persistent volumes (Prometheus, search-indexer cache, batch jobs)
1. Check growth rate: when will it be full at the current rate?
2. Prometheus: reduce retention or drop high-cardinality metrics (a new label with user IDs is a common cause).
3. EBS volumes can be expanded online if the storage class allows it (`allowVolumeExpansion: true`). Edit the PVC size; the filesystem grows automatically.

### Databases
See the RDS storage full runbook. Database storage is urgent: a full database stops accepting writes.

## Prediction
Prefer predictive alerts: "full within 4 hours" based on `predict_linear` is more useful than a fixed percentage.
