# Inventory Service Runbook

## Service overview
inventory-service tracks stock levels for every SKU and reserves stock when a customer starts checkout. Reservations expire after 15 minutes if payment is not completed. It publishes `stock.changed` events to the Kafka event bus.

## Symptom: checkout fails with "item unavailable" while stock exists
1. Check the reservation table for expired reservations that were not released. The release job runs every minute; look for `reservation-release` CronJob failures in Kubernetes.
2. Compare stock in the inventory database with the value shown on the product page. The product page reads from catalog-search, which can lag if Kafka consumers are behind.
3. Check Kafka consumer lag for the `inventory-sync` consumer group.

## Symptom: overselling (orders accepted for out-of-stock items)
1. Treat as a SEV-2 incident: overselling creates customer-facing cancellations.
2. Confirm whether reservation locking is enabled. The feature flag `inventory.strict_reservation` must be ON in production.
3. Check for database deadlock or lock-timeout errors in inventory-service logs.
4. Pause the affected SKUs through the admin portal rather than disabling inventory checks globally.

## Escalation
Escalate to the database team for lock contention that continues after traffic is reduced, and to the merchandising on-call for any SKU-level manual stock correction.
