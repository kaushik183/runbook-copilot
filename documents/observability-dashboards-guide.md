# Observability Dashboards Guide

All dashboards are in Grafana under the folder **Production**.

## Start here
- **Production Overview**: request rate, error rate and latency for every customer-facing service, plus checkout success rate and orders per minute. Open this first during any incident.
- **Business KPIs**: orders, payment success rate, conversion rate, compared with the same time last week. Use it to estimate customer impact.

## Service dashboards
Every service has a dashboard named after it (for example **checkout-api**) with the four golden signals: traffic, errors, latency, saturation; plus pod restarts, CPU throttling and dependency latency.

## Infrastructure dashboards
- **Kubernetes Cluster**: nodes, pending pods, node pressure conditions.
- **Orders DB**: connections, PgBouncer pools, slow queries, replica lag, storage.
- **Redis Session Cache**: memory, evictions, command latency, connections.
- **Kafka**: consumer lag per group, under-replicated partitions, broker disk.
- **Ingress**: requests by status and upstream, reload errors.

## Tips
- Use the deployment annotations (vertical lines) to spot changes that line up with problems.
- Compare with "same time last week" before concluding traffic is abnormal.
- Take screenshots for the incident timeline; Grafana links can change.
