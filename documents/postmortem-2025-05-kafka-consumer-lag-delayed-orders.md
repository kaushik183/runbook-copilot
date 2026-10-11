# Postmortem: Order Fulfillment Delayed by Consumer Lag (May 2025)

**Severity:** SEV-2 · **Duration:** 3 hours 5 minutes · **Owner:** Order management team

## Summary
order-fulfillment-worker fell far behind on the `payments.captured` topic. Paid orders were not sent to the warehouse, and about 2,300 orders missed the same-day dispatch cut-off.

## Timeline (UTC)
- 10:30 Warehouse system API latency rises from 200 ms to 6 seconds.
- 10:45 Consumer lag alert fires (threshold: 1,000 messages).
- 11:20 On-call scales workers from 6 to 24; lag still grows.
- 12:10 Discovery: the topic has 12 partitions, so only 12 workers can consume; and each worker calls the warehouse API synchronously.
- 12:40 Warehouse vendor fixes their latency problem.
- 13:35 Lag cleared.

## Root cause
Throughput was limited by a slow downstream dependency called synchronously, one message at a time. Scaling beyond the partition count had no effect.

## Lessons
Consumer lag is usually a downstream problem. The Kafka consumer lag runbook now says to check dependencies before scaling.

## Action items
- Batch warehouse API calls (up to 50 orders per request) (done).
- Increase `payments.captured` partitions to 24 (done).
- Alert on warehouse API latency above 1 second (done).
