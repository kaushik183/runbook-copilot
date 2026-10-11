# Alert Playbook: High Latency (p99)

**Alert:** `HighLatencyP99` · **Fires when:** p99 latency above the service threshold for 10 minutes (checkout-api: 1.5 s, cart-service: 500 ms, search: 1.2 s).

## What it means
The slowest 1% of requests are too slow. This often comes before errors and timeouts.

## First checks
1. Is latency high for all endpoints or one? One endpoint usually means one slow query or one slow dependency.
2. Check dependencies in the service dashboard: database query time, Redis latency, external API latency.
3. Check CPU throttling (`container_cpu_cfs_throttled_periods_total`). Throttled pods are slow even when average CPU looks fine.
4. Check garbage collection or event-loop lag for JVM and Node.js services.
5. Check traffic: a spike can saturate connection pools.

## Typical actions
- Roll back a release that introduced the slowness.
- Scale out if throttling or traffic is the cause and dependencies can handle more load.
- Enable degraded modes (for example `search.degraded_mode`) to shed expensive work.

## Do not
Do not raise client or ingress timeouts to make the alert stop. That hides the problem and ties up more connections.
