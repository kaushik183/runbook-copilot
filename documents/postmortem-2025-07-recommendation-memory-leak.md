# Postmortem: Homepage Slowdown from Recommendation Memory Leak (July 2025)

**Severity:** SEV-3 (raised to SEV-2 for 20 minutes) · **Duration:** 1 hour 40 minutes · **Owner:** Data science platform team

## Summary
A new version of recommendation-service leaked memory and was OOMKilled every 25 minutes. Because the web app's timeout for recommendation calls had been raised from 200 ms to 2 seconds in an unrelated change, homepage loads became slow while pods restarted.

## Impact
Homepage p95 load time went from 1.2 s to 3.8 s. Bounce rate increased by 9% during the window.

## Root cause
1. The new model-loading code kept old model versions in memory after hot reloads.
2. The web app timeout change removed the protection that made recommendations non-critical.

## Timeline (UTC)
- 09:00 Release deployed.
- 09:25 First OOMKilled restarts.
- 10:15 Homepage latency alert; SEV-2 declared.
- 10:20 `reco.enabled=false`; homepage latency normal.
- 10:40 Release rolled back; recommendations re-enabled.

## Action items
- Contract test: web app must not wait more than 200 ms for optional services (done).
- Memory growth alert for recommendation-service (done).
