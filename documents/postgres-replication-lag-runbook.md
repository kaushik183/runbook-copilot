# PostgreSQL Replication Lag Runbook

## Background
The Orders database has one read replica used by reporting, the admin portal search and some read-only API endpoints. Alert: replica lag above 30 seconds for 5 minutes.

## Why it matters
Readers on the replica see old data. Customers may not see a just-placed order in "My orders", and admin staff may act on stale stock values.

## Checks
1. Check the `ReplicaLag` metric in CloudWatch and the replica's CPU and IOPS.
2. Look for heavy queries on the replica (reporting exports) competing with replay.
3. Check the primary for very large write bursts: bulk imports, big `UPDATE` statements, or migrations rewriting tables.
4. Long queries on the replica can delay replay if `hot_standby_feedback` conflicts occur; check for `canceling statement due to conflict with recovery` errors.

## Mitigation
1. Pause or reschedule bulk jobs on the primary.
2. Stop heavy reporting queries on the replica.
3. If lag exceeds 5 minutes, switch read-after-write endpoints ("My orders") to the primary with the flag `orders.read_from_primary=true`. Watch primary load when doing this.

## Escalation
Database team if lag keeps growing for more than 15 minutes.
