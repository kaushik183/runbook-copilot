# Postmortem: Checkout Outage from Expired TLS Certificate (January 2025)

**Severity:** SEV-1 · **Duration:** 47 minutes · **Owner:** Platform team

## Summary
The certificate for `api` hostnames expired. Browsers and the mobile apps refused to connect, so customers could not sign in, add to cart or check out.

## Impact
About 100% of API traffic failed for 47 minutes. Roughly 3,900 checkouts were not completed during the window.

## Timeline (UTC)
- 06:12 Certificate expires. Synthetic checks fail; alert routed to a muted channel.
- 06:31 Customer support reports app errors.
- 06:38 SEV-1 declared.
- 06:52 Cause identified: ACM renewal failed because the DNS validation record had been deleted in a Route 53 clean-up two months earlier.
- 06:59 Validation record restored; ACM issues a new certificate.
- 06:59 Recovery confirmed.

## Root cause
A DNS clean-up script deleted records it did not recognise, including `_acm-validations` CNAMEs. ACM sent renewal warning emails to an unmonitored mailbox.

## What went well
Once identified, the fix took 7 minutes.

## Action items
- Alert on certificate expiry at 21 and 7 days in PagerDuty (done).
- Protect ACM validation records from clean-up scripts (done).
- Route synthetic check failures to on-call, not a muted channel (done).
