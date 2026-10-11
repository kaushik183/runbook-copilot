# Postmortem: Black Friday Session Evictions (November 2025)

**Severity:** SEV-2 · **Duration:** 2 hours 10 minutes (intermittent) · **Owner:** Platform team

## Summary
During the Black Friday peak, the Redis session cache reached its memory limit and started evicting sessions and carts. Customers were logged out and lost cart contents.

## Impact
About 6% of active sessions were evicted. Conversion rate dropped from 3.1% to 2.6% during the affected window.

## Timeline (UTC)
- 08:00 Peak traffic starts (2.8x normal).
- 09:20 Redis memory at 95%; `evicted_keys` climbing. Alert fires.
- 09:45 Cause found: a new rate-limiting feature wrote per-request keys **without a TTL**.
- 10:05 Rate-limit feature disabled with its flag; memory stops growing.
- 10:30 Script expires the orphaned keys in batches.
- 11:30 Memory back to 60%.

## Root cause
Keys without TTL cannot be evicted under `volatile-lru`, so Redis evicted sessions instead. The capacity plan did not include the new feature's keys.

## Action items
- Lint rule: every Redis `SET` in application code must include a TTL (done).
- Alert on memory used by keys without TTL (done).
- Include new features in pre-freeze capacity planning (process updated).
