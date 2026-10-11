# Alert Playbook: Synthetic Check Failure

**Alert:** `SyntheticCheckFailed` · **Fires when:** a synthetic user journey fails from 2 or more locations in a row.

## Background
Synthetic checks run every minute from three regions and act like a real customer:
1. Load the homepage.
2. Search for a test product and open it.
3. Add it to the cart.
4. Check out with a test card in the payment provider's test mode.
5. Sign in and view "My orders".

## What to do
1. Open the failed run: it shows the step that failed, a screenshot and the HTTP responses.
2. Failure from one region only: probably a network problem near that region; check again before escalating.
3. Failure from all regions: treat as a likely SEV-1/SEV-2 and confirm with real-user metrics (error rate, checkout success rate).
4. Failure at the payment step only: check the payment provider's test environment status before assuming production is broken.

## Common false alarms
- The test product was deleted or went out of stock in the catalog.
- The test account's password was rotated without updating the check.
Fix false alarms the same day; noisy synthetic checks get ignored.
