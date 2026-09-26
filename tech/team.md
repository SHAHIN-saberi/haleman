# Build Protocol — Solo-Senior Mode

## Status of this file

Since 2026-09-26 the build runs in **solo-senior mode**: one agent does architecture, backend/engine, frontend,
tests and reviews. The former three-agent model (senior + worker-a + worker-b) is **retired**; its structure below
the line is kept as history and as the source of the gates, which are unchanged.

## Roles

| Role | Who | Owns |
|---|---|---|
| Owner (product owner) | the human | direction, every plan gate, milestone verdicts, merges to `main`, anything product-facing (copy, colours, legal, provider keys, therapist list) |
| Solo senior | the build agent | architecture, `backend/` + `engine/`, `frontend/`, tests, reviews, reports, deployments artefacts |

There are no worker lanes any more. The old split (backend lane / frontend lane) survives only as a rule about
**where code lives**: backend/engine logic in `backend/`, UI in `frontend/`, zero business logic in the frontend.

## Branching

- One branch per session: `arena/<id>-haleman`. Everything for a task goes there; no per-task branches any more.
- `main` is the owner's. The agent never pushes to it. Merges happen only when the owner says "merge", and the
  final merge of the session branch is a **squash merge** through one PR.
- Historical names (`w-a/*`, `w-b/*`, `senior/*`) are dead; branches already merged stay merged.

## Step cycle (replaces worker/senior cycles)

1. **Plan gate** — post the next step to the owner in Persian, ≤10 lines: task, scope, files to be touched,
   acceptance criteria from `tech/tasks.md` / `tech/tests.md`, and any open question. Wait for «تأیید».
   A reply that changes course = revise the plan and ask again; do not argue.
2. **Build** — only that scope, plus its tests.
3. **Self-review** — run every gate that can run; review the diff for scope creep and rule violations; keep raw
   outputs for the report.
4. **Report** — `reports/senior/<TASK>.md` (what, files, commands, real outputs, missing evidence labelled
   MISSING), update the `STATUS.md` board row → `✅ done-on-branch (awaiting owner)`, append a dated entry,
   commit `T-xxx: <summary>`, push the session branch.
5. **Done gate** — report to the owner in Persian, ≤8 lines. Wait for his approval before the next step.

Milestone gate: `reports/senior/M<n>-final.md` against `tech/tests.md` §B, then the owner's verdict.

## STATUS.md protocol

- Single coordination file at repo root. Append-only, dated entries — never rewrite history.
- Sections: milestone + goal / task board / orders / message board / decisions / blockers.
- The board is the truth for "what is done"; a task is only `✅` when its report exists and its gates ran.

## Quality gates (block any "done")

- Backend: `pytest` green; coverage `engine/` ≥ 90 %, backend overall ≥ 80 %; `ruff` clean; `manage.py check`
  clean; no missing migrations; the engine stays pure Python (no Django import).
- Frontend: `npm ci`, `lint`, `typecheck`, `check:tokens` (tokens only, no hex outside `tokens.css`), `build`.
- Infra: exactly one published port (Caddy); images api ≤ 350 MB, web ≤ 250 MB; Django stateless; every new env
  var in `.env.example`.
- `tech/tests.md` §C (safety, 5 items) re-verified after any related change; §D (RTL, Persian digits, Jalali,
  contrast, 360 px, keyboard) checked for every UI change.
- Docker gates: `bash scripts/docker-gates.sh` (exit 0 green / 1 failed / 2 no-Docker = MISSING) and the
  equivalent GitHub Actions run.

## Prohibitions

- No merges to `main` without the owner's explicit "merge"; no second published port; no secrets in the repo.
- No business logic in frontend components; no LLM-side scoring; no invented user-facing copy or persona data.
- No new dependency without the owner's approval and a licence note.
- No "passed" for a gate that was not actually run — write MISSING.

---

## History — the retired three-agent model (kept for the record, no longer in force)

The M0/M1 build ran with a senior plus two workers (worker-a backend lane, worker-b frontend lane), coordinated
through `STATUS.md` orders, one branch and one report per task, with the owner (and an AI supervisor role) merging
to `main`. Evidence of that period lives in `reports/worker-a/` and `reports/worker-b/`, and in `STATUS.md` orders
before 2026-09-26. Two lessons from that period are kept as rules:

- **Branch exclusivity** is established by live remote state (`git ls-remote`, `gh pr list`) at start time, never by
  absence of contrary mentions (former D-S11).
- A merge that happens before its review gets a **post-merge verdict** — requested changes become follow-up tasks,
  never reverts, unless a §C safety regression is found (former D-S8).
