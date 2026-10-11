# Escalation Policy SOP

## Paging order
1. Primary on-call for the owning team (acknowledge within 5 minutes).
2. Secondary on-call (auto-escalation after 10 minutes without acknowledgement).
3. Engineering manager of the owning team (after 20 minutes).
4. Head of engineering for SEV-1 lasting more than 1 hour.

## Which team owns what
| Area | Owning team |
|---|---|
| checkout-api, cart-service | Checkout team |
| payments-service, payment provider integration | Payments team |
| fraud-service, manual review | Risk team |
| inventory-service, pricing-service | Commerce platform team |
| Kubernetes, ingress, load balancers, VPC, Kafka, Redis | Platform team |
| PostgreSQL, PgBouncer, migrations | Database team |
| auth-service, WAF, secrets, access | Security team |
| catalog-search | Search team |

## Cross-team escalation
Page the other team directly through PagerDuty; do not wait for a reply in chat. Include: incident channel link, severity, what you observed, and what you need from them.

## Vendors
Payment provider, carriers and AWS support cases are opened by the owning team. For SEV-1, open AWS support cases with "Production system down" priority.
