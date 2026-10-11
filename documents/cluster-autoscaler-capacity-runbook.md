# Cluster Autoscaler and Capacity Runbook

## Background
Nodes are added by the cluster autoscaler when pods are Pending because of insufficient CPU or memory. We run three managed node groups: `general` (on-demand), `spot-general`, and `memory-optimized`.

## Symptom: pods Pending with "Insufficient cpu" or "Insufficient memory"
1. Check the cluster autoscaler logs in `kube-system` for scale-up decisions and errors.
2. **Max size reached**: the node group is at its maximum. Raising it needs platform-team approval and a check of AWS instance quotas.
3. **Insufficient capacity in the zone**: AWS has no instances of that type available. Spot groups are affected most; the on-demand group is the fallback.
4. **Pod cannot fit on any node type**: a pod requests more memory than the largest node offers.

## Mitigation
- Temporarily raise `maxSize` of the on-demand node group (platform team).
- Lower the priority of batch workloads so customer-facing pods are scheduled first; batch jobs use the `low-priority` PriorityClass.

## Scale-up time
A new node takes about 3-4 minutes to join and become ready. Autoscaling cannot absorb a sudden traffic spike instantly; pre-scale before planned events such as sales.
