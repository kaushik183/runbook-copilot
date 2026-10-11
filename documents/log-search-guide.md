# Log Search Guide

Logs from all pods are collected by Fluent Bit and stored in Loki for 14 days. Search them in Grafana Explore with the **Loki** data source.

## Log format
Services log JSON with these fields: `level`, `service`, `trace_id`, `request_id`, `route`, `status`, `duration_ms`, `msg`.

## Useful queries
- Errors for one service in the last hour: `{namespace="checkout", app="checkout-api"} | json | level="error"`
- Count errors by route: `sum by (route) (count_over_time({app="checkout-api"} | json | level="error" [5m]))`
- Follow one request across services: `{namespace=~".+"} | json | trace_id="<id>"`
- Slow requests: `{app="checkout-api"} | json | duration_ms > 2000`

## Good practice
- Narrow by namespace and app labels first; full-text search across everything is slow.
- Use `trace_id` from an error log to open the trace in Tempo and see which dependency was slow.
- Never log secrets, full card numbers or passwords. If you find such data in logs, report it to the security team immediately.

## When logs are missing
Check the Fluent Bit DaemonSet on the node and whether the application writes to stdout. Files written inside the container are not collected.
