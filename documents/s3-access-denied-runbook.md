# S3 Access Denied Runbook

## Symptom
A service logs `AccessDenied` (HTTP 403) when reading or writing an S3 bucket.

## Checks
1. Identify the exact bucket, key and IAM role from the error or from CloudTrail.
2. Check what changed recently:
   - Bucket policy edits (a `Deny` statement wins over every `Allow`).
   - The service's IAM role policy (Terraform change).
   - The service account annotation that maps the pod to its IAM role (see the IRSA runbook).
   - KMS key policy, if the bucket uses SSE-KMS. The role needs `kms:Decrypt` and `kms:GenerateDataKey`.
3. Use the IAM policy simulator with the role and the action to confirm which statement denies it.

## Common mistake
Granting `s3:GetObject` on `arn:aws:s3:::bucket` instead of `arn:aws:s3:::bucket/*`. Object actions need the `/*` resource.

## Mitigation
Revert the change in Terraform and apply it through the pipeline. Do not make manual IAM edits in the console; the next Terraform run reverts them and the state drifts.

## Escalation
Platform team for IAM; security team for any public-access change.
