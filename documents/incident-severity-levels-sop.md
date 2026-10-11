# Incident Severity Levels SOP

Severity decides who is paged, how fast we respond, and how we communicate. When unsure, choose the **higher** severity; it can be lowered later.

| Level | Definition | Examples | Response |
|---|---|---|---|
| SEV-1 | Critical customer impact or data/security risk | Checkout down, payments failing for most users, expired public certificate, data breach | Page on-call + incident commander immediately; status page within 15 minutes; updates every 30 minutes |
| SEV-2 | Major feature degraded or a significant share of users affected | Checkout error rate above 5%, one-time codes delayed, overselling, orders delayed more than 1 hour | Page on-call; incident commander assigned; status page if customer-visible |
| SEV-3 | Minor impact or internal tools affected, workaround exists | Search results stale, admin portal slow, one carrier failing with fallback working | Handle in business hours unless it is getting worse |
| SEV-4 | No customer impact | Recommendations missing, a non-critical batch job failed | Ticket in the owning team's backlog |

## Rules
- Any engineer may declare an incident by posting in #incidents with `/incident declare`.
- Security incidents are at least SEV-2 until the security team says otherwise.
- SEV-1 and SEV-2 incidents require a postmortem within 5 business days.
