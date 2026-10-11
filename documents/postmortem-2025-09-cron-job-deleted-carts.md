# Postmortem: Cleanup Job Deleted Active Carts (September 2025)

**Severity:** SEV-2 · **Duration:** 40 minutes · **Owner:** Checkout team

## Summary
A nightly job that deletes abandoned carts older than 30 days ran with a wrong unit after a refactor and deleted carts older than 30 **minutes**.

## Impact
About 41,000 active carts were deleted between 02:00 and 02:40 UTC. Most were from customers in Asia-Pacific time zones who were shopping at that time.

## Timeline (UTC)
- 02:00 Job starts.
- 02:18 Cart-empty complaints in support chat.
- 02:30 On-call notices `carts_deleted` metric 200x higher than usual.
- 02:40 Job suspended (`kubectl patch cronjob ... suspend=true`).
- 03:30 Carts restored from the hourly PostgreSQL snapshot of the carts table.

## Root cause
The refactor replaced a duration string (`"30d"`) with an integer interpreted as minutes. No test checked the threshold, and the job had no safety limit.

## Action items
- Safety limit: the job aborts if it would delete more than 5% of carts in one run (done).
- Unit test for the age threshold (done).
- Alert on abnormal deletion volume (done).
