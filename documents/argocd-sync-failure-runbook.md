# Argo CD Sync Failure Runbook

## Background
All Kubernetes deployments are GitOps-based: the desired state lives in the `deploy-manifests` repository, and Argo CD syncs it to the cluster. Releases change the image tag in Git.

## Symptom: application stuck "OutOfSync" or "Degraded"
1. Open the application in Argo CD and read the sync result for the failing resource.
2. **Validation errors**: an invalid manifest (for example a typo in a field name). Fix it in Git; Argo CD will retry.
3. **Hook failed**: a pre-sync job such as a database migration failed. Read the job logs before retrying (see the failed database migration runbook).
4. **Degraded health**: the resource applied but pods are not becoming ready. Follow the CrashLoopBackOff or ImagePullBackOff runbooks.

## Symptom: manual changes keep being reverted
Self-heal is enabled, so manual `kubectl edit` changes are reverted within 3 minutes. Make changes in Git. During a SEV-1 the incident commander may disable auto-sync for one application; re-enable it after the incident.

## Rollback
Prefer reverting the Git commit. Argo CD's "History and Rollback" is allowed during incidents but must be followed by a Git revert so Git matches the cluster.
