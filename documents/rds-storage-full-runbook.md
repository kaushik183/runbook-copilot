# RDS Storage Full Runbook

## Background
RDS storage autoscaling is enabled up to a maximum of 2 TiB for the Orders database. Alerts fire when free storage drops below 15% and page below 10%.

## Why it is urgent
When storage fills completely the database becomes read-only and every write fails. Recovery requires a storage increase, which can take time to apply.

## Checks
1. Check the free storage graph. Is it a slow trend or a sudden drop?
2. Sudden drop causes:
   - A long-running transaction or an abandoned replication slot keeping WAL files: `SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) FROM pg_replication_slots;`
   - A large data import or a table rewrite from a migration.
   - Temporary files from huge sorts.
3. Check whether autoscaling hit its maximum.

## Mitigation
1. Database team increases allocated storage (allowed once every 6 hours).
2. Drop inactive replication slots only after confirming no consumer needs them.
3. Stop the import or migration that is consuming space.

## Never
Do not delete table data to free space without the data owner's approval.
