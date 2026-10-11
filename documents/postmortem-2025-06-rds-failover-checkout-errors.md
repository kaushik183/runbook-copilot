# Postmortem: Checkout Errors During RDS Failover (June 2025)

**Severity:** SEV-2 · **Duration:** 4 minutes of errors, 25 minutes of degraded service · **Owner:** Database team

## Summary
AWS replaced failing hardware under the Orders database primary, triggering a Multi-AZ failover. Writes were unavailable for about 90 seconds, which was expected. However, one service kept failing for 25 minutes.

## Timeline (UTC)
- 03:12 RDS failover starts.
- 03:14 Failover complete; most services recover.
- 03:14 order-fulfillment-worker keeps failing with connection errors.
- 03:30 Investigation shows the worker cached the database IP address at startup.
- 03:37 Worker restarted; recovery.

## Root cause
order-fulfillment-worker used an old database driver setting that resolved DNS once and kept the IP forever. After failover the IP pointed to the old (now standby) instance.

## What went well
PgBouncer-based services reconnected automatically. Payment confirmations were retried safely with idempotency keys.

## Action items
- Move order-fulfillment-worker behind PgBouncer like other services (done).
- Add "survives an RDS failover" to the quarterly staging failover test (done).
- RDS failover runbook updated to check for services caching IPs (done).
