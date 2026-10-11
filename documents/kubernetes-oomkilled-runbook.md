# Kubernetes OOMKilled Runbook

## What it means
The container used more memory than its limit and the kernel killed it (exit code 137, reason `OOMKilled`).

## Checks
1. Confirm with `kubectl describe pod` (Last State: OOMKilled) and the container memory graph in Grafana.
2. Decide the pattern:
   - **Memory climbs steadily until the kill**: likely a memory leak. Compare with the previous release.
   - **Memory jumps suddenly**: a large request or batch (for example an export or a huge cart). Check logs just before the kill.
   - **Killed at startup**: the limit is too low for the app's baseline (common for services that load a model or a large cache).
3. Check if the node itself is under memory pressure (`kubectl describe node`), which can cause evictions as well as OOM kills.

## Mitigation
- Roll back if the problem started with a release.
- Raising the memory limit is allowed up to 2x the current value when the request is also raised. Larger changes need platform-team review because they affect node capacity.
- For JVM or Node.js services, make sure the runtime heap setting is below the container limit (about 75% of it).

## Do not
Do not remove memory limits. A pod without limits can take down the whole node.
