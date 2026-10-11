# DDoS and WAF Runbook

## Background
AWS Shield Standard protects the load balancer and CloudFront. AWS WAF runs managed rule groups (common exploits, known bad IPs, bot control) plus our own rate-based rules.

## Symptoms of an attack
- Sudden traffic increase (5x or more) without a marketing event.
- Many requests from few IP ranges, unusual countries, or a single user agent.
- High rate of 4xx (login attempts) or requests to random URLs.

## Steps
1. Confirm it is not legitimate traffic: check with the commercial team for campaigns, launches or press coverage.
2. Open the WAF dashboard: top client IPs, countries, URIs and rules matched.
3. **Credential stuffing** (many failed logins): enable the stricter login rate rule and CAPTCHA on `/login` (security team).
4. **Volumetric attack on one URL**: add a temporary WAF rule to rate limit or block that pattern. Rules start in **count** mode for 5 minutes to check for false positives, unless the site is already down.
5. Scale ingress and checkout services if real customers are affected by load.

## Escalation
Security team owns WAF rules. For large attacks, the security team engages the AWS Shield Response Team (requires Shield Advanced on the affected resource).

## Do not
Do not block entire countries or large IP ranges without security team approval; carrier-grade NAT can make many real customers share one IP.
