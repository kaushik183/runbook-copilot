# Postmortem: Mobile Users Blocked by Rate Limiting (August 2025)

**Severity:** SEV-2 · **Duration:** 52 minutes · **Owner:** Platform team

## Summary
A new global rate limit of 100 requests per second per client IP was enabled on the ingress. Many mobile users on a large carrier share a small pool of public IP addresses (carrier-grade NAT), so thousands of real users looked like one client and received HTTP 429 errors.

## Impact
About 22% of mobile app requests from that carrier failed. App store reviews mentioned "app not loading".

## Timeline (UTC)
- 18:00 Rate limit enabled during a routine change.
- 18:12 Mobile error rate alert; web traffic normal.
- 18:30 429s grouped by client IP show a handful of IPs with huge volume.
- 18:45 Rate limit for authenticated mobile traffic switched to per-user-token instead of per-IP.
- 18:52 Recovery.

## Root cause
Per-IP limits do not work for traffic behind carrier-grade NAT. The change was tested only with web traffic patterns.

## Action items
- Rate limit authenticated traffic per user token; keep per-IP limits only for unauthenticated endpoints (done).
- Roll out rate-limit changes in "log-only" mode for 24 hours first (done).
