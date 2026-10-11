# Admin Portal Runbook

## Overview
The admin portal is an internal web app used by customer support, merchandising and finance. It is available only through the corporate VPN and SSO. It writes directly to the pricing, inventory and orders services through their internal APIs.

## Symptom: staff cannot log in
1. Check the SSO provider status and the admin portal's OIDC configuration.
2. Confirm the user is in the correct SSO group; access is granted per team.
3. VPN problems affect many internal tools at once; check with IT.

## Symptom: bulk actions time out
Bulk price or stock updates over 5,000 rows run as background jobs. If a job is stuck, check the `admin-jobs` deployment logs and the job table. Do not re-submit the same job before the first one is confirmed failed; that applies changes twice.

## Audit
Every admin action is written to the audit log with the user, time and before/after values. Use it to reverse a bad bulk change.

## Priority
Admin portal outages are SEV-3 unless they block a SEV-1 or SEV-2 mitigation, such as disabling a promotion.
