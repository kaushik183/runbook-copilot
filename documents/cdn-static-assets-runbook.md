# CDN and Static Assets Runbook

## Overview
JavaScript, CSS and product images are stored in S3 and served through CloudFront. Asset file names include a content hash, so new deployments never overwrite old files. HTML pages are not cached at the CDN.

## Symptom: blank pages or broken styling after a release
1. Open the browser console: 404s for `.js` files mean HTML references assets that were not uploaded.
2. Check the deployment pipeline step `upload-assets`. It must finish before the new web pods receive traffic.
3. Roll back the web deployment; old asset files are still in S3 because they are never deleted on deploy.

## Symptom: product images slow or missing
1. Check the CloudFront error rate (4xx/5xx) and cache hit ratio. A hit ratio below 80% puts load on the image origin.
2. Check S3 bucket policy changes. A policy that removes CloudFront's origin access causes 403s.

## Cache invalidation
Invalidate only specific paths (for example `/images/promo/*`). Wildcard invalidation of `/*` is slow and costs money; it needs approval from the platform team.
