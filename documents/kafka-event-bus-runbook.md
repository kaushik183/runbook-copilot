# Kafka Event Bus Runbook

## Overview
The event bus is Amazon MSK (Kafka 3.x, 3 brokers, replication factor 3, `min.insync.replicas=2`). Main topics: `orders.created`, `payments.captured`, `stock.changed`, `catalog.updated`, `notifications.outbound`.

## Symptom: producers failing with `NotEnoughReplicas`
1. Check broker health in the MSK console. With one broker down, writes still work; with two down they fail by design.
2. Check broker disk usage. A full disk takes a broker offline. Retention is 7 days; reduce retention on large topics only with platform-team approval.

## Symptom: consumers far behind
See the Kafka consumer lag runbook. Most lag comes from slow consumers, not from Kafka itself.

## Symptom: under-replicated partitions
1. Usually follows a broker restart or MSK maintenance. Watch the count fall over 10-20 minutes.
2. If it does not recover, open an AWS support case.

## Rules
Never delete a topic to clear a backlog. Never reduce the replication factor in production. Topic creation goes through Terraform, not the Kafka CLI.
