# Spot Instance Interruption Runbook

## Background
Stateless, non-critical workloads (recommendation-service, search-indexer, batch jobs, notification workers) may run on the `spot-general` node group. AWS can reclaim spot instances with a 2-minute warning. The AWS Node Termination Handler cordons and drains the node when a warning arrives.

## Symptom: many pods restarting at once on spot nodes
1. Check the Node Termination Handler logs for interruption notices.
2. Check the spot interruption rate for the instance types used. We spread across at least 4 instance types to reduce simultaneous interruptions.

## Symptom: customer-facing service affected by spot interruptions
Customer-facing services (checkout-api, payments-service, auth-service, cart-service) must **not** run on spot nodes. Check their node affinity and tolerations. Move them back to the on-demand group immediately.

## Good practice for spot workloads
- Handle SIGTERM and finish in-flight work within 90 seconds.
- Use a PodDisruptionBudget so not all replicas are drained together.
- Keep enough replicas in different zones.

## Escalation
Platform team if interruptions exceed 20% of spot capacity in an hour.
