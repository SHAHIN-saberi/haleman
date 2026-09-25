# STATUS — Haleman build coordination (append-only, newest at bottom of each section)

> Roles: supervisors (owner+AI) · senior · worker-a (backend lane) · worker-b (frontend lane).
> Protocol: `tech/team.md`. Tasks: `tech/tasks.md`. Tests: `tech/tests.md`.

## Milestone

- [2026-09-25] M0+M1 starting. Goal: compose boots with one port; Django+Next skeleton;
  W-01/W-02 + device token + consent API. Pack: tech-pack v2 (Django + Docker + 3-agent team).
- [2026-09-25] SENIOR: M0 verified → **NOT green**. The skeleton can't boot until app code exists (F1) + 4 infra
  defects (F2–F4, F7). Full text: `reports/senior/M0-review-1.md`. M0 exit now closes at the end of T-004 (D-S1, Q-02).

## Task board

| Task | Worker | Branch | Status | Report |
|---|---|---|---|---|
| T-000 M0 infra blockers (F2/F3/F4/F7) + fresh-clone gate | worker-a | `w-a/T-000-m0-boot-check` | ✅ pending-review (Arena session branch `arena/01a0da44-haleman`) | reports/worker-a/T-000.md |
| T-001 Django project + health + device model | worker-a | `w-a/T-001-django-skeleton` | ⬜ todo (after T-000 pushed) | reports/worker-a/T-001.md |
| T-002 Next.js shell + RTL + theme + fonts + W-01 | worker-b | `w-b/T-002-next-shell` | ⬜ todo (start now) | reports/worker-b/T-002.md |
| T-003A consent API + log + server gate | worker-a | `w-a/T-003A-consent-api` | ⏸ blocked on T-001 merge | reports/worker-a/T-003A.md |
| T-003B W-02 screen + /chat placeholder | worker-b | `w-b/T-003B-consent-screen` | ⏸ blocked on T-002 merge | reports/worker-b/T-003B.md |
| T-004 compose integration + make check + M1 acceptance | worker-a (B on call) | `w-a/T-004-compose-integration` | ⏸ blocked on T-001..T-003B merge | reports/worker-a/T-004.md |

(Further milestones: senior extends the board from `tech/tasks.md` when assigning.)

## Orders (senior → workers)

- [2026-09-25] SUPERVISORS → SENIOR: pack v2 is locked. Read `AGENTS.md` + `tech/team.md`,
  verify M0 skeleton yourself, then post the first orders (T-000..T-004 split across A/B).
- [2026-09-25] SENIOR → ALL: round-1 orders. Full text + binding API contract (§1):
  `reports/senior/M1-orders-1.md`. Read it fully before branching. Waves:
  **T-000 → T-001 ∥ T-002 → T-003A ∥ T-003B → T-004.**

  | Task | Worker | Branch | Start condition |
  |---|---|---|---|
  | T-000 infra blockers F2/F3/F4/F7 + fresh-clone gate transcript | worker-a | `w-a/T-000-m0-boot-check` | now |
  | T-001 Django skeleton, `/api/health/`, device token `hid`, `/api/me/` | worker-a | `w-a/T-001-django-skeleton` | once T-000 is pushed + reported (pre-authorised, branch from `main`) |
  | T-002 Next shell, fa/RTL, Vazirmatn, tokens, ThemeToggle, api client, W-01 | worker-b | `w-b/T-002-next-shell` | now |
  | T-003A `Consent` model, `POST /api/consent/`, `/api/me/` consent, `/api/chat/` 403 gate | worker-a | `w-a/T-003A-consent-api` | after T-001 is merged |
  | T-003B W-02 `/consent`, `/terms` stub, `/chat` placeholder (server-gated) | worker-b | `w-b/T-003B-consent-screen` | after T-002 is merged |
  | T-004 test stage, `make check` wiring, fresh-clone boot, `scripts/m1-acceptance.sh` | worker-a (B on call) | `w-a/T-004-compose-integration` | after T-001..T-003B are merged |

- [2026-09-25] SENIOR → ALL: file ownership in M1: only T-000/T-004 touch `Makefile`, `docker-compose*.yml`,
  `docker/*`, `Caddyfile`. Nobody edits `tech/`, `product/`, `design/`, `src/`. In STATUS.md, edit only your own
  board row + append. First report from each worker must include `docker version` + `docker compose version`.

## Message board

- [2026-09-25] SUPERVISORS: welcome, team. Step by step, tests always green, one port,
  small images. Senior: you own the plan's daily truth here.
- [2026-09-25] SENIOR: hello team. I review by checking out your pushed branch in a detached worktree and re-running
  pytest (real Postgres 16), ruff, `npm ci/lint/typecheck/build`, screenshots in both themes, and the ports check myself.
  My sandbox has no Docker engine (B-01), so paste **verbatim** transcripts of `docker compose build`, `make up`,
  `make size`, `make verify-ports`. Summaries like "all green" will be sent back.

## Decisions

- [2026-09-25] Stack locked: Next.js + Django/DRF + Postgres 16 + Caddy, single published
  port, image budgets backend ≤350MB / frontend ≤250MB. (TD-01..TD-16)
- [2026-09-25] SENIOR D-S1 (provisional, escalated Q-02): T-000 re-scoped to infra fixes. The M0 boot/healthy/size proof
  moves to T-004 acceptance, because the Dockerfiles can't build without T-001/T-002 app code.
- [2026-09-25] SENIOR D-S2: T-003 split into T-003A (api, worker-a) + T-003B (screen, worker-b), sharing the contract in
  `reports/senior/M1-orders-1.md` §1. T-004 has a single owner (worker-a) to avoid Makefile conflicts; worker-b is on call.
- [2026-09-25] SENIOR D-S3 (provisional, escalated Q-06): `frontend/` + `backend/` are canonical; `src/` is not used.
- [2026-09-25] SENIOR D-S4: the `Consent` model lives in `apps/summaries` (per `backend/README.md`) with `kind` in
  {informed, share}, append-only, FK `SET_NULL` so audit rows survive a later wipe (final policy at T-022).
- [2026-09-25] SENIOR D-S5: pre-approved deps list in `M1-orders-1.md` §0 (psycopg LGPL pending Q-04). No
  `next/font/google`, no third-party runtime origins.
- [2026-09-25] SENIOR D-S6: API conventions: trailing slash on every `/api/*` path, JSON-only, no CORS, cookie `hid`
  HttpOnly + SameSite=Lax + `Secure` from `COOKIE_SECURE`, sha256-only storage, health never issues tokens. The consent
  gate is enforced server-side (`/api/chat/` 403), never by client state.

## Blockers

- (none)
- [2026-09-25] WORKER-A T-000: Docker is unavailable in this worker sandbox (`docker: command not found`), so compose config, fresh-clone boot, image-size, pull, and health evidence require supervisor spot-run.
- [2026-09-25] SENIOR B-01: senior sandbox has no Docker engine (all container registries blocked). Docker gates in
  senior reviews rest on worker transcripts + a supervisor spot-run until Q-01 is answered. → SUPERVISORS
- [2026-09-25] SENIOR B-02: these orders live on the senior session branch `arena/01a0da37-haleman` (docs only:
  STATUS.md, reports/senior/, tech/questions.md). Workers branch from `main`, so **supervisors, please merge it
  before the workers start.** → SUPERVISORS
- [2026-09-25] SENIOR: B-02 → opened PR #1 (`arena/01a0da37-haleman` → `main`, docs only):
  https://github.com/SHAHIN-saberi/haleman/pull/1 — awaiting supervisor merge. → SUPERVISORS
