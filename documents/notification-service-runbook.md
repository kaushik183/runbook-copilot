# Notification Service Runbook

## Overview
notification-service sends order confirmations, shipping updates, password resets and one-time codes by email and SMS through two external providers. Messages are queued on Kafka (`notifications.outbound`) and sent by workers with automatic retry and exponential backoff.

## Symptom: customers not receiving emails
1. Check the queue depth and consumer lag of the notification workers.
2. Check the provider's delivery dashboard for bounces and blocks. A spike in hard bounces can get our sending domain throttled.
3. Verify SPF, DKIM and DMARC records were not changed in DNS.

## Symptom: one-time codes delayed
One-time codes block sign-in, so treat delays over 2 minutes as SEV-2.
1. Check SMS provider latency and error codes.
2. Fail over to the secondary SMS provider using the flag `notify.sms_provider=secondary`.

## Symptom: duplicate emails
Usually caused by consumer rebalances during deploys. Check that workers commit offsets after sending and that the deduplication key (message ID) is present.

## Escalation
Escalate to the growth engineering team for template problems and to the platform team for Kafka issues.
