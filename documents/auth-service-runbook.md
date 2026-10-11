# Auth Service Runbook

## Overview
auth-service handles sign-in, sign-up and token issuance. It issues short-lived JWT access tokens (15 minutes) and refresh tokens (30 days) signed with keys stored in the secrets manager. Every other service validates tokens using the public keys published at `/.well-known/jwks.json`.

## Symptom: users cannot sign in
1. Check auth-service error rate and the dependency on the users table in PostgreSQL.
2. Check the rate limiter. Credential-stuffing attacks trigger lockouts that can also hit real users; look at the WAF dashboard.
3. Confirm the email/SMS provider is healthy if sign-in uses one-time codes (see notification-service runbook).

## Symptom: every service returns 401 at the same time
This almost always means a signing key problem.
1. Check whether a key rotation ran recently.
2. Confirm the JWKS endpoint returns both the new and previous key. During rotation both must be published for at least 30 minutes.
3. Check clock skew on nodes; tokens appear expired if a node clock is wrong by more than 60 seconds.

## Safety rules
Do not extend token lifetimes as an incident fix. Do not disable signature validation in any service. Escalate to the security team for suspected account takeover.
