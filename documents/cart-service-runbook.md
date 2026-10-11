# Cart Service Runbook

## Service overview
The cart-service stores shopping carts for signed-in and guest users. Carts live in the Redis session cache with a 7-day TTL and are copied to the PostgreSQL Orders database when checkout starts. The web app and mobile-bff call cart-service; checkout-api reads the final cart.

## Symptom: items disappear from carts
1. Check the Redis session cache dashboard for evictions (`evicted_keys` rising) and memory above 90%.
2. Confirm the cart TTL in the current config is still 7 days. A config push that sets TTL in seconds instead of hours has caused this before.
3. Check whether guest carts are affected only. Guest carts are keyed by a cookie; a cookie domain change on the web app will make carts look empty.
4. Review cart-service logs for `WRONGTYPE` or serialization errors after a deployment.

## Symptom: add-to-cart latency above 300 ms (p95)
1. Compare cart-service latency with Redis command latency. If Redis is slow, follow the Redis memory eviction runbook.
2. Check pod CPU throttling. cart-service is CPU-limited at 500m per pod.
3. Scale replicas within the approved limit of 24 if traffic is the cause.

## Escalation
Escalate to the checkout team if cart data loss is confirmed for more than 1% of active carts. Do not flush Redis to "fix" corrupted carts; that deletes every active session.
