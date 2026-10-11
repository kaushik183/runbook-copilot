# Recommendation Service Runbook

## Overview
recommendation-service powers "You may also like" and homepage carousels. It is **non-critical**: pages must load without it. Calls from the web app have a 200 ms timeout and fall back to bestseller lists.

## Symptom: high memory and restarts
recommendation-service loads a model file of about 2 GB into memory at startup.
1. Check for `OOMKilled` restarts (see the Kubernetes OOMKilled runbook).
2. Confirm the model file size did not grow after the nightly training job. Pods are limited to 4 GiB.
3. Roll back to the previous model version with the flag `reco.model_version`.

## Symptom: pages slow because of recommendations
1. Confirm the web app timeout is still 200 ms. If recommendation calls are blocking page rendering, the timeout was changed.
2. Disable recommendations with `reco.enabled=false`; the bestseller fallback is shown instead.

## Priority
Recommendation outages alone are SEV-4 unless they slow down page loads. Do not wake the data science team at night for SEV-4.
