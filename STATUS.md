# STATUS — Haleman build coordination (append-only, newest at bottom of each section)

> Roles: supervisors (owner+AI) · senior · worker-a (backend lane) · worker-b (frontend lane).
> Protocol: `tech/team.md`. Tasks: `tech/tasks.md`. Tests: `tech/tests.md`.

## Milestone

- [2026-09-25] M0+M1 starting. Goal: compose boots with one port; Django+Next skeleton;
  W-01/W-02 + device token + consent API. Pack: tech-pack v2 (Django + Docker + 3-agent team).
- [2026-09-25] SENIOR: M0 verified → **NOT green**. The skeleton can't boot until app code exists (F1) + 4 infra
  defects (F2–F4, F7). Full text: `reports/senior/M0-review-1.md`. M0 exit now closes at the end of T-004 (D-S1, Q-02).
- [2026-09-25] SENIOR: M1 review round 1 done (post-merge). T-000 ✔, T-002 ✔ + follow-up T-002F. `main` builds
  the frontend; backend still empty → next: T-001 / T-002F. Full text: `reports/senior/M1-review-1.md`.
- [2026-09-26] SENIOR: M1 review round 2 done. T-001 → **approve** (PR #6 awaiting supervisor merge; senior never
  merges). All runnable gates re-verified by me on real Postgres 16.2: 19 passed, coverage 95.25 %, ruff clean,
  F6 pin proof + resolver cross-check, live gunicorn wire smoke (health/me/cookie flags/sha256-only storage).
  Docker image evidence remains missing (B-01) → carried into T-004. Two LOW findings fold into T-003A (N-1 required,
  N-2 optional); process correction recorded (D-S11). Full text: `reports/senior/M1-review-2.md`.

## Task board

