# Payment Gateway Integration Runbook

## Service overview
payments-service talks to our external payment provider over HTTPS. Every charge request carries an idempotency key built from the order ID, so a retried request must never create a second charge. Webhooks from the provider confirm captures and refunds.

## Symptom: payment authorization failures above 3%
1. Check the provider's public status page and our `payment_provider_errors_total` metric grouped by error code.
2. Separate declines (customer card problems, normal at 1-2%) from technical errors (timeouts, 5xx). Only technical errors are an incident.
3. If timeouts dominate, check egress through the NAT gateway and DNS resolution for the provider hostname.
4. Confirm the API credentials have not expired. Credentials rotate every 90 days per the secrets rotation SOP.

## Symptom: webhooks not arriving
1. Check the webhook endpoint returns 200 within 5 seconds; the provider retries for 24 hours, then gives up.
2. Verify the webhook signing secret matches the value in the secrets manager.
3. Replay missed webhooks from the provider dashboard once the endpoint is healthy.

## Safety rules
Never disable idempotency keys to "unblock" payments. Never retry charges manually from a laptop. Escalate to the payments team and the provider's support line for incidents longer than 15 minutes.
