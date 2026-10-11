# Blue-Green Deployment SOP

## When we use blue-green
For components that cannot run two versions side by side with split traffic: the NGINX ingress controller, the web front-end asset bundle, and major version upgrades of the admin portal.

## How it works
Two complete environments exist: **blue** (current) and **green** (new). Green is deployed and tested while blue serves all traffic. Then traffic switches to green at once. Blue stays running for quick rollback.

## Procedure
1. Deploy green and run the smoke test suite against its internal URL.
2. Announce the switch in #deployments.
3. Switch traffic (service selector or load balancer target group change).
4. Watch error rate, latency and business metrics for 15 minutes.
5. Keep blue running for at least 2 hours, then scale it down.

## Rollback
Switch traffic back to blue. Because blue was never changed, rollback takes seconds.

## Cautions
- Both environments share the same database; schema changes must be backward-compatible.
- Background workers must run in only one environment at a time to avoid processing messages twice.
- Blue-green doubles resource usage temporarily; check cluster capacity before starting.
