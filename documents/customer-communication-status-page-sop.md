# Customer Communication and Status Page SOP

## When to post
- SEV-1: always, within 15 minutes of declaring the incident.
- SEV-2: if customers can notice it (failed checkouts, login problems, delayed confirmations).
- SEV-3/SEV-4: normally not.

## Who posts
The comms lead, assigned by the incident commander. Engineers working on the fix should not write status updates.

## How to write updates
- Describe the impact in customer terms: "Some customers cannot complete checkout" rather than "checkout-api 502s".
- Do not guess the cause or promise a time to fix.
- Post updates at least every 30 minutes for SEV-1, every 60 minutes for SEV-2, even if nothing changed.
- Never mention vendors by name or blame a third party publicly.

## Templates
- **Investigating**: "We are investigating reports that some customers are unable to <action>. We will share an update within 30 minutes."
- **Identified**: "We have identified the cause and are working on a fix. Orders already placed are not affected."
- **Resolved**: "The issue has been resolved. Customers can <action> normally. We apologise for the inconvenience."

## Internal updates
Post a short summary in #incidents-announce for support and leadership after each status page update.
