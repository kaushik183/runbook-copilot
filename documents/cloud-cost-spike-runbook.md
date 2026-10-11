# Cloud Cost Spike Runbook

## Trigger
AWS Cost Anomaly Detection alerts when daily spend for a service is more than 30% above its expected value, or when the forecast for the month exceeds budget by 10%.

## Checks
1. Open Cost Explorer grouped by service, then by usage type, for the last 7 days.
2. Common causes in our environment:
   - **NAT gateway data processing**: a service pulling large data from S3 or ECR without VPC endpoints, or a retry loop calling an external API.
   - **EC2**: the cluster autoscaler added nodes that never scaled down (pods without PodDisruptionBudgets or with local storage block scale-down), or spot fell back to on-demand.
   - **CloudWatch Logs**: debug logging left enabled in production.
   - **Data transfer**: cross-zone traffic from a chatty service, or a public bucket being downloaded heavily.
   - **RDS**: storage autoscaling or provisioned IOPS increased during an incident and was not reduced.
3. Check whether the increase lines up with a deployment or incident.

## Actions
Fix the cause rather than deleting resources. Any deletion of production resources needs owning team approval and goes through Terraform.

## Ownership
Platform team investigates; owning teams fix their services. Cost anomalies above 1,000 EUR per day are reported in the weekly engineering review.
