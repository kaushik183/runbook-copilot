# CoreDNS Resolution Failures Runbook

## Symptoms
Errors such as `no such host`, `i/o timeout` on DNS lookups, or `EAI_AGAIN` across several services at the same time.

## Checks
1. Check CoreDNS pods in `kube-system`: restarts, CPU throttling, and the `coredns_dns_requests_total` and error metrics.
2. Test from a debug pod: `kubectl run dnsutils --rm -it --image=<internal dnsutils image> -- nslookup orders-db.internal`.
3. Separate internal names (`*.svc.cluster.local`) from external names. If only external names fail, check the VPC resolver and outbound DNS limits.
4. Check for the per-ENI DNS packet limit (1024 packets per second). High-traffic nodes can hit it; NodeLocal DNSCache reduces this.

## Mitigation
- Scale CoreDNS up (we run at least 4 replicas; scale to 8 during incidents).
- Restart only CoreDNS pods that are unhealthy, one at a time.
- Make sure applications reuse connections; services that resolve DNS on every request amplify the problem.

## Escalation
Platform team. Cluster-wide DNS failure is SEV-1 because almost every request depends on it.
