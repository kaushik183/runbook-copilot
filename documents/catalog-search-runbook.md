# Catalog Search Runbook

## Overview
catalog-search serves product search and category pages from an Elasticsearch 8 cluster (3 master, 6 data nodes). Product updates arrive from Kafka (`catalog.updated`) and are indexed by the `search-indexer` deployment. A full reindex takes about 40 minutes.

## Symptom: search returns no or stale results
1. Check cluster health: `GET _cluster/health`. Yellow is degraded but serving; red means some shards are unassigned.
2. Check `search-indexer` consumer lag. Stale prices or stock usually mean indexing is behind, not that search is broken.
3. Confirm the `products` alias points at the current index: `GET _alias/products`.

## Symptom: search latency above 800 ms (p95)
1. Check JVM heap usage on data nodes. Above 85% sustained causes long GC pauses.
2. Look for expensive queries (leading wildcards, very large `size`) in the slow log.
3. Enable the "simple search" fallback flag `search.degraded_mode`, which disables facets and typo tolerance.

## Reindex rule
Always reindex into a new index and switch the alias when complete. Never delete the live index first.

## Escalation
Escalate to the search team for red cluster health lasting more than 10 minutes.
