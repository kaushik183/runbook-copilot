# Postmortem: Overselling a Limited-Edition Product (March 2025)

**Severity:** SEV-2 · **Duration:** 18 minutes · **Owner:** Commerce platform team

## Summary
A limited-edition sneaker launch with 500 units in stock received 9,000 checkout attempts in the first minute. 1,240 orders were accepted, so 740 had to be cancelled.

## Impact
740 customer cancellations and significant social media complaints.

## Timeline (UTC)
- 10:00 Launch.
- 10:01 Stock reaches zero in the inventory database, but orders keep being accepted.
- 10:08 Merchandising notices negative available stock in the admin portal.
- 10:12 SKU paused in the admin portal.
- 10:18 Incident closed; cancellations started.

## Root cause
The `inventory.strict_reservation` flag was OFF in production after a test the week before. Without it, inventory-service checks stock but does not lock the row while reserving, so concurrent checkouts all saw stock available.

## Action items
- `inventory.strict_reservation` cannot be turned off in production without commerce-platform approval (done).
- Load test for launch events with 10x expected concurrency (done).
- Queue-based "waiting room" for high-demand launches (planned).
