# Node Disk Pressure Runbook

## What it means
The node's root or container volume is nearly full. At 85% usage the kubelet starts garbage-collecting images; at 90% it reports `DiskPressure` and begins evicting pods.

## Checks
1. `kubectl describe node <node>`: look for the `DiskPressure` condition and eviction events.
2. Find what is using space. Common causes:
   - Applications writing large log files inside the container instead of stdout.
   - `emptyDir` volumes used as scratch space by batch jobs.
   - Many unused container images on long-lived nodes.
3. Use the node's disk usage panel in Grafana to see whether usage grew slowly or suddenly.

## Mitigation
1. Cordon and drain the node, then replace it. New nodes start with clean disks.
2. Fix the workload that writes to local disk. Logs must go to stdout; scratch data needs a size limit on the `emptyDir`.

## Prevention
Node root volumes are 100 GiB gp3. Raising this is a platform-team decision; it hides the problem rather than fixing it.
