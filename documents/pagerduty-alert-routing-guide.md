# PagerDuty Alert Routing Guide

## How alerts reach people
Prometheus Alertmanager sends alerts to PagerDuty. Each alert has a `team` label and a `severity` label.

| Severity label | Routing |
|---|---|
| `page` | Pages the owning team's primary on-call immediately, 24/7 |
| `ticket` | Creates a ticket for the owning team, no page |
| `info` | Slack channel only |

## Rules for new alerts
1. Page only for customer impact or imminent customer impact (for example storage filling within hours). Everything else is a ticket.
2. Every paging alert must link to a runbook in its `runbook_url` annotation.
3. Alert on symptoms (errors, latency, SLO burn) rather than causes (CPU usage) where possible.
4. Test new alerts in `info` mode for a week before switching them to `page`.

## Maintenance and silences
Create a silence in Alertmanager for planned maintenance, with an end time and a comment linking the change. Never create silences without an end time.

## Escalation
Unacknowledged pages escalate to secondary on-call after 10 minutes, then to the engineering manager after 20 minutes (escalation policy SOP).
