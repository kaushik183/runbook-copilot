# Order Fulfillment Worker Runbook

## Overview
order-fulfillment-worker consumes `payments.captured` events, marks orders as paid, sends them to the warehouse system, and triggers label creation in shipping-service. It is idempotent: processing the same event twice must not send an order to the warehouse twice.

## Symptom: paid orders stuck in "processing"
1. Check consumer lag for the `fulfillment` consumer group.
2. Check the dead-letter topic `payments.captured.dlq` for poison messages. One bad message must not block the partition; the worker moves it to the DLQ after 5 attempts.
3. Check the warehouse system API status. When it is down, the worker pauses and retries every 60 seconds.

## Symptom: orders sent to the warehouse twice
1. Stop the worker immediately (scale to 0) to prevent more duplicates.
2. Check whether the deduplication table was truncated or a migration changed its key.
3. Send the list of duplicated order IDs to warehouse operations so they can cancel picks.

## Escalation
Escalate to the order management team. Notify fulfillment operations if more than 500 orders are delayed beyond 2 hours.
