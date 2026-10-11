# Postmortem: Carrier API Timeouts from NAT Port Exhaustion (June 2025)

**Severity:** SEV-3 · **Duration:** 1 hour 30 minutes · **Owner:** Logistics engineering team

## Summary
shipping-service started opening a new HTTPS connection for every carrier rate request after an HTTP client library upgrade. During a traffic peak the NAT gateway ran out of ports for connections to the carrier's IP address.

## Impact
Shipping options at checkout fell back to flat rates for about 30% of requests. Label creation was delayed by up to 45 minutes.

## Timeline (UTC)
- 16:00 Traffic peak; NAT `ErrorPortAllocation` rises.
- 16:10 Carrier timeouts alert.
- 16:40 Platform team links timeouts to NAT port allocation errors.
- 17:05 Connection pooling restored by configuration; errors stop.
- 17:30 Label backlog cleared.

## Root cause
The library upgrade changed the default to no keep-alive. Each request used a new source port, and connections in TIME_WAIT kept ports busy.

## What went well
The `shipping.fallback_rates` flag kept checkout working.

## Action items
- Explicit connection pooling configuration in all HTTP clients (done).
- Alert on NAT `ErrorPortAllocation` above 0 (done).
