# On-Call Handoff SOP

On-call shifts rotate weekly on Monday at 10:00 local time. Primary and secondary on-call are scheduled in PagerDuty for each team.

## Before the handoff (outgoing engineer)
1. Write a handoff note in the team's on-call channel covering:
   - Open incidents and their current state.
   - Alerts that fired more than twice and whether they were noise.
   - Ongoing risky work: migrations, feature rollouts, change freezes.
   - Anything that needs follow-up during the next shift.
2. Close or reassign tickets created during the shift.

## At the handoff
Hold a 15-minute call. The incoming engineer confirms they can access PagerDuty, the VPN, Grafana, Argo CD, the AWS console (read-only role) and the break-glass procedure.

## During the shift
- Acknowledge pages within 5 minutes (SEV-1/SEV-2) and start working within 15 minutes.
- If you cannot respond (travel, illness), swap shifts in PagerDuty and tell the team.
- Escalate to secondary on-call after 15 minutes without progress.

## Noisy alerts
Every alert that woke someone up without needing action must get a ticket to fix or delete it.
