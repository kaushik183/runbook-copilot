# Orders Database (PostgreSQL) Runbook

## Overview
The Orders database is a PostgreSQL 15 instance on Amazon RDS (Multi-AZ) with one read replica. Writers: checkout-api, payments-service, order-fulfillment-worker. Applications connect through PgBouncer in transaction pooling mode, never directly.

## Key health signals
- Active connections on PgBouncer versus the pool size (200 server connections).
- Replica lag (alert above 30 seconds).
- CPU above 80% for 15 minutes, or free storage below 15%.
- Long-running transactions older than 5 minutes.

## First response
1. Identify whether the problem is connections, CPU, storage, or locks using the Orders DB Grafana dashboard.
2. Find long-running queries: `SELECT pid, now() - query_start AS age, state, query FROM pg_stat_activity WHERE state <> 'idle' ORDER BY age DESC LIMIT 20;`
3. Do not terminate sessions owned by migrations without the database team.
4. If CPU is high after a deployment, check for a new query missing an index (see the slow queries runbook).

## Related runbooks
PgBouncer connection pool exhaustion, PostgreSQL replication lag, deadlocks, vacuum and bloat, RDS failover, RDS storage full.

## Escalation
The database team owns schema changes, parameter-group changes and manual failovers. Page them for any write outage.
