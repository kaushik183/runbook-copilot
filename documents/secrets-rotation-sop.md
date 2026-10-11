# Secrets Rotation SOP

## Where secrets live
All application secrets are stored in AWS Secrets Manager and synced into Kubernetes Secrets by the External Secrets Operator (refresh every 5 minutes). Secrets must never be committed to Git or pasted into chat or tickets.

## Rotation schedule
| Secret type | Rotation |
|---|---|
| Database passwords | Automatic, every 30 days |
| Payment provider API keys | Every 90 days |
| Carrier and email/SMS provider keys | Every 180 days |
| JWT signing keys | Every 90 days, overlapping |
| Any secret possibly exposed | Immediately |

## Zero-downtime rotation
1. Create the new credential while the old one still works (most providers allow two active keys).
2. Update the value in Secrets Manager.
3. Wait for External Secrets to sync, then restart the pods (rolling restart) so they read the new value.
4. Confirm traffic succeeds with the new credential.
5. Revoke the old credential.

## Emergency rotation (leaked secret)
Follow the leaked credentials security runbook. Revoke first if the secret is actively abused, even if it causes a short outage; the security team decides.
