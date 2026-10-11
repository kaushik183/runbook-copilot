# Alert Playbook: SLO Error Budget Burn Rate

**Alerts:** `SLOFastBurn` (pages) and `SLOSlowBurn` (ticket).

## Background
Checkout has an availability SLO of 99.9% of successful requests over 30 days, which allows about 43 minutes of full outage per month (the error budget). Burn rate measures how fast we spend that budget.

| Alert | Condition | Meaning |
|---|---|---|
| Fast burn | Burn rate above 14.4 over 1 hour (and over 5 minutes) | At this rate the monthly budget is gone in about 2 days |
| Slow burn | Burn rate above 3 over 6 hours | Budget gone in about 10 days |

## What to do
- **Fast burn**: treat as an active incident. Follow the high 5xx error rate playbook.
- **Slow burn**: usually a low, constant error rate (for example one endpoint failing for some users). Find the top failing routes and open a ticket for the owning team the same day.

## Error budget policy
If more than 75% of the monthly budget is spent, the owning team pauses feature releases and works on reliability until the budget recovers. Exceptions require the head of engineering.
