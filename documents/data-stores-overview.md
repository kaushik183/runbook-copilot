# Data Stores Overview

| Store | Technology | Used for | Backups | Owner |
|---|---|---|---|---|
| Orders DB | PostgreSQL 15, RDS Multi-AZ, 1 read replica | Orders, order items, carts snapshot | Automated daily snapshots (35 days) + point-in-time recovery | Database team |
| Users DB | PostgreSQL 15, RDS Multi-AZ | Accounts, addresses | Same as Orders | Database team |
| Inventory DB | PostgreSQL 15, RDS Multi-AZ | Stock levels, reservations | Same as Orders | Database team |
| Payments DB | PostgreSQL 15, RDS Multi-AZ, encrypted with a dedicated KMS key | Payment attempts, refunds | Same, restricted access | Payments team |
| Session cache | Redis 7, ElastiCache, 1 primary + 2 replicas | Sessions, carts, rate limits | None (rebuildable) | Platform team |
| Search | Elasticsearch 8, 6 data nodes | Product search index | Rebuilt from catalog DB | Search team |
| Event bus | Kafka on MSK, 3 brokers | Events between services, 7-day retention | Not backed up; producers use an outbox | Platform team |
| Object storage | S3 | Images, assets, exports, DB snapshots exports | Versioning on critical buckets | Platform team |

## Restore times (tested quarterly)
- PostgreSQL point-in-time restore to a new instance: about 45 minutes for the Orders DB.
- Elasticsearch full reindex: about 40 minutes.
- Redis: no restore; sessions and carts rebuild as customers return (carts can be restored from the hourly PostgreSQL snapshot).
