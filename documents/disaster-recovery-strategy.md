# Disaster Recovery Strategy

## Targets
| Scenario | Recovery time objective (RTO) | Recovery point objective (RPO) |
|---|---|---|
| Single pod or node failure | Automatic, under 5 minutes | No data loss |
| Single availability zone outage | Under 15 minutes (automatic for most components) | No data loss |
| Database primary failure | 1-2 minutes (Multi-AZ failover) | No data loss |
| Accidental data deletion | Under 4 hours | Up to 5 minutes (point-in-time recovery) |
| Full region outage | Under 24 hours (manual) | Up to 1 hour |

## Availability zone outage
EKS nodes, RDS Multi-AZ, ElastiCache replicas, MSK brokers and the load balancer span three zones. Services run at least 3 replicas with topology spread constraints. On a zone outage, the cluster autoscaler adds capacity in the remaining zones; pre-scale if the outage is long.

## Region outage
Infrastructure is defined in Terraform and can be created in the secondary region. Database snapshots and S3 data are copied to the secondary region every hour. The region failover plan is tested once a year and requires the head of engineering's decision to start.

## Data deletion
Restore to a new database instance from point-in-time recovery, then copy back only the affected rows. Never restore over the live database.
