# Change Freeze SOP

## When freezes apply
- Black Friday through Cyber Monday (Thursday 00:00 to Tuesday 23:59).
- The last week of December.
- Any major marketing event announced by the commercial team at least two weeks ahead.

## What is frozen
Production deployments, infrastructure changes (Terraform), feature-flag changes that alter checkout, payments or pricing behaviour, and database migrations.

## What is allowed
- Fixes for active SEV-1/SEV-2 incidents, approved by the incident commander.
- Disabling a feature through an existing kill switch.
- Scaling within approved limits.
- Content changes in the CMS and promotion setup in the admin portal (owned by the commercial team).

## Exception process
Request an exception in #change-freeze with: what changes, why it cannot wait, rollback plan, and who will watch the release. It needs approval from the head of engineering and the owning team's manager.

## Before the freeze
- Pre-scale node groups, Redis and database capacity based on last year's peak plus 30%.
- Run a load test against staging with peak traffic profiles.
- Confirm on-call coverage, with secondary on-call physically available.
