# Break-Glass Access SOP

## Background
Engineers have read-only access to production by default. Write access to the AWS console, databases and Kubernetes `cluster-admin` is granted only through break-glass roles, which are time-limited and audited.

## When to use break-glass
Only during an active SEV-1 or SEV-2 incident when the normal path (GitOps, pipelines) is too slow or broken.

## Procedure
1. Request access in the access portal, selecting the incident ID. Approval comes from the incident commander or the on-call engineering manager.
2. Access lasts 4 hours and is logged (CloudTrail, Kubernetes audit logs, database audit).
3. Announce in the incident channel what you will do before doing it.
4. Record every manual change in the incident timeline.

## After the incident
- Any manual change must be reflected in Git/Terraform within 2 business days, or reverted.
- The security team reviews all break-glass sessions weekly.

## Not allowed even with break-glass
Reading customer payment data, exporting customer personal data, disabling audit logging, or deleting backups.
