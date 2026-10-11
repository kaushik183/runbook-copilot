# Ingress 504 Gateway Timeout Runbook

## What it means
The NGINX ingress controller waited for the upstream service longer than its timeout (60 seconds by default, 30 seconds for checkout paths) and returned 504.

## Checks
1. Identify which paths return 504 from the ingress logs or the 5xx dashboard grouped by `path` and `service`.
2. Check the upstream service's own latency. If p99 latency is near the timeout, the service is slow, not the ingress.
3. Look for slow dependencies: database queries, a third-party API, or a lock.
4. Check whether the upstream pods are CPU throttled.

## Common causes
- A long-running report or export behind a normal HTTP request. These must run as background jobs.
- Database connection pool exhaustion: requests wait for a connection until the ingress gives up.
- A third-party API (payment provider, carrier) responding slowly without a client timeout.

## Mitigation
Fix or roll back the slow upstream. Raising the ingress timeout is not a fix; it only makes users wait longer and holds more connections.
