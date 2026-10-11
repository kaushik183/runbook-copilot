# Failed Database Migration Runbook

## Background
Schema migrations run as an Argo CD pre-sync job before the new application version starts. Migrations must be backward-compatible: the previous application version must keep working with the new schema (expand-and-contract pattern).

## Symptom: deployment blocked by a failed migration job
1. Read the job logs: `kubectl logs job/<migration-job> -n <ns>`.
2. Check whether the migration ran partly. Our migration tool runs each migration in a transaction, but statements such as `CREATE INDEX CONCURRENTLY` cannot run inside a transaction and may leave an invalid index.
3. Check the migration history table to see which version is recorded.

## Symptom: migration is still running and holding locks
1. Find blocked queries: `SELECT pid, wait_event_type, query FROM pg_stat_activity WHERE wait_event_type = 'Lock';`
2. If customer traffic is blocked, the database team may cancel the migration's backend (`pg_cancel_backend`).

## Recovery
- The old application version keeps running because the rollout has not started. Customer impact is usually only from locks.
- Fix the migration in a new commit. Never edit a migration that has already run in production.
- Drop invalid indexes left by failed concurrent builds before retrying.

## Escalation
Database team for every production migration failure.
