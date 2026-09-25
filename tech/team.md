# Team Workflow — Senior + 2 Workers + 2 Supervisors

## Roles

| Role | Who | Reads extra | Owns |
|---|---|---|---|
| Supervisor | product owner + AI supervisor | everything | direction, `main`, merges, final reports |
| Senior | build agent #1 | this file + all of `tech/` | reviews, integration verdicts, consolidated reports, next orders |
| Worker A | build agent #2 | this file + assigned tasks | backend + engine + API tests (default lane) |
| Worker B | build agent #3 | this file + assigned tasks | frontend + smoke tests (default lane) |

Default lanes are a starting point — senior may rebalance any task in `STATUS.md`.

## Branches

- `main` — supervisors merge ONLY. Always green, always deployable.
- `w-a/<task>-<slug>` — worker A, one branch per task (e.g. `w-a/T-001-django-skeleton`).
- `w-b/<task>-<slug>` — worker B, same rule.
- `senior/fix-<slug>` — senior may open for integration fixes only (still merged by supervisors).
- Never push to `main`. Never commit to another role's branch. Branch from latest `main`.

## Worker cycle (per task)

1. Read your order in `STATUS.md` (task + branch name). Mark task 🔄 doing.
2. Branch from `main`. Implement ONLY that task's scope + its tests.
3. Run the gates: `make check` (lint+type+unit) and anything the task lists. All green.
4. Push branch. Write report `reports/worker-a/<TASK>.md` (or `worker-b/`) from
   `reports/_TEMPLATE_WORKER.md`. Update `STATUS.md` board → `✅ pending-review`.
5. STOP and wait. Do not start the next task until senior posts new orders.

## Senior cycle (per review round)

1. Read worker branches + reports. Check out each branch, run `make check` + relevant
   `tech/tests.md` items yourself. Review diffs for scope creep and rule violations.
2. Write consolidated review `reports/senior/<MILESTONE>-review-<n>.md` from
   `reports/_TEMPLATE_SENIOR.md`: verdict per branch (approve / request-changes with
   exact fixes), consolidated test evidence, integration notes.
3. Post next orders in `STATUS.md` (task → worker + branch names). Update board.
4. If workers disagree or a doc gap appears, decide (or escalate to supervisors) and log
   the decision in `STATUS.md`. Ties are yours to break; supervisors override you.

## Supervisor cycle

1. Read senior reports. Spot-check branches and preview deploys.
2. Merge approved branches to `main` (squash, one merge per task). Read final milestone
   report, approve next milestone in `STATUS.md`.

## STATUS.md protocol

- Single coordination file at repo root. Append-only, dated entries — never rewrite history.
- Sections: milestone + goal / task board / orders (senior→workers) /
  message board (any→any: thoughts, opinions, proposals) / decisions / blockers.
- Workers: update board on start/finish; post blockers immediately, never stall silently.
- Senior: posts every order + verdict there (reports/ holds the full text).

## Quality gates (block any "done")

- `make check` green (lint + typecheck + unit + compose build).
- Coverage: `engine/` ≥ 90%, backend overall ≥ 80%.
- `make verify-ports` green (exactly ONE published port).
- `make size` within budgets: backend ≤ 350MB, frontend ≤ 250MB.
- `tech/tests.md` section C (safety) re-verified after any prompt/copy/engine change.

## Prohibitions

- Workers: no merges, no `main` pushes, no unassigned tasks, no skipped tests, no new
  dependencies without senior approval (free + OSS-licensed only, logged in report).
- Senior: no merges to `main`, no silent scope changes (log + escalate), no review
  without running the tests.
- Everyone: no secrets in repo (`.env` local only), no second published port, no
  business logic in frontend components, no LLM-side scoring.
