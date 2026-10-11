# API Gateway and Ingress Runbook

## Overview
Public traffic flows: Route 53 -> CloudFront (static assets) / AWS Application Load Balancer -> NGINX ingress controller in Kubernetes -> services. The ingress controller runs 6 replicas across three availability zones and terminates TLS with certificates from ACM at the load balancer.

## Symptom: many services return 502 or 503 at once
1. Check ingress controller pods: restarts, CPU, and the `nginx_ingress_controller_requests` metric by status.
2. Check for a recent ingress configuration change. One invalid annotation can make the controller reject a reload; look for `Error reloading NGINX` in its logs.
3. Check load balancer target health. If targets are unhealthy, see the load balancer health check runbook.

## Symptom: one service returns 502
The problem is usually the service, not the ingress. Check the service's endpoints: `kubectl get endpoints <service> -n <namespace>`. Empty endpoints mean no ready pods.

## Rate limiting
Global rate limits are set per client IP (100 requests/second). Raising them during an attack is not allowed; contact the security team instead.

## Escalation
The platform team owns the ingress controller and load balancer.
