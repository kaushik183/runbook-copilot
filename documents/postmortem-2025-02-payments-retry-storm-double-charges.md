# Postmortem: Duplicate Charges from Payment Retry Storm (February 2025)

**Severity:** SEV-1 · **Duration:** 1 hour 20 minutes · **Owner:** Payments team

## Summary
A release changed how payments-service builds idempotency keys. During a short slowdown at the payment provider, automatic retries created a second charge for some customers.

## Impact
412 customers were charged twice. All duplicates were refunded within 24 hours.

## Timeline (UTC)
- 14:05 Release deployed; idempotency key now included a timestamp.
- 14:40 Provider latency rises to 4 seconds; clients retry after 3 seconds.
- 15:02 Support reports double charges. SEV-1 declared.
- 15:18 Release rolled back.
- 16:00 Duplicate charges identified and refunds started.

## Root cause
The idempotency key must be stable for the same order. Adding a timestamp made every retry look like a new request. Tests did not cover retries after a timeout.

## Contributing factors
- Client retry timeout (3 s) was shorter than provider latency during the slowdown.
- No alert on "more than one capture per order".

## Action items
- Contract test: same order must always produce the same idempotency key (done).
- Alert when an order has more than one successful capture (done).
- Retry only with exponential backoff and a maximum of 2 retries (done).
