# Hotfix Release SOP

## What a hotfix is
A small, targeted code change released outside the normal schedule to fix a production problem when rollback is not possible (for example, the bug exists in the last two releases, or rollback would undo a required migration).

## Rules
1. Keep it minimal: fix the bug only. No refactoring, no unrelated changes.
2. Branch from the commit currently in production, not from `main`, if `main` contains unreleased changes.
3. At least one reviewer from the owning team. During SEV-1 the reviewer can approve on a call.
4. CI must pass. Skipping tests requires incident commander approval and is recorded in the postmortem.
5. Deploy through the normal pipeline and canary steps. The canary steps may be shortened to 5 minutes each with IC approval.

## After release
- Merge the fix back into `main`.
- Watch the metrics that showed the problem for 30 minutes.
- Add a regression test in a follow-up change if one was not included.

## During a change freeze
Hotfixes for SEV-1/SEV-2 are allowed with incident commander approval.
