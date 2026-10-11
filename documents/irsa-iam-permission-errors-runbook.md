# IAM Roles for Service Accounts (IRSA) Permission Errors Runbook

## Background
Pods get AWS permissions through IRSA: each Kubernetes service account is annotated with an IAM role ARN, and the AWS SDK exchanges the pod's web identity token for role credentials.

## Symptom: AWS calls fail with AccessDenied or "unable to locate credentials"
1. Check the service account: `kubectl get sa <name> -n <ns> -o yaml` and confirm the `eks.amazonaws.com/role-arn` annotation.
2. Check the pod actually uses that service account (`spec.serviceAccountName`).
3. Check the role's trust policy: it must trust the cluster's OIDC provider and the exact `system:serviceaccount:<ns>:<name>` subject.
4. Confirm the pod has the projected token: environment variables `AWS_ROLE_ARN` and `AWS_WEB_IDENTITY_TOKEN_FILE` should exist.
5. Old SDK versions do not support web identity credentials and fall back to the node role.

## After moving a service to a new namespace
The trust policy subject includes the namespace, so it must be updated. This is the most common cause of IRSA failures after a migration.

## Fix
Update the role or trust policy in Terraform, then restart the pods so they pick up a fresh token.
