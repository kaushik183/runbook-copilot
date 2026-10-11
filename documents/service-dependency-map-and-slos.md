# Service Dependency Map and SLOs

| Service | Critical dependencies | Availability SLO | Latency SLO (p95) | Tier |
|---|---|---|---|---|
| checkout-api | auth, cart, pricing, inventory, payments, Orders DB | 99.9% | 1.2 s | Tier 1 |
| payments-service | payment provider, fraud-service, Payments DB | 99.9% | 900 ms | Tier 1 |
| auth-service | Users DB, Redis | 99.95% | 250 ms | Tier 1 |
| cart-service | Redis, Orders DB | 99.9% | 300 ms | Tier 1 |
| inventory-service | Inventory DB, Kafka | 99.9% | 300 ms | Tier 1 |
| pricing-service | Promotions DB | 99.9% | 250 ms | Tier 1 |
| mobile-bff | Tier 1 services | 99.9% | 800 ms | Tier 1 |
| catalog-search | Elasticsearch | 99.5% | 800 ms | Tier 2 |
| shipping-service | carrier APIs (fallback rates) | 99.5% | 700 ms | Tier 2 |
| order-fulfillment-worker | Kafka, warehouse API | Orders processed within 10 minutes (99%) | n/a | Tier 2 |
| notification-service | Kafka, email/SMS providers | Delivered within 2 minutes (99%) | n/a | Tier 2 |
| recommendation-service | model store | 99% | 200 ms | Tier 3 |
| admin-portal | internal APIs, SSO | 99% (business hours) | 2 s | Tier 3 |

## Tiers
- **Tier 1**: on the purchase path. Pages 24/7, canary deployments required.
- **Tier 2**: important but has a fallback or delay tolerance. Pages 24/7 for SEV-2+.
- **Tier 3**: degrade gracefully; business-hours response.
