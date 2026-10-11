# Redis Memory Eviction Runbook

## Background
The session cache uses `maxmemory` with the `volatile-lru` policy. When memory is full, Redis evicts keys that have a TTL, starting with the least recently used.

## Symptoms
- `evicted_keys` rising on the ElastiCache dashboard.
- Customers logged out or carts emptied.
- Memory usage above 90% of `maxmemory`.

## Checks
1. Find which key prefixes use the most memory. Use `redis-cli --bigkeys` against a **replica**, never the primary during peak traffic.
2. Check for keys written without a TTL. They can never be evicted and slowly fill memory. A recent release that forgot the TTL is a common cause.
3. Compare memory growth with traffic. Seasonal peaks (sales events) can legitimately need more memory.

## Mitigation
1. Fix or roll back the release that writes keys without TTL; then expire those keys in small batches with a script reviewed by the platform team.
2. Scale the node type up (online resize takes 10-30 minutes; do it before peak if possible).
3. Shorten TTLs for low-value keys such as rate-limit counters.

## Never
Never run `FLUSHALL` or `FLUSHDB`. Never switch the eviction policy to `allkeys-lru` without platform approval; it can evict keys that other services expect to persist.
