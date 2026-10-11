# NAT Gateway and Egress Failures Runbook

## Background
Private subnets reach the internet through one NAT gateway per availability zone. External dependencies reached this way include the payment provider, carriers, email/SMS providers and the feature-flag service.

## Symptom: timeouts to every external API, internal traffic fine
1. Check NAT gateway metrics: `ErrorPortAllocation` and `PacketsDropCount`. Port allocation errors mean too many simultaneous connections to the same destination.
2. Check whether only one availability zone is affected; the route table for that zone's subnets may point at a deleted or failed NAT gateway.
3. Check recent changes to route tables, network ACLs and security group egress rules.

## Symptom: port allocation errors
A service is opening a new connection per request to the same host. Fix the client to reuse connections (keep-alive). As a short-term mitigation, scale that service down or spread traffic across zones.

## Cost note
NAT data processing is expensive. Large transfers to AWS services (S3, ECR) should use VPC endpoints instead of the NAT gateway.

## Escalation
Platform team owns the VPC and NAT gateways.
