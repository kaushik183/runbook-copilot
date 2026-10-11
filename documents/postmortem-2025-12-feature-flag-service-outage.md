# Postmortem: Feature Flag Service Outage (December 2025)

**Severity:** SEV-3 · **Duration:** 2 hours · **Owner:** Platform team

## Summary
The external feature-flag service had an outage. Most services continued with cached flag values as designed, but newly started pods had no cache and fell back to code defaults, which turned **off** express checkout and **on** an unfinished new checkout layout.

## Impact
For about 2 hours, customers served by new pods saw an incomplete checkout layout. Conversion on those pods dropped by 12%.

## Timeline (UTC)
- 12:00 Flag service outage begins.
- 12:40 HPA scales checkout web pods up for lunchtime traffic; new pods use code defaults.
- 13:10 Product team reports the unfinished layout in production.
- 13:30 Code defaults identified as the cause; checkout web scaled back to the old pods' count.
- 14:00 Flag service recovers.

## Root cause
Code defaults did not match production values. Defaults for unfinished features must always be "off".

## Action items
- Lint rule: new feature flags must default to off (done).
- Ship a snapshot of production flag values with each release as a secondary fallback (done).
