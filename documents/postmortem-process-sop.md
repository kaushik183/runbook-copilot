# Postmortem Process SOP

## When a postmortem is required
SEV-1 and SEV-2 incidents, and any incident involving data loss, security, or a near miss the IC thinks we can learn from.

## Timeline
- Owner assigned by the IC before the incident is closed.
- Draft within 3 business days, review meeting within 5 business days.

## Blameless principle
Postmortems focus on systems and processes, not individuals. Write "the deploy pipeline allowed an untested config" rather than "Alex pushed a bad config". People act reasonably with the information and tools they have.

## Template
1. **Summary**: two or three sentences.
2. **Impact**: duration, affected customers, orders/revenue affected, SLO budget used.
3. **Timeline**: detection, key decisions, mitigation, resolution (UTC times).
4. **Root cause and contributing factors**: use "5 whys"; there is rarely a single cause.
5. **What went well / what went badly / where we got lucky.**
6. **Action items**: each with an owner, a ticket and a due date. Prefer items that prevent the whole class of problem.

## Follow-up
Action items are reviewed in the weekly reliability meeting until closed. Postmortems are published internally so every team can learn from them.
