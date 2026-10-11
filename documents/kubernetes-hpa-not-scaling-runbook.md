# Kubernetes HPA Not Scaling Runbook

## Background
Most services use a HorizontalPodAutoscaler targeting 65% CPU. Some (checkout-api, payments-service) also scale on requests per second through custom metrics.

## Symptom: load is high but replicas do not increase
1. `kubectl describe hpa <name> -n <ns>` and read the Conditions and Events.
2. **"failed to get cpu utilization"**: metrics-server is unhealthy, or the pods have no CPU **requests** set. HPA percentages are calculated against requests.
3. **"ScalingLimited: TooManyReplicas"**: the HPA is at `maxReplicas`. Raising it needs a check that the database and downstream services can handle more pods.
4. Custom metrics missing: check the Prometheus adapter pods.

## Symptom: replicas increase but pods stay Pending
The cluster has no free capacity. See the cluster autoscaler capacity runbook.

## Symptom: replica count flapping up and down
Check the scale-down stabilization window (we use 300 seconds). Flapping usually means a very short window was configured.

## Manual override
During an incident you may scale manually with `kubectl scale`, but Argo CD or the HPA may revert it. Raise `minReplicas` in Git for a lasting change.
