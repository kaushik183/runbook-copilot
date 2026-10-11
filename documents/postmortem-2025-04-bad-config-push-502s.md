# Postmortem: 502 Errors After Configuration Change (April 2025)

**Severity:** SEV-2 · **Duration:** 34 minutes · **Owner:** Checkout team

## Summary
A configuration change for checkout-api pointed it at a new Payment Gateway URL that only existed in staging. New pods failed readiness checks; as the rollout continued, healthy capacity shrank and the load balancer returned 502s.

## Impact
Checkout error rate peaked at 18%. About 1,100 checkouts failed.

## Timeline (UTC)
- 13:10 ConfigMap change merged and synced by Argo CD.
- 13:14 New pods fail readiness; rollout continues because `maxUnavailable` was 50%.
- 13:19 502 alerts fire.
- 13:31 Deployment timestamp correlated with the incident; config change identified.
- 13:36 Git revert synced; pods become ready.
- 13:44 Error rate normal.

## Root cause
Configuration changes were not deployed through the canary process, and the rollout settings allowed half of the pods to be unavailable.

## What went well
The checkout runbook's "compare with the latest deployment timestamp" step pointed to the cause quickly.

## Action items
- ConfigMap changes for checkout-api go through Argo Rollouts canaries (done).
- `maxUnavailable: 0`, `maxSurge: 25%` for customer-facing deployments (done).
- Startup check that validates the Payment Gateway URL (done).