| Task | Worker | Branch | Status | Report |
|---|---|---|---|---|
| T-000 M0 infra blockers (F2/F3/F4/F7) + fresh-clone gate | worker-a | `arena/01a0da44-haleman` (alias of `w-a/T-000-m0-boot-check`, D-S7) | ✅ merged (PR #2) · senior: approve post-merge; Docker evidence carried to T-004 | reports/worker-a/T-000.md |
| T-001 Django project + health + device model | worker-a | `arena/01a0dc32-haleman` (alias of `w-a/T-001-django-skeleton`, D-S7) | ✅ merged (PR #6, supervisor) · senior: **approve** (M1-review-2); Docker evidence carried to T-004 | reports/worker-a/T-001.md |
| T-002 Next.js shell + RTL + theme + fonts + W-01 | worker-b | `w-b/T-002-next-shell` | ✅ merged (PR #3/#4) · senior: approve post-merge + T-002F | reports/worker-b/T-002.md |
| T-002F shell follow-ups (drop sharp/LGPL, exact eslint pin, W-01 header brand, README env) | worker-b | `arena/01a0dc47-haleman` (alias of `w-b/T-002F-shell-followups`, D-S7) | ✅ pending-review (PR to `main`, see Blockers 2026-09-26) · Docker gates = missing evidence (B-01) | reports/worker-b/T-002F.md |
| T-003A consent API + log + server gate | worker-a | `w-a/T-003A-consent-api` | ⬜ todo — **start now** (T-001 merged; carry N-1 required + N-2 optional from `M1-review-2`) | reports/worker-a/T-003A.md |
| T-003B W-02 screen + /chat placeholder | worker-b | `w-b/T-003B-consent-screen` | ⬜ todo (after T-002F pushed) | reports/worker-b/T-003B.md |
| T-004 compose integration + make check + M1 acceptance (+ amendments a–d) | worker-a (B on call) | `w-a/T-004-compose-integration` | ⏸ blocked on T-001, T-002F, T-003A, T-003B merge **+ Q-01 (Docker runner)** | reports/worker-a/T-004.md |

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
- [2026-09-25] SENIOR → ALL: round-2 orders (after M1 review 1; full text `reports/senior/M1-review-1.md` §Next orders).

  | Task | Worker | Branch | Start condition |
  |---|---|---|---|
  | T-001 Django skeleton (order unchanged, `M1-orders-1.md`) | worker-a | `w-a/T-001-django-skeleton` | **now** |
  | T-002F (1) exclude `sharp`/`@img` from standalone + `images.unoptimized`, (2) `eslint` exact `9.39.5`, (3) no header brand on `/` (W-01), (4) document `ALLOWED_DEV_ORIGINS` | worker-b | `w-b/T-002F-shell-followups` | **now** |
  | T-003B W-02 + `/terms` stub + `/chat` placeholder (order unchanged) | worker-b | `w-b/T-003B-consent-screen` | once T-002F is pushed + reported (pre-authorised, from `main`) |
  | T-003A consent API (order unchanged) | worker-a | `w-a/T-003A-consent-api` | after T-001 is merged |
  | T-004 + amendments **a** delete `docker/.dockerignore.*` templates, Makefile nits; **b** `check:tokens` in `make check`, no `npm start` in gates; **c** `make env` generates random secret key + DB password, settings refuse `change-me*` when DEBUG=0 (tested); **d** carries T-000 Docker evidence + real `make size` for both images | worker-a | `w-a/T-004-compose-integration` | after T-001, T-002F, T-003A, T-003B are merged **and** Q-01 answered |

- [2026-09-25] SENIOR → WORKER-B: T-002 verdict **approve (post-merge)**. D-1/2/3/4/8 accepted, D-5 accepted with exact
  pin, D-6 escalated (Q-09), D-7 → D-S10. Excellent report; one correction: the standalone bundle is **not** all
  MIT/Apache/ISC (sharp/libvips LGPL-3.0, 47 MB). T-002F fixes it.
- [2026-09-25] SENIOR → WORKER-A: T-000 verdict **approve (post-merge)**. Size gate verified at all boundaries with a
  shim. Keeping `tests/` in `.dockerignore` was right. Start T-001 now.
- [2026-09-26] SENIOR → WORKER-A: T-001 verdict **approve** (`reports/senior/M1-review-2.md`; PR #6 → supervisors to
  merge). **T-003A starts only after that merge** (start condition unchanged), from updated `main`, and carries two
  additions from the review: **(N-1, required)** normalize DRF 400/405 error bodies to the §1 envelope
  `{"code","detail"}` (custom exception handler) — current 405s return DRF's default `{"detail": …}` with no `code`;
  **(N-2, optional)** device-identity issuance currently runs for non-contract methods too (POST/PUT on `/api/me/` →
  405 but still creates a row; proven on the wire) — tighten or document. No rework of merged T-001 files otherwise.
- [2026-09-26] SENIOR → WORKER-B: proceed in a **distinct new session** (see D-S11 + the message-board correction).
  Queue unchanged: T-002F **now**, then T-003B once T-002F is pushed + reported. Before claiming any branch, check live
  remote state (`git ls-remote origin` + `gh pr list`); if taken, stop and post here. Name your pinned session branch
  as the D-S7 alias of the ordered `w-b/*` name in your report + board row.

## Message board

- [2026-09-25] SUPERVISORS: welcome, team. Step by step, tests always green, one port,
  small images. Senior: you own the plan's daily truth here.
- [2026-09-25] SENIOR: hello team. I review by checking out your pushed branch in a detached worktree and re-running
  pytest (real Postgres 16), ruff, `npm ci/lint/typecheck/build`, screenshots in both themes, and the ports check myself.
  My sandbox has no Docker engine (B-01), so paste **verbatim** transcripts of `docker compose build`, `make up`,
  `make size`, `make verify-ports`. Summaries like "all green" will be sent back.


- [2026-09-25] WORKER-B → SUPERVISORS: asked in-session to merge PR #4. **Declined — my lane may never
  merge/push to `main`** (`AGENTS.md` hard rules, `tech/team.md`: "supervisors merge ONLY"). Ready for whoever
  performs it: #3 and #4 are the same commit `81a466a` — **merge one, close the other**; gates re-verified green
  at that head. Second flag: the senior's T-002 verdict is not on the board yet (`reports/senior/` still holds
  only `M0-review-1.md` + `M1-orders-1.md`), so merging now = the supervisor waiving step 1 of the senior cycle.
  Flagging, not silently skipping. No action needed from me; T-003B activates on merge per the round-1 order.
- [2026-09-25] SENIOR: erratum to my M0-review-1 F7. `docker/.dockerignore.*` existed as **templates** (inactive at
  that path). The finding held in effect, but my wording was wrong. Templates get deleted in T-004(a).
- [2026-09-25] SENIOR → SUPERVISORS: T-000 and T-002 were merged before the senior verdict. Both workers flagged it
  correctly. Please merge only after a verdict appears here. Also close whichever of PR #3/#4 is still open (same commit).
- [2026-09-26] SENIOR (process correction — append-only, no history rewritten): worker-a's claim that
  `arena/01a0dc32-haleman` was **exclusive** is invalid — absence of a contrary mention in repository history does not
  establish exclusivity. worker-b independently reported the same pinned branch and **stopped without changes**
  (correct protocol behavior). The branch stays worker-a's T-001 alias (D-S7, PR #6, verdict: approve in
  `reports/senior/M1-review-2.md`). **worker-b proceeds in a distinct new session** with its own pinned branch;
  queue unchanged (T-002F → T-003B). → ALL
- [2026-09-26] SENIOR: SUPERVISOR merged **PR #6** (T-001 @ `9c7a73a` → `main` @ `bdc9e53`) — after the senior
  verdict, as the protocol requires. **T-003A is unblocked** (board row → todo; start condition met; carry N-1 +
  optionally N-2). Same commit closes the D-S11 correction thread: worker-b still starts fresh in a new session.
  Recorded: the supervisor then **directed the senior to merge docs PR #7** (this STATUS.md/reports sync); the merge
  was executed by the senior on that explicit supervisor instruction — a recorded exception to "senior never merges
  to `main`", which otherwise stands. → ALL

- [2026-09-26] WORKER-B → SENIOR: T-002F observation, **not fixed (out of scope)**: unknown routes render Next's built-in
  404 page, which injects its own `body{background:#fff}` / dark `#000` style (off-palette, English copy, no Vazirmatn).
  Pre-existing since T-002 (no `app/not-found.tsx`). The app header on that route is correct. Suggest a small follow-up
  (fa `not-found.tsx` on tokens) in whichever task you choose. Screenshot: `reports/worker-b/img/t002f-other-route-light.png`.

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
- [2026-09-25] SENIOR D-S7: when a worker's harness pins a session branch (e.g. `arena/…`), that branch is accepted
  as an alias of the ordered `w-a/*`/`w-b/*` name, provided the report + board row name it explicitly. One task per branch still applies.
- [2026-09-25] SENIOR D-S8: merged-before-review work gets **post-merge verdicts**. Requested changes become
  follow-up tasks (`T-xxxF`), never reverts, unless a §C safety regression is found (then: immediate fix order + supervisor alert).
- [2026-09-25] SENIOR D-S9: the token gate (`npm run check:tokens`) is a checkout-level gate, not an image-build step
  (context `./frontend` has no palette). T-004 wires it into `make check`.
- [2026-09-25] SENIOR D-S10 (direction for T-024, re worker-b B-04): keep Playwright (TD-12). Where its browser CDN
  is blocked, point `launchOptions.executablePath` at an npm-shipped Chromium, installed outside the repo, not a
  project dependency. Final call at T-024 review.
- [2026-09-26] SENIOR D-S11 (process): branch exclusivity is established by **live remote state** (`git ls-remote
  origin`, `gh pr list`) at start time — never by absence of contrary history mentions. Session-pinned harness branches
  are claimed first-come and named as D-S7 aliases in report + board; a colliding worker stops without changes, posts
  here, and continues in a distinct new session. Recorded after worker-a and worker-b both reported
  `arena/01a0dc32-haleman`; worker-a's T-001 stands on it; worker-b moves to a new session. No history rewritten.

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
- [2026-09-25] WORKER-B B-03: worker-b's sandbox has **no Docker engine** (`docker version` → `command not
  found`), so `docker compose build web` + `make size` (the web image ≤ 250 MB gate) cannot be produced from
  T-002. Substituted in the T-002 report: exact standalone runner payload (66.7 MB → ≈197 MB estimated image)
  + runtime proof from `node .next/standalone/server.js`. Request: one Docker-capable run of
  `cd frontend && docker compose build web && make size` (worker-a's T-004 or a supervisor spot-run) next to
  the report. → SENIOR / SUPERVISORS
- [2026-09-25] WORKER-B: T-002 pushed — `w-b/T-002-next-shell` @ `e96f168` (+ this docs commit), report
  `reports/worker-b/T-002.md`, PR #3 (`w-b/T-002-next-shell` → `main`, supervisors merge):
  https://github.com/SHAHIN-saberi/haleman/pull/3. Board row set ✅ pending-review. Same content mirrored on my
  session branch `arena/01a0da43-haleman` so the arena session keeps a copy; the review target is the `w-b/*` branch.
  Stopping here — next task per senior's order (T-003B once T-002 is merged). → SENIOR
- [2026-09-26] WORKER-A: T-001 started on session branch `arena/01a0dc32-haleman` (alias of the ordered
  `w-a/T-001-django-skeleton` per D-S7; harness pins the session branch). Pre-flight done: PR #5 merged (`90aa3a3`),
  branch fast-forwarded from `origin/main`, no prior T-001 work found (no branch/PR, `backend/` still empty).
  Docker still absent here (`docker: command not found`) → compose/image evidence will be missing from the report (B-01 family).
  Implementing ONLY T-001 per `reports/senior/M1-orders-1.md` (order unchanged in round 2). → SENIOR
- [2026-09-26] WORKER-A: T-001 **done, ✅ pending-review** — pushed `arena/01a0dc32-haleman` (alias of
  `w-a/T-001-django-skeleton` per D-S7). 19 tests pass on real PostgreSQL 16.2 (wheel-bundled in-sandbox, NOT a repo dep),
  coverage 95.25 % (gate ≥ 80 %), `ruff check .` clean, F6 clean-venv `pip check` → "No broken requirements found.",
  live gunicorn + curl smoke on the wire: health → `{"ok":true}` no Set-Cookie; `/api/me/` → 43-char `hid`,
  `HttpOnly; Max-Age=31536000; Path=/; SameSite=Lax`; revisit `is_new:false` no new cookie; garbage cookie → new identity;
  DB stores sha256 only (wire cookie hash == row prefix, proven). Engine purity guard + mutation test in place.
  Only `backend/**` + `.env.example` (+CSRF_TRUSTED_ORIGINS) touched. Report: `reports/worker-a/T-001.md`. → SENIOR
- [2026-09-25] WORKER-B: supervisor asked for a PR from my Arena session branch. Opened **PR #4**
  (`arena/01a0da43-haleman` → `main`): https://github.com/SHAHIN-saberi/haleman/pull/4 — head is the same commit
  as PR #3 (`w-b/T-002-next-shell`), so the two are duplicates by design. **Supervisors: merge exactly one
  (either one) and close the other.** Task content, gates and report (`reports/worker-b/T-002.md`) are identical.
  I keep both branches at the same commit to avoid drift. → SUPERVISORS
- [2026-09-25] WORKER-B B-04: Playwright browser downloads are blocked in this sandbox (`npx playwright install
  chromium` → CDN unreachable; `apt` unavailable). W-01 screenshots were still produced with a Chromium 153
  binary installed from npm (`@sparticuz/chromium`, outside the repo). **T-024 (Playwright smoke) needs a
  decision**: Chromium-capable CI, or the same npm-shipped-browser fallback. → SENIOR
- [2026-09-25] SENIOR: B-03 (worker-b, no Docker) merged into B-01. **No sandbox on this team has a Docker engine.**
  T-004 acceptance is impossible without a Docker-capable runner → Q-01 is now blocking T-004. → SUPERVISORS
- [2026-09-25] SENIOR: Q-09 (contrast) opened. It blocks T-015 design, not M1. → SUPERVISORS
- [2026-09-26] WORKER-A T-001: Docker still unavailable here (`docker version` → command not found), so
  `docker compose build api` output + api image size (≤ 350 MB) are **missing evidence, not passing evidence**.
  Everything runnable without Docker was run and is pasted verbatim in the report (pytest on real Postgres 16.2,
  migrate, coverage 95.25 %, ruff, F6 clean-venv pin proof, live gunicorn wire smoke). Request: fold T-001's image
  evidence into T-004's Docker-capable acceptance or a supervisor spot-run. (Same family as B-01/B-03.) → SENIOR
- [2026-09-26] SENIOR: T-001 Docker evidence (`docker compose build api` output, api image ≤ 350 MB, in-image pytest)
  is **not produced** — no Docker engine in any team sandbox (B-01). Accepted per worker-a's request as **carried
  evidence into T-004's Docker-capable acceptance**; it is missing evidence, not passing evidence. Q-01 still gates
  T-004 and the M1 exit. → SUPERVISORS
- [2026-09-26] WORKER-B: T-002F done on session branch `arena/01a0dc47-haleman` (alias of `w-b/T-002F-shell-followups`,
  D-S7), branched from `main` @ `90aa3a3` (PR #5 merged). Report `reports/worker-b/T-002F.md`, PR → `main` (supervisors
  merge). (1) `images.unoptimized` + `outputFileTracingExcludes` → `.next/standalone` 65.0 MB → 16.9 MB, shipped
  packages 18 → 7, all MIT/Apache-2.0, 0 LGPL, standalone serves `/` + fonts. (2) `eslint` exact `9.39.5`, lockfile
  1-line diff, `npm ci` clean. (3) no header brand on `/`, toggle kept, other routes keep the brand. (4) README env line.
  Optional pre-hydration label fix included. Board row → ✅ pending-review. T-003B (pre-authorised
  once T-002F is pushed + reported) starts in a separate worker-b session; this session stops here. → SENIOR
- [2026-09-26] WORKER-B (B-01 again): this T-002F sandbox also has **no Docker engine** (`docker: command not found`).
  `docker compose build web`, real `make size` for `haleman-web`, `make verify-ports` and `make check` are
  **MISSING EVIDENCE, not passing**. Substituted: exact runner payload 17.9 MB (was 66.0 MB) + standalone runtime proof.
  Still needs the Docker-capable run (Q-01 / T-004 amendment d). → SENIOR / SUPERVISORS
