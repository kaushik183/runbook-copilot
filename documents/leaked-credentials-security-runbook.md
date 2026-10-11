# Leaked Credentials Security Runbook

## When to use
A secret (API key, password, access key, private key, token) may have been exposed: committed to a repository, pasted in chat or a ticket, shown in logs, or found by secret scanning.

## Immediate steps
1. Declare a security incident (at least SEV-2) and page the security team.
2. Do **not** delete the commit or message first. Deleting does not undo exposure, and the security team needs the evidence (time, location, who could see it).
3. Identify the credential: what system, what permissions, which environments.

## Contain
1. Rotate the credential using the secrets rotation SOP. If it is being actively abused, revoke immediately even if this causes an outage; the security team decides.
2. For AWS access keys: deactivate the key, then review CloudTrail for every action taken with it since the exposure time.
3. For payment or carrier keys: ask the provider for activity logs and restrict the new key by source IP where possible.

## Investigate
Check logs for use of the credential from unknown IP addresses or at unusual times. Assume it was used if the exposure was public for more than a few minutes.

## Afterwards
Remove the secret from Git history only after rotation. Write a postmortem; the fix is usually a process or tooling gap (for example missing pre-commit scanning).
