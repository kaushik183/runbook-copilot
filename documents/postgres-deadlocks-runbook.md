# PostgreSQL Deadlocks Runbook

## What it means
Two transactions wait for locks held by each other. PostgreSQL detects this after `deadlock_timeout` (1 second) and cancels one of them with `ERROR: deadlock detected`.

## Checks
1. Count deadlock errors per service in the logs. A few per day is normal under high concurrency; dozens per minute is an incident.
2. Read the PostgreSQL log entry: it lists both queries and the locked rows or tables.
3. Check recent releases for new code paths that update the same rows in a different order (for example inventory reservations updating SKUs in cart order).

## Common causes in our systems
- inventory-service reserving several SKUs without sorting them first.
- Long transactions that call external APIs while holding row locks.
- A migration adding a foreign key, which locks both tables.

## Mitigation
1. Roll back the release that introduced the new locking pattern.
2. Application fix: always lock rows in a consistent order (for example by SKU ID) and keep transactions short.
3. Retry the cancelled transaction in the application with a small random delay; deadlocks are safe to retry.

## Escalation
Database team if deadlocks involve schema changes or system catalogs.
