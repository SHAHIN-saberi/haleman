# Senior review — M1 round 2 (T-001)

- Date: 2026-09-26
- Reviewed: PR #6 — `arena/01a0dc32-haleman` @ `9c7a73a` ("T-001 (worker-a): Django 5 skeleton + /api/health/ +
  AnonymousIdentity + hid device flow + engine purity guard"), base `main` @ `90aa3a3` (post PR #5).
  Delta: 28 files, +954/−1. Existing senior verdicts checked first: `reports/senior/` held M0-review-1,
  M1-orders-1, M1-review-1 — **no prior T-001 verdict existed**; PR #6 had 0 reviews/comments. Nothing duplicated.
- Branch name: `arena/01a0dc32-haleman` is the **D-S7 alias of the ordered `w-a/T-001-django-skeleton`** — named in the
  report and the board row, one task on the branch. Accepted.
- Method: PR head fetched (`refs/pull/6/head` = `9c7a73a`) and inspected in a **detached worktree**
  (`git worktree add --detach`); my primary checkout stayed on the senior session branch `arena/01a0dc46-haleman`.
  Every command below was run by me, today, against that exact head.

## Verdicts

| Branch / PR | Verdict (approve / request-changes) | Notes + exact fixes |
|---|---|---|
| T-001 · worker-a · `arena/01a0dc32-haleman` @ `9c7a73a` (PR #6) | **approve — ready for supervisor merge** | Scope exact: `backend/**` + `.env.example` append (pre-approved) + own STATUS rows + report; **no** Makefile/compose/Dockerfile/Caddyfile/frontend/tech/product/design/src changes (verified with a path filter over the full delta). Order items 1–7 all implemented. Every runnable gate re-run by me and green (below). Two LOW findings fold into T-003A (N-1 required there, N-2 optional); no rework of merged T-001 code. Docker evidence remains missing (G-1, environment) and is explicitly **not** treated as passing. |

Worker-reported results were **not** adopted: every number in `reports/worker-a/T-001.md` that could be reproduced here
was re-produced by my own runs (19 passed · 95.25 % · ruff clean · `pip check` clean · wire flags · sha256-only storage).
All matched.

## Consolidated test evidence (I ran these myself)

Environment: senior sandbox, Debian 12, Python **3.11.2**, Node 22.22.3, **no Docker engine** (`docker version` →
`command not found`; B-01 family). Real Postgres: **PostgreSQL 16.2** booted in-sandbox from the `pgserver` PyPI wheel —
a dev-harness tool installed outside the repo (like my M0 run); `pgserver` appears in **no** project file
(`requirements*.txt` untouched — verified). All commands ran against the PR head in the detached worktree.

### Gates

| Check | Command | My result |
|---|---|---|
| migrate on plain DB | `manage.py migrate --noinput` (env per `.env.example`) | `Applying accounts.0001_initial... OK` ✔ |
| migration drift (my addition) | `manage.py makemigrations --check --dry-run` | `No changes detected` ✔ |
| pytest, real Postgres 16.2 | `pytest --cov=. --cov-fail-under=80 --cov-report=term-missing` | **19 passed** in 0.57 s ✔ |
| backend coverage (gate ≥ 80 %) | same run | **95.25 %** ✔ (`device.py`/`authentication.py`/`views.py` 100 %; only `manage.py`/`wsgi.py` at 0 % — exercised by the live gunicorn run below) |
| `engine/` coverage (≥ 90 %) | n/a | engine is an empty package by order; gate activates when `engine/` has code |
| lint | `ruff check .` (config `ruff.toml`, migrations exempted from style) | `All checks passed!` ✔ |
| **F6 pin proof** | clean venv → `pip install --no-deps -r requirements.txt && pip check` | installs exactly the 9 declared pins; **`No broken requirements found.`**; `import django, rest_framework, gunicorn, psycopg` OK (5.2.17 / 3.16.1 / 3.2.13) ✔ |
| F6 resolver cross-check (my addition) | separate venv, resolver install of the 5 root pins, `pip list` | resolver independently chose **exactly** the pinned transitives: `asgiref==3.12.1 sqlparse==0.6.0 typing_extensions==4.16.0 packaging==26.3` ✔ — requirements.txt is a true lock |
| static ports check | PyYAML parse of `docker-compose.yml` | proxy 1, web 0, api 0, db 0 → **TOTAL 1** ✔ (compose untouched by this delta) |
| **Docker gates** | `docker compose build api`, api image ≤ 350 MB, `make size`, in-image pytest | **NOT RUNNABLE — `docker: command not found`** (no engine in any team sandbox, B-01/Q-01). **Missing evidence, not passing evidence.** Carried into T-004's Docker-capable acceptance per worker-a's explicit request |

### Device-cookie / health behavior — live wire smoke (pinned gunicorn 23.0.0 + curl)

| Check | My result |
|---|---|
| `GET /api/health/` | `200 {"ok":true}`, `Content-Type: application/json`, **zero Set-Cookie headers** ✔ |
| health DB side-effects | `anonymous_identities` count 0 after health calls (incl. with a garbage cookie presented) ✔ |
| `POST /api/health/` | 405, **no Set-Cookie, no row** ✔ (F9 holds on every path) |
| `GET /api/me/` first visit | `200 {"anonymous":true,"is_new":true}`; `Set-Cookie: hid=<43 url-safe chars>; HttpOnly; Max-Age=31536000; Path=/; SameSite=Lax` — **exactly §1/D-S6**, no `Secure` (COOKIE_SECURE=0) ✔ |
| revisit with `hid` | `200 {"anonymous":true,"is_new":false}`; **no new Set-Cookie**; same row; `last_seen_at` advanced over `created_at` (DB timestamps) ✔ |
| garbage cookie (`garbage-not-a-token`) | 200 (never 401), `is_new:true`, fresh 43-char cookie, new row ✔ |
| well-formed unknown cookie (`b`×43) | 200, `is_new:true`, new row ✔ (the regex path is tested, not just the garbage path) |
| `COOKIE_SECURE=1` (second gunicorn instance) | `Set-Cookie: … SameSite=Lax; Secure` — flag follows the env ✔ |
| **sha256-only storage** (my DB cross-proof via raw `psycopg`) | `sha256(cookie)` hex **present in `anonymous_identities.token_hash`**, raw cookie value **absent**, all rows `length(token_hash)==64` ✔ |
| missing/empty `DJANGO_SECRET_KEY` | subprocess tests (part of the 19): process exits non-zero with `ImproperlyConfigured` naming `DJANGO_SECRET_KEY` ✔ |
| settings posture | DEBUG default off; Postgres-only engine (no sqlite fallback, TD-03); `fa`/UTC/`USE_TZ`; `SECURE_PROXY_SSL_HEADER` set; no `contrib.admin`/`contrib.sessions`, no Session/Csrf/Auth middleware ✔ |
| engine purity | guard tests pass (incl. the mutation test proving the guard has teeth); my `grep -rn "django\|rest_framework" backend/engine/` → no matches ✔ |

### What the 19 tests lock (order §Tests mapping verified in code)

First visit → 1 row + exact cookie flags · revisit → same row, count 1, `last_seen_at` advanced, `is_new=false` ·
garbage **and** well-formed-unknown → new row, never 401 · `token_hash ≠ cookie` and `== sha256(cookie)` ·
health → 0 rows + no Set-Cookie + 405 · SECRET_KEY missing/empty → `ImproperlyConfigured` (subprocess-isolated) ·
defaults + stateless middleware posture · `Secure` follows `COOKIE_SECURE` · engine purity (+ mutation) ·
`/api/me/` returns exactly `{"anonymous","is_new"}` (locks T-001 scope until T-003A adds `consent`).

## Findings

| # | Sev | Finding | Disposition |
|---|---|---|---|
| N-1 | LOW | 405 error bodies use DRF's default `{"detail":"متد POST مجاز نیست."}` — no `code` key, so they don't match the binding §1 error envelope `{"code","detail"}`. (The fa wording itself is fine — §1 allows "fa or en".) The envelope becomes contractual at `/api/consent/` (unknown kind/version → 400 `invalid_consent`; GET → 405). | **Required in T-003A**: normalize DRF error bodies to the envelope (custom exception handler for 400/405). Not a T-001 blocker — no M1 client path POSTs to health/me. |
| N-2 | LOW | DRF authenticates **before** the method check, so `POST`/`PUT`/`DELETE` on `/api/me/` (which 405) still resolve-or-issue an identity + row (I proved this on the wire: a 405 carried a fresh `Set-Cookie` and created a row). §1 governs only GET, and `/api/health/` is exempt (`authentication_classes=[]`), so this is contract-clean — but it widens the unauthenticated row-creation surface to non-contract methods. | **Optional hardening in T-003A** (same file): issue only on the contract's methods, or accept and document. No T-001 change. |
| N-3 | PROCESS NIT | The worker's two 2026-09-26 message-board entries were **inserted mid-section** between 2026-09-25 entries instead of appended at the bottom ("newest at bottom" convention). Content was purely additive — nothing deleted, no history rewritten — so append-only is intact in substance. | Recorded; senior does **not** reorder (append-only). Future entries: append at the bottom of each section. |
| G-1 | ENVIRONMENT (recorded) | Docker checks (`docker compose build api`, api image ≤ 350 MB, `make size`, in-image pytest) could not run: `docker: command not found` in this sandbox (B-01 family, all team sandboxes). | Missing evidence; carried into T-004's Docker-capable acceptance (worker-a requested the same). Q-01 still open and still gates T-004/M1 exit. |
| G-2 | ENVIRONMENT (note) | My verification ran on Python 3.11.2; the backend image targets `python:3.12-slim`. Both are inside Django 5.2 LTS's supported range and the F6 pin proof is version-independent, but the 3.12 in-image proof lands with T-004. | No action. |

Positives worth recording: `UNAUTHENTICATED_USER: None` correctly avoids DRF building an `AnonymousUser` without
`contrib.auth` (a classic boot-failure here); health is a plain view with `authentication_classes([])` so F9 holds on
every method; the purity guard ships with a mutation test; `makemigrations --check` shows no drift; dependency pins are
a true lock (resolver cross-check); the report honestly separates produced evidence from missing evidence.

## Process correction (recorded append-only; no history rewritten)

- Worker A claimed `arena/01a0dc32-haleman` was **exclusive** on the grounds that repository history did not mention
  another user. **That reasoning is invalid**: absence of a contrary mention does not establish exclusivity. Exclusivity
  is established only by live remote state (`git ls-remote origin`, `gh pr list`) at start time.
- Worker B independently reported the same pinned branch and **stopped without changes** — the correct behavior under
  the protocol. Worker A's PR #6 uses the branch; it stands as the D-S7 alias of `w-a/T-001-django-skeleton`.
- Worker B proceeds in a **distinct new session** (its harness will pin a different branch). No existing history is
  rewritten; this correction is recorded here, in `STATUS.md` (decision **D-S11** + message board), append-only.
- Board guidance updated: T-002F/T-003B remain worker-b's tasks, now expected from the new session.

## Integration notes

- **Merge order:** supervisors merge **PR #6** (T-001) — verdict above is the gate they were waiting for. My docs PR
  (this review + STATUS.md updates) touches only `reports/senior/` + `STATUS.md`; if the T-001 board row conflicts with
  the one in PR #6, take the senior-docs version (it carries the alias + this verdict).
- After merge: **T-003A** starts (worker-a, `w-a/T-003A-consent-api`, from updated `main`) carrying N-1 (+ optionally
  N-2). `/api/me/` already speaks the §1 shape; `DeviceAuthentication`/`DeviceCookieMixin` are reusable as-is — no
  rework of merged T-001 files is needed beyond the ordered additions.
- Worker-b queue unchanged (T-002F → T-003B), from the new session.
- T-004 remains blocked on the T-001/T-002F/T-003A/T-003B merges **and Q-01** (Docker-capable runner); it now also
  carries T-001's image evidence (G-1).

## Next orders

| Task | Worker | Branch | Start |
|---|---|---|---|
| T-003A consent API (+ N-1 envelope normalization; N-2 optional) — order in `M1-orders-1.md` unchanged otherwise | worker-a | `w-a/T-003A-consent-api` (or its D-S7 session alias, named in report + board) | **after PR #6 is merged by a supervisor** |
| T-002F shell follow-ups (round-2 order unchanged) | worker-b | new session, own pinned branch (alias of `w-b/T-002F-shell-followups`, D-S7) | **now** (from the new session) |
| T-003B W-02 + `/terms` + `/chat` placeholder (unchanged) | worker-b | alias of `w-b/T-003B-consent-screen` | once T-002F is pushed + reported (pre-authorised) |
| T-004 compose integration + amendments a–d (+ T-001 image evidence G-1) | worker-a (B on call) | `w-a/T-004-compose-integration` | after T-001, T-002F, T-003A, T-003B are merged **and Q-01 answered** |

## Risks / escalations to supervisors

- **Q-01 (re-raise):** still no Docker-capable runner on the team, so T-001's image evidence and all of T-004's
  acceptance remain unproducible. Until it is answered, `docker compose build api` + api image size are **missing
  evidence**, not passing evidence.
- Merge PR #6 only after this verdict (done — it is above); per protocol, supervisors merge, senior never merges.
- T-001 board row / STATUS.md conflict between PR #6 and the docs PR: trivial, take the union (both are additive).
- Q-04 (psycopg LGPL wording), Q-09 (contrast) and the rest of Q-02..Q-09 remain open as before; none block this merge.
