# Mobile BFF Runbook

## Overview
mobile-bff (backend for frontend) is the single API used by the iOS and Android apps. It aggregates calls to cart, catalog, auth, pricing and checkout services and shapes responses for the apps. Older app versions are supported for 12 months.

## Symptom: errors only on one app version
1. Group mobile-bff errors by the `app_version` header.
2. Check for a recent change that removed a field older apps still require. Response contracts are tested only against the last three app versions.
3. Restore the field or roll back mobile-bff; app store releases take days, so the server must adapt.

## Symptom: app slow, web fine
1. Compare mobile-bff latency with the downstream services it calls. A slow optional call (for example recommendations) should have a timeout.
2. Check payload size; responses above 1 MB are slow on mobile networks.

## Forced upgrade
Showing the forced-upgrade screen (`mobile.min_supported_version`) needs approval from the mobile product owner. It is a last resort.

## Escalation
Mobile platform team for mobile-bff; the owning service team for downstream errors.
