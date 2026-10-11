# System Architecture Overview

## Request path
Customers use the web app and the iOS/Android apps. Traffic goes through Route 53 DNS to CloudFront (static assets) and to an AWS Application Load Balancer, then to the NGINX ingress controller in our Kubernetes cluster (Amazon EKS, three availability zones).

## Main services
- **Edge**: NGINX ingress, mobile-bff (mobile API aggregation).
- **Shopping**: catalog-search (Elasticsearch), recommendation-service, cart-service, pricing-service.
- **Checkout**: checkout-api, inventory-service, payments-service, fraud-service, shipping-service.
- **After the order**: order-fulfillment-worker, notification-service.
- **Identity**: auth-service (JWT tokens).
- **Internal**: admin-portal.

## Data stores
- PostgreSQL on RDS: Orders, Users, Inventory, Promotions databases (via PgBouncer).
- Redis on ElastiCache: sessions, carts, rate limits.
- Elasticsearch: product search index.
- Kafka on MSK: events between services.
- S3: assets, exports, backups.

## Delivery and operations
GitOps with Argo CD, canaries with Argo Rollouts, infrastructure in Terraform, metrics in Prometheus, logs in Loki, traces in Tempo, dashboards in Grafana, paging through PagerDuty.

## Critical path
Checkout depends on: ingress, auth-service, cart-service, pricing-service, inventory-service, payments-service (plus the external payment provider), Orders database and Redis. Search and recommendations are not on the checkout critical path.
