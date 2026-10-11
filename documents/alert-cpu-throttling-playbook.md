# Alert Playbook: CPU Throttling

**Alert:** `ContainerCPUThrottlingHigh` · **Fires when:** more than 25% of CPU periods are throttled for a container for 15 minutes.

## What it means
The container wants more CPU than its limit allows, so the kernel pauses it in every scheduling period. This adds latency even if average CPU usage looks below the limit, because work arrives in bursts.

## Checks
1. Compare the CPU limit with actual usage peaks (not averages) in Grafana.
2. Check whether throttling started with a release (more work per request) or with traffic growth.
3. For multi-threaded runtimes, check thread pool sizes; a runtime that thinks it has 16 cores but is limited to 1 core throttles heavily.

## Actions
- Short term: scale out replicas so each pod receives less work.
- Medium term: raise the CPU limit (up to 2x with matching request increase is allowed; larger changes need platform review) or optimize the code.
- Set runtime CPU awareness: for example `GOMAXPROCS` matching the limit, or the JVM's container support enabled.

## Related
Payments service high CPU runbook, high latency playbook.
