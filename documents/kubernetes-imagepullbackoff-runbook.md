# Kubernetes ImagePullBackOff Runbook

## What it means
The node cannot download the container image, so the pod stays in `ImagePullBackOff` or `ErrImagePull`.

## Checks
1. `kubectl describe pod <pod> -n <ns>` and read the Events section for the exact error.
2. **"manifest unknown" / "not found"**: the image tag does not exist in Amazon ECR. Usually the CI build failed but the deployment manifest was still updated. Confirm the tag in ECR.
3. **"no basic auth credentials" / 403**: the node role lost permission to read from ECR, or the image is in a different AWS account. Check the node IAM role policy.
4. **Timeouts**: nodes cannot reach ECR. Check the NAT gateway and the ECR VPC endpoints.
5. **Rate limits from Docker Hub**: we must not pull from Docker Hub in production. Mirror the image into ECR.

## Mitigation
Running pods with the old image keep serving traffic, because a rolling update does not remove them until new pods are ready. Fix the image reference or roll back the manifest in Git; Argo CD will sync it.

## Prevention
Deployment manifests must reference immutable tags (Git SHA), never `latest`.
