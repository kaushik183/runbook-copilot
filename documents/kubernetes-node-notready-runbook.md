# Kubernetes Node NotReady Runbook

## What it means
The kubelet on a node stopped reporting to the control plane. After 5 minutes, pods on the node are evicted and rescheduled.

## Checks
1. `kubectl get nodes` and `kubectl describe node <node>`; look at Conditions (MemoryPressure, DiskPressure, PIDPressure) and recent events.
2. Check the EC2 instance status in the AWS console. A failed status check means a hardware or hypervisor problem.
3. If it is a spot instance, check for a spot interruption notice (see the spot interruption runbook).
4. Check disk pressure; a full root volume stops the kubelet (see the node disk pressure runbook).

## Mitigation
1. Cordon the node so nothing new is scheduled: `kubectl cordon <node>`.
2. Drain it: `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`.
3. Terminate the instance; the node group will replace it.

## When many nodes go NotReady together
Suspect a shared cause: a bad AMI rollout, a CNI (aws-node) problem, or an availability-zone outage. Stop any node group upgrade in progress and page the platform team.
