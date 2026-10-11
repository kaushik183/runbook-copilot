# Shipping Service Runbook

## Overview
shipping-service calculates shipping options at checkout and creates labels with carrier APIs after an order is paid. Rate quotes are cached for 10 minutes per destination and cart weight.

## Symptom: checkout shows "no shipping options"
1. Check carrier API error rates. One carrier outage should not remove all options; if it does, the fallback rate table may be disabled.
2. Ensure flag `shipping.fallback_rates` is ON. It shows flat-rate options when carriers time out.
3. Check for address validation failures caused by a recent change in address formatting.

## Symptom: labels not created for paid orders
1. Check the `label-creation` queue and the dead-letter topic.
2. Inspect the most common carrier error. Invalid package dimensions are a frequent cause after catalog imports.
3. Replay dead-lettered messages after the cause is fixed using the replay job, not by hand.

## Business impact
Orders without labels miss the warehouse cut-off at 16:00 local time. Notify the fulfillment operations channel if more than 200 orders are blocked.

## Escalation
Escalate to the logistics engineering team and, for carrier outages, open a ticket with the carrier.
