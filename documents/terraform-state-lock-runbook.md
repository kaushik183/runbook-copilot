# Terraform State Lock Runbook

## Background
Infrastructure is managed with Terraform. State is stored in S3 and locked with a DynamoDB table so two runs cannot change the same stack at once. All applies run through the CI pipeline, not from laptops.

## Symptom: "Error acquiring the state lock"
1. Read the lock info in the error: who holds it, when, and which operation.
2. Check whether a pipeline run is still in progress for that stack. If yes, wait; it will release the lock.
3. If the run was cancelled or the runner crashed, the lock can remain after the job is gone.

## Releasing a stale lock
1. Confirm no apply is running (check the pipeline and ask in the platform channel).
2. Run `terraform force-unlock <LOCK_ID>` from the pipeline's maintenance job.
3. Run `terraform plan` before any apply to check the state is consistent with reality.

## Never
Never force-unlock while another apply might be running; two concurrent applies can corrupt state. Never edit the state file by hand. Never apply emergency changes from a laptop during an incident without the platform team.
