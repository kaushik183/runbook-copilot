# Payments Architecture

## Components
- **payments-service**: owns payment state, talks to the external payment provider, receives provider webhooks.
- **fraud-service**: scores every payment attempt.
- **Payments database** (PostgreSQL): payment attempts, captures, refunds. Card numbers are **never** stored; we keep only the provider's token and the last four digits.

## Flows
- **Authorize and capture**: card payments are authorized at checkout and captured immediately for in-stock items.
- **Refunds**: started from the admin portal by customer support; payments-service calls the provider and records the result. Refunds over 1,000 EUR need a second approver.
- **Webhooks**: the provider confirms captures, refunds and chargebacks. Webhooks are verified with a signing secret and processed idempotently by event ID.

## Reliability rules
- Idempotency keys come from the order ID and attempt number, never timestamps.
- At most 2 automatic retries, with exponential backoff, only for timeouts and 5xx responses.
- Reconciliation job compares our records with the provider's daily settlement report and alerts on differences.

## Compliance
Card data flows directly from the client to the provider's hosted fields, keeping our systems out of PCI DSS scope for card storage. Do not add logging that could capture raw card data.
