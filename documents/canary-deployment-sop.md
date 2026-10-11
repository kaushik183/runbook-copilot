# Canary Deployment SOP

## Background
Customer-facing services (checkout-api, payments-service, auth-service, mobile-bff) deploy with canaries managed by Argo Rollouts.

## Default steps
1. 5% of traffic to the new version for 10 minutes.
2. 25% for 10 minutes.
3. 50% for 10 minutes.
4. 100%.

## Automatic analysis
At each step, Argo Rollouts compares the canary with the stable version:
- HTTP 5xx rate must not exceed stable by more than 0.5 percentage points.
- p95 latency must not exceed stable by more than 20%.
- Business metric: payment success rate (payments-service only).
If analysis fails, the rollout aborts and traffic returns to the stable version automatically.

## On-call responsibilities
- Watch the rollout in Argo CD during working hours. Deployments to these services are not allowed after 17:00 or on Fridays without approval.
- If you see a problem the analysis missed, abort manually: `kubectl argo rollouts abort <rollout> -n <ns>`.

## Database changes
Canaries mean two versions run at the same time. Schema changes must work for both versions (expand-and-contract), as described in the database migration SOP.
