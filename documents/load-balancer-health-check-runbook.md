# Load Balancer Health Check Failures Runbook

## Background
The public Application Load Balancer sends traffic to the NGINX ingress controller pods. Health checks call `/healthz` on port 10254 every 10 seconds; a target is unhealthy after 3 failures.

## Symptom: targets unhealthy, site down or partly down
1. Check target group health in the AWS console and the reason codes (`Target.Timeout`, `Target.ResponseCodeMismatch`).
2. Check the ingress controller pods. If they are healthy inside the cluster, compare security group rules: the load balancer security group must be allowed to reach the node ports.
3. Check for a recent change to security groups, network ACLs or the target group (port, path, protocol).
4. If only one availability zone is unhealthy, check node and network health in that zone.

## Symptom: healthy targets but users get 502
502 from the load balancer means the target closed the connection. Check ingress controller restarts and keep-alive settings; the ingress keep-alive must be longer than the load balancer idle timeout (60 seconds).

## Escalation
Platform team owns the load balancer, target groups and security groups. Changes go through Terraform.
