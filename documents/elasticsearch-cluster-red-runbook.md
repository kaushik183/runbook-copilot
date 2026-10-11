# Elasticsearch Cluster Red or Yellow Runbook

## What it means
- **Yellow**: all primary shards are assigned, some replicas are not. Search works but there is less redundancy.
- **Red**: at least one primary shard is unassigned. Searches on that index return partial results or errors.

## Checks
1. `GET _cluster/health` and `GET _cat/shards?v&h=index,shard,prirep,state,unassigned.reason`.
2. Ask why a shard is unassigned: `GET _cluster/allocation/explain`.
3. Common reasons:
   - A data node left the cluster (check node count and pod restarts).
   - Disk watermark exceeded: above 85% disk, Elasticsearch stops allocating shards to that node; above 95% indices become read-only.
   - Too many shards for the heap size.

## Mitigation
1. Bring back the missing node or add capacity.
2. Free disk by deleting **old** indices left over from previous reindexes (never the one behind the `products` alias).
3. After freeing disk, remove the read-only block: `PUT _all/_settings {"index.blocks.read_only_allow_delete": null}`.
4. If a primary shard is lost permanently, rebuild the index with a full reindex from the catalog database (about 40 minutes) and switch the alias.

## Customer mitigation
Enable `search.degraded_mode` to reduce query load while the cluster recovers.
