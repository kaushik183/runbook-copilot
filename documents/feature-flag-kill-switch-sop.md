# Feature Flag Kill Switch SOP

## Background
Feature flags are managed in the feature-flag service and evaluated in each application with a local cache (refreshed every 30 seconds). If the flag service is unreachable, applications use the last known values, then the defaults in code.

## Kill switches
A kill switch is a flag that turns off a feature quickly and safely. Important ones:
| Flag | Effect when OFF |
|---|---|
| `pricing.promotions_enabled` | All promotions disabled |
| `reco.enabled` | Recommendations hidden, bestseller fallback shown |
| `search.degraded_mode` (ON) | Simple search without facets |
| `shipping.fallback_rates` (ON) | Flat-rate shipping when carriers fail |
| `checkout.express_pay` | Express wallet buttons hidden |

## When to use a kill switch
When a feature is causing customer impact and turning it off is faster than a rollback. Kill switches are allowed during change freezes.

## Procedure
1. Announce in the incident channel which flag you will change and why.
2. Change the flag in the flag service (production environment only, never "all environments").
3. Watch metrics for 5 minutes to confirm the effect.
4. Record the change in the incident timeline.

## Afterwards
Turning the feature back on is a normal change: it needs the owning team's approval and is not done in the middle of the night.
