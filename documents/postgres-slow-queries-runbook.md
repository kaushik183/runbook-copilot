# PostgreSQL Slow Queries Runbook

## Symptoms
Database CPU above 80%, rising API latency, and queries appearing in the slow query log (threshold 500 ms).

## Find the culprit
1. Top queries by total time: `SELECT query, calls, total_exec_time, mean_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;`
2. Check when it started. A new query after a deployment usually means a missing index or an N+1 query pattern in the code.
3. Run `EXPLAIN (ANALYZE, BUFFERS)` on a copy of the query against the read replica, not the primary. Look for `Seq Scan` on large tables.

## Common causes
- A new filter or sort column without an index.
- Outdated planner statistics after a large data load. Run `ANALYZE <table>`.
- An ORM loading related rows one by one (N+1).
- A query using a function on an indexed column (`WHERE lower(email) = ...`) so the index is not used.

## Mitigation
1. Roll back the release if the query is new.
2. Creating an index on a large table must use `CREATE INDEX CONCURRENTLY`, through the database migration SOP, never as an ad-hoc command during peak hours.

## Escalation
Database team for index changes and parameter tuning.
