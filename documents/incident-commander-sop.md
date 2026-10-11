# Incident Commander SOP

The incident commander (IC) coordinates the response. The IC does **not** debug; they make sure the right people are working on the right things and that everyone knows what is happening.

## When an IC is required
Every SEV-1 and SEV-2. The first responder is the IC until someone from the IC rotation takes over.

## IC checklist
1. Open the incident channel (`#inc-<date>-<short-name>`) and the video bridge.
2. Confirm severity and write a one-line summary of customer impact.
3. Assign roles: **Ops lead** (drives technical investigation), **Comms lead** (status page and internal updates), **Scribe** (timeline).
4. Every 15-30 minutes ask: what do we know, what are we trying, what is the next decision?
5. Prefer mitigation over root cause: roll back, fail over, or disable a feature first; investigate after customers recover.
6. Approve risky actions explicitly (rollbacks, failovers, disabling auto-sync, data changes).
7. Declare the incident resolved only after metrics are stable for 15 minutes.
8. Assign a postmortem owner before closing.

## Handover
If the incident lasts longer than 3 hours, hand over to a fresh IC with a written summary in the channel.
