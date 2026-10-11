# Kubernetes CrashLoopBackOff Runbook

## What it means
A container starts, exits, and Kubernetes restarts it with growing delays (up to 5 minutes). The pod never becomes ready, so it receives no traffic.

## Checks, in order
1. Find the exit reason: `kubectl describe pod <pod> -n <ns>` and read **Last State** (exit code and reason).
   - Exit code 1 or 2: the application crashed. Read the logs.
   - Exit code 137 with reason `OOMKilled`: see the OOMKilled runbook.
   - Exit code 143: the container was terminated (often by a failing liveness probe).
2. Read the logs of the **previous** container: `kubectl logs <pod> -n <ns> --previous`. The current container may not have logged anything yet.
3. Check configuration: missing environment variables, a missing Secret or ConfigMap key, or a wrong database URL are the most common causes after a deploy.
4. Check the liveness probe. A probe with too short an `initialDelaySeconds` kills slow-starting apps before they are ready.
5. Check dependencies the app needs at startup (database, Redis, Kafka). Many of our services exit if a dependency is unreachable at boot.

## Mitigation
If the crash started with a new release, roll back using the deployment rollback SOP. Do not delete the pods repeatedly; the logs you need disappear with them.
