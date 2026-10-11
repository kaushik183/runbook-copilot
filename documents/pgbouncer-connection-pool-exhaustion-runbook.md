# PgBouncer Connection Pool Exhaustion Runbook

## Background
Applications connect to PostgreSQL through PgBouncer (transaction pooling). PgBouncer keeps up to 200 server connections to the Orders database and queues client requests when all are busy.

## Symptoms
- Application errors such as `timeout waiting for connection` or `remaining connection slots are reserved`.
- Rising latency across checkout-api and payments-service at the same time.
- PgBouncer metrics: `cl_waiting` above 0 for more than a minute, `sv_active` at the pool maximum.

## Checks
1. Find what holds connections: long-running queries or transactions left open (`idle in transaction`) in `pg_stat_activity`.
2. Check for a deployment that increased replicas. Each pod opens its own client pool; 3x replicas can mean 3x connection demand.
3. Check for slow queries that keep each connection busy longer (see the slow queries runbook).
4. Check for a retry storm: clients retrying failed requests multiply load.

## Mitigation
1. Terminate sessions stuck `idle in transaction` for more than 10 minutes (database team approval).
2. Roll back the release that introduced the slow query or connection leak.
3. Reduce replicas of non-critical writers (batch jobs, reporting) to free connections for checkout.

## Do not
Do not raise `max_connections` on PostgreSQL during an incident; more connections increase memory use and usually make contention worse.
