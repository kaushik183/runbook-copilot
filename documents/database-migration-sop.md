# Database Migration SOP

## Principles
1. **Backward-compatible**: the running application version must work with both the old and new schema.
2. **Expand and contract**: add new columns or tables first (expand), move the code over, then remove old ones in a later release (contract).
3. **No long locks**: anything that rewrites or locks a large table during business hours is not allowed.

## Safe and unsafe operations (PostgreSQL)
| Operation | Safe? | Notes |
|---|---|---|
| Add nullable column | Yes | Instant |
| Add column with constant default | Yes | Instant in PostgreSQL 11+ |
| Create index | Only `CONCURRENTLY` | Cannot run in a transaction |
| Add foreign key | Use `NOT VALID`, then `VALIDATE` separately | Avoids long locks |
| Rename or drop column | Only in the contract phase | After no code uses it |
| Change column type | Usually no | Rewrites the table; plan with the database team |

## Process
1. Migration reviewed by the database team for tables over 1 million rows.
2. Tested against a staging copy with production-like data size.
3. Set `lock_timeout = '5s'` in migrations so they fail fast instead of blocking traffic.
4. Run through the Argo CD pre-sync job, never by hand.

## If it fails
Follow the failed database migration runbook.
