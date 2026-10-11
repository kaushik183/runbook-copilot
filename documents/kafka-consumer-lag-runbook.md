# Kafka Consumer Lag Runbook

## What it means
Consumer lag is the number of messages written to a topic but not yet processed by a consumer group. Lag that keeps growing means consumers are slower than producers.

## Alert thresholds
- `fulfillment` group on `payments.captured`: lag above 1,000 or older than 5 minutes (SEV-2, delays orders).
- `inventory-sync` and `search-indexer`: lag above 50,000 (SEV-3, stale data).
- `notifications`: lag older than 2 minutes for one-time codes (SEV-2).

## Checks
1. Is lag on all partitions or only one? One partition means a stuck consumer or a poison message on that partition.
2. Check consumer pods: restarts, CPU, and errors. Frequent rebalances (consumers joining and leaving) stop processing each time.
3. Check the consumer's downstream dependency (database, external API). Consumers are usually slow because what they call is slow.
4. Check for a producer burst, for example a bulk catalog import.

## Mitigation
1. Scale consumers up to the number of partitions; more consumers than partitions do nothing.
2. Move poison messages to the dead-letter topic.
3. Fix the slow dependency.

## Do not
Do not reset consumer offsets to "latest" to clear lag; that silently skips messages (lost orders or notifications). Offset changes need approval from the owning team.
