# Fraud Detection Service Runbook

## Overview
fraud-service scores every payment attempt before authorization. Scores above 0.9 are declined, scores between 0.6 and 0.9 go to manual review. payments-service calls it with a 300 ms timeout.

## Fail-open versus fail-closed
If fraud-service times out, payments-service **fails open for orders under 200 EUR** (payment continues) and **fails closed above 200 EUR** (sent to manual review). This policy was agreed with the risk team; do not change it during an incident.

## Symptom: decline rate jumps
1. Compare the fraud decline rate with the last 7 days. A doubling usually means a bad model or rule change, not a real attack.
2. Check the rules changelog in the risk console for changes in the last 24 hours.
3. Roll back the model version with the flag `fraud.model_version` after approval from the risk on-call.

## Symptom: manual review queue overflowing
Notify the risk operations lead. Orders waiting more than 24 hours are auto-cancelled.

## Escalation
Risk team on-call for model and rule changes; payments team for timeout problems.
