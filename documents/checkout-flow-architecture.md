# Checkout Flow Architecture

## Step by step
1. The client calls `POST /checkout` on checkout-api with the cart ID and a valid JWT.
2. checkout-api loads the cart from cart-service (Redis) and asks pricing-service for the final price.
3. inventory-service reserves stock for each item (15-minute reservation).
4. checkout-api creates an order in the Orders database with status `pending_payment`.
5. payments-service calls fraud-service (300 ms timeout), then the payment provider to authorize the card, using an idempotency key derived from the order ID.
6. On success, the order becomes `paid`; payments-service publishes `payments.captured` to Kafka.
7. order-fulfillment-worker consumes the event, sends the order to the warehouse and asks shipping-service for a label.
8. notification-service sends the confirmation email.

## Failure handling
- Payment declined: reservation released, order marked `payment_failed`, customer can retry.
- Payment provider timeout: payments-service retries up to 2 times with backoff using the same idempotency key, so no double charge.
- Fraud-service timeout: fail open under 200 EUR, manual review above.
- Kafka unavailable after payment: the event is stored in an outbox table and published when Kafka recovers, so paid orders are never lost.

## Latency budget
Target p95 for `POST /checkout`: 1.2 seconds, of which the payment provider typically takes 400-700 ms.
