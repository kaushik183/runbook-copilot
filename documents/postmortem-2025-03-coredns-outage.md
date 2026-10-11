# Postmortem: Cluster DNS Failures (March 2025)

**Severity:** SEV-1 · **Duration:** 26 minutes · **Owner:** Platform team

## Summary
CoreDNS pods were overloaded after a node group upgrade reduced their replica count. Services failed to resolve internal and external hostnames, causing errors across checkout, payments and search.

## Impact
Error rate above 30% for most services for 26 minutes.

## Timeline (UTC)
- 11:02 Node group upgrade drains nodes; CoreDNS drops to 2 replicas because its PodDisruptionBudget allowed it.
- 11:05 DNS timeouts begin; many services alert at once.
- 11:14 SEV-1 declared; DNS suspected because errors are spread across unrelated services.
- 11:21 CoreDNS scaled to 8 replicas manually.
- 11:28 Error rates return to normal.

## Root cause
CoreDNS ran with a fixed replica count of 2 instead of proportional autoscaling, and its PodDisruptionBudget allowed both replicas to be disrupted during the upgrade. Services resolving DNS on every request amplified the load.

## Action items
- Run CoreDNS with the cluster-proportional autoscaler, minimum 4 replicas (done).
- Deploy NodeLocal DNSCache on all nodes (done).
- PodDisruptionBudget `maxUnavailable: 1` for CoreDNS (done).
