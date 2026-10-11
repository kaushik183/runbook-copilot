# Alert Playbook: High 5xx Error Rate

**Alert:** `HighErrorRate` · **Fires when:** 5xx responses above 2% of requests for a service for 5 minutes (pages above 5%).

## What it means
The service is returning server errors to clients. 5xx counts errors from our side, not client mistakes (4xx).

## First checks (5 minutes)
1. Is it one service or many? Many services at once suggests a shared dependency: DNS, ingress, database, Redis, or Kafka.
2. Did anything change? Check Argo CD for deployments and the flag service audit log in the last 30 minutes.
3. Which endpoints? Group errors by route; one endpoint failing points to a specific dependency.
4. Which status code? 502/503 often mean no healthy pods or a crashing upstream; 500 means an application exception; 504 means a timeout.

## Typical actions
- Recent deployment correlated: roll back (deployment rollback SOP).
- Dependency down: follow that dependency's runbook and consider disabling the feature with a kill switch.
- No change and no dependency issue: check traffic volume for a spike or an attack (DDoS runbook).

## Related
Checkout API runbook (502 after deployment), ingress 504 runbook, load balancer health check runbook.
