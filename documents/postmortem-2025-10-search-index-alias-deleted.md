# Postmortem: Search Outage from Deleted Index (October 2025)

**Severity:** SEV-2 · **Duration:** 1 hour 15 minutes · **Owner:** Search team

## Summary
During cleanup of old indices, an engineer ran a delete with a wildcard pattern that matched the live `products-2025-10-02` index behind the `products` alias. Search and category pages returned empty results.

## Impact
Search and browse were unavailable for 1 hour 15 minutes; product pages opened from direct links still worked. Orders fell by about 35% during the window.

## Timeline (UTC)
- 15:05 `DELETE products-2025-*` executed to remove old indices.
- 15:07 Empty search results alert.
- 15:15 Cause identified.
- 15:16 `search.degraded_mode` enabled (no effect: no index).
- 15:20 Full reindex from the catalog database started.
- 16:20 Reindex complete; alias switched to new index.

## Root cause
Wildcard deletes were allowed in production, and nothing protected the index behind the live alias.

## Action items
- `action.destructive_requires_name: true` on the cluster (wildcard deletes blocked) (done).
- Cleanup script that skips any index referenced by an alias (done).
- Keep the previous index for 7 days after each reindex for fast rollback (done).
