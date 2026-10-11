# TLS Certificate Expiry Runbook

## Background
Public certificates for `www`, `api` and `m` hostnames are issued by AWS Certificate Manager and renew automatically when DNS validation records exist. Internal certificates inside the cluster are issued by cert-manager and renew 30 days before expiry.

## Alerts
`CertificateExpiresSoon` fires at 21 days and pages at 7 days.

## Symptom: certificate about to expire
1. Find out why automatic renewal did not happen. For ACM: the DNS validation CNAME was deleted from Route 53. For cert-manager: check the `Certificate` and `CertificateRequest` resources and the cert-manager logs.
2. Restore the validation record or fix the issuer, then confirm a renewed certificate is issued.

## Symptom: certificate already expired (customers see browser errors)
This is a SEV-1.
1. Request or import a valid certificate and attach it to the load balancer listener.
2. Check every place the certificate is used: load balancer, CloudFront distribution, and any partner integration that pins certificates.
3. Clear CDN and client caches are not needed; browsers pick up the new certificate on the next connection.

## Prevention
Never delete Route 53 records named `_<hash>.acm-validations` during DNS clean-ups.
