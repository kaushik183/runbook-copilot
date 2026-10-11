# Redis Failover Runbook

## Background
ElastiCache automatically promotes a replica if the primary fails. The primary endpoint DNS name moves to the new primary within about 30-60 seconds.

## What on-call sees
A short burst of connection errors and timeouts from every service using Redis (cart, auth, rate limiting), then recovery.

## Checks after a failover
1. Read the ElastiCache event log to confirm the failover and its cause.
2. Confirm clients reconnected: Redis error rate back to normal in each service.
3. Check for services that connected to a **node** endpoint instead of the primary endpoint. They will keep writing to a replica and fail with `READONLY You can't write against a read only replica`. Fix their configuration and restart them.
4. Check for lost writes: sessions created in the last seconds before failover may be missing. This logs out a small number of users and is acceptable.

## Testing
The platform team runs a failover test every quarter in staging. Services must survive it without manual restarts.

## Escalation
Platform team if failover does not complete within 5 minutes or repeats more than twice in a day.
