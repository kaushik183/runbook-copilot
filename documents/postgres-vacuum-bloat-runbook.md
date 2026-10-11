# PostgreSQL Vacuum and Bloat Runbook

## Background
PostgreSQL does not remove updated or deleted rows immediately; autovacuum cleans them later. If cleanup falls behind, tables and indexes grow ("bloat") and queries slow down.

## Symptoms
- A table's size grows much faster than its row count.
- Queries on frequently updated tables (orders, inventory reservations, sessions) get slower over days.
- Warning: `database is not accepting commands to avoid wraparound data loss` (emergency, SEV-1).

## Checks
1. Last autovacuum per table and dead tuples: `SELECT relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;`
2. Long-running transactions block vacuum from removing rows. Check `pg_stat_activity` for transactions open for hours.
3. Abandoned replication slots also hold back cleanup.

## Mitigation
1. End long-running transactions (database team approval).
2. Run a manual `VACUUM (VERBOSE, ANALYZE) <table>` during low traffic.
3. For severe index bloat use `REINDEX INDEX CONCURRENTLY`.

## Never
Do not run `VACUUM FULL` on a production table during business hours; it takes an exclusive lock and blocks all reads and writes.
