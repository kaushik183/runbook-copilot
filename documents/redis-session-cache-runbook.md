# Redis Session Cache Runbook

## Overview
The session cache is an Amazon ElastiCache for Redis cluster (cluster mode disabled, one primary, two replicas). It stores user sessions, carts, and short-lived rate-limit counters. Eviction policy is `volatile-lru`, so only keys with a TTL can be evicted.

## Symptoms and checks
**Users logged out unexpectedly**
1. Check `evicted_keys` and memory usage. Sessions have TTLs and are the first to be evicted under memory pressure.
2. Check for a recent failover in the ElastiCache event log. Clients reconnect automatically but in-flight writes can be lost.

**Latency spikes**
1. Look for slow commands: `SLOWLOG GET 20`. `KEYS *` or large `HGETALL` calls block the single Redis thread.
2. Check client connection count; a connection leak in one service can exhaust `maxclients`.

## Safe actions
- Scale up the node type during a maintenance window, not during peak traffic.
- Remove a misbehaving client by scaling down the offending deployment, not by `CLIENT KILL` loops.

## Never
Never run `FLUSHALL` in production. It logs out every customer and empties every cart. Escalate to the platform team before changing the eviction policy.
