# Postmortem: Carrier API Key Exposed in a Public Repository (August 2025)

**Severity:** SEV-2 (security) · **Duration:** 3 hours from exposure to revocation · **Owner:** Security team

## Summary
A carrier API key was committed to a personal public repository by mistake while sharing a code sample. Automated secret scanning detected it 2 hours later.

## Impact
No evidence of misuse in the carrier's logs. The key allowed creating shipping labels billed to our account.

## Timeline (UTC)
- 09:00 Commit pushed to a public repository.
- 11:05 Secret scanning alert to the security team.
- 11:20 Security incident declared.
- 11:45 New key created and deployed (secrets rotation SOP).
- 12:00 Old key revoked; carrier confirms no unusual activity.

## Root cause
The sample code contained a real key copied from a local `.env` file. Pre-commit secret scanning was installed only on company repositories.

## Action items
- Pre-commit secret scanning on all developer laptops (done).
- Carrier keys restricted by source IP to our NAT gateway addresses (done).
- Training: use placeholder values in code samples (done).
