# Distributed Tracing Guide

Services send traces with OpenTelemetry to Grafana Tempo. Traces are sampled: 10% of normal requests and 100% of requests that end with an error or take longer than 2 seconds.

## When to use traces
- To find **which dependency** makes a request slow (database query, Redis, another service, an external API).
- To see the full path of a checkout request through checkout-api, cart-service, pricing-service, inventory-service and payments-service.

## How
1. Get a `trace_id` from an error log line or from an exemplar on a latency graph in Grafana.
2. Open it in Explore with the Tempo data source.
3. Look for the longest span and for spans with errors. Gaps between spans often mean time spent waiting for a connection from a pool.

## Reading common patterns
- Many short identical database spans in a row: N+1 query problem.
- One long span calling an external API: missing or too-long client timeout.
- Long span before any database call: waiting for a PgBouncer connection.

## Missing spans
A service without instrumentation shows up as a gap. Instrumentation is part of the service template; ask the platform team if a service is missing it.
