# Pricing and Promotions Runbook

## Overview
pricing-service returns the final price for a cart, applying promotions, coupon codes and member discounts. Promotion rules are edited in the admin portal and cached in pricing-service for 60 seconds.

## Symptom: wrong prices or discounts at checkout
1. Treat a discount that is too large as SEV-1 if it is being exploited publicly; it causes direct revenue loss.
2. Identify the promotion ID from pricing-service logs (`applied_promotions` field).
3. Disable the promotion in the admin portal. The change takes effect within 60 seconds.
4. If the admin portal is unavailable, use the kill switch flag `pricing.promotions_enabled=false`, which disables all promotions.

## Symptom: pricing timeouts slow down checkout
1. Check pricing-service latency and its dependency on the promotions database.
2. A promotion with thousands of eligible SKUs can make evaluation slow; check for recently created large promotions.

## After the incident
Export the list of affected orders for the finance team. Do not cancel orders without approval from customer support leadership.

## Escalation
Escalate to the pricing team and inform the commercial on-call manager.
