# RDS Failover Runbook

## Background
The Orders and Users PostgreSQL databases run on RDS Multi-AZ. During a failover the standby becomes primary and the DNS endpoint moves to it. Writes are unavailable for 60-120 seconds.

## What on-call sees
A burst of connection errors from every writer, then recovery. PgBouncer reconnects automatically, but long-running transactions are lost and clients receive errors.

## Checks after a failover
1. Read the RDS event log for the reason (hardware failure, maintenance, manual reboot with failover).
2. Confirm applications reconnected: error rate back to baseline, PgBouncer server connections recovered.
3. Check that no service cached the old IP address. Services must use the endpoint hostname and respect DNS TTL (5 seconds).
4. Check the read replica is replicating from the new primary.

## Manual failover
Only the database team may trigger a manual failover ("Reboot with failover"). It is used when the primary is degraded but not failing.

## Customer impact
Orders submitted during the window may fail; checkout-api retries payment confirmation safely using idempotency keys. Share the failover window with customer support.
