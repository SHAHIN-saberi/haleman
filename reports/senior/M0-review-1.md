# Senior review — M0 round 1 (skeleton verification, pre-orders)

- Date: 2026-09-25
- Branches reviewed: `main` @ `c1381a6` (tech-pack v2). No worker branches exist yet (`git fetch` → only `origin/main`).
- Reviewer: senior. Senior work branch (session-fixed): `arena/01a0da37-haleman`.

## Verdicts

| Branch | Verdict | Notes + exact fixes |
|---|---|---|
| `main` @ c1381a6 (M0 skeleton) | **request-changes: M0 NOT green** | The skeleton **cannot boot on any host yet**. The Dockerfile contracts need app code that doesn't exist (F1). Fixes are split across T-000/T-001/T-002/T-004 in `reports/senior/M1-orders-1.md`. |

## Consolidated test evidence (I ran these myself)

Senior sandbox: Debian 12, sudo, Python 3.11, Node 22. Network allows PyPI, npm and GitHub. It **blocks every
container registry** (Docker Hub, GHCR, Quay, ECR, mirror.gcr.io), download.docker.com, apt mirrors, the Playwright CDN
and GitHub release assets. So I can't install a Docker engine or pull base images here. See blocker B-01 / Q-01.

| Gate | Command | Real result |
|---|---|---|
| boot | `make up` | `make: docker: No such file or directory` → Error 127 (no engine in the senior sandbox) |
| ports | `make verify-ports` | `FAIL: published ports != 1` (docker missing → fails closed ✔, correct behaviour) |
| ports (static equivalent) | PyYAML parse of `docker-compose.yml`, count `ports:` | **proxy=1, web=0, api=0, db=0 → TOTAL 1 ✔** (web/api/db use `expose` only) |
| size | `make size` | printed `docker: not found` twice and **exited 0** ✘. The target can never fail (F4) |
| build contracts | file-existence check vs `docker/Dockerfile.*` | `backend/requirements.txt`, `manage.py`, `config/wsgi.py`, `frontend/package.json`, `frontend/public/`, `next.config.*` → **all MISSING** (F1) |
| wireframes | headless Chromium (npm-bundled), full-page light + dark screenshots | W-01..W-10 render in both themes ✔ |
| tokens | hex-set diff: `palette.md` vs wireframe `<style>` vs `theme-preview.html` | **identical sets** (14 light + 14 dark). `--shadow` exists only in wireframe/theme-preview: light `0 10px 30px rgba(43,53,66,.08)`, dark `0 10px 30px rgba(0,0,0,.35)` ✔ |
| review tooling | `pgserver` (PyPI) → `SHOW server_version` | **16.2** ✔. Senior can run pytest against real Postgres 16 without Docker |

- coverage (`engine/` / backend): n/a (no code yet).
- safety section C: n/a (no screens/prompts/engine yet). Baseline: **nothing implemented, nothing violated**.

## Findings

| # | Sev | Finding | Owner / fix |
|---|---|---|---|
| F1 | BLOCKER | The Dockerfiles `COPY requirements.txt` / `package.json` / `public/`, but `backend/` and `frontend/` only hold READMEs. The implementation plan's M0 "placeholder apps" don't exist, so `make up` fails at build on **every** host. | T-001 (A) + T-002 (B) create the real apps. The full boot proof moves to T-004 (decision D-S1, escalated Q-02) |
| F2 | BLOCKER (fresh clone) | `env_file: .env` plus `${POSTGRES_PASSWORD:?}` make `docker compose config/up` fail on a fresh clone, and so `make verify-ports` fails too. The Makefile never creates `.env`. | T-000: `make env` target (copy `.env.example`→`.env` only if missing), made a prerequisite of `up`/`verify-ports`/`check` |
| F3 | HIGH | The `api` service gets no `POSTGRES_HOST`/`POSTGRES_PORT`, so Django can't locate `db`. | T-000: add `POSTGRES_HOST=db`, `POSTGRES_PORT=5432` to `.env.example` + compose `api.environment` defaults |
| F4 | HIGH | `make size` only displays sizes and exits 0 even with no Docker. It is not a gate. | T-000: enforcing target. Fail if docker is missing, an image is missing, `haleman-api` > 350 MB or `haleman-web` > 250 MB (decimal MB, like `docker images`) |
| F5 | HIGH | `make check` runs pytest inside the **prod** api image, which (correctly) has no dev deps, so pytest isn't found. It also has no lint/typecheck/compose-build, which `team.md` requires. The frontend build runs on the host without `npm ci`. | T-004: `test` stage in `Dockerfile.backend` + `docker-compose.test.yml` (image `haleman-api-test`, **zero ports**), ruff + coverage gate, `npm ci && lint && typecheck && build`, `docker compose build` |
| F6 | MED | `pip wheel --no-deps` means `requirements.txt` must pin **every transitive dep**. Otherwise the build passes (only `import django` is checked) and runtime import fails. | T-001: full lock; prove it with `pip install --no-deps -r requirements.txt && pip check` in a clean venv |
| F7 | MED | There's no `.dockerignore`, so build contexts would ship `node_modules/.next/.venv/.env` (size + secret-leak risk). | T-000: `backend/.dockerignore`, `frontend/.dockerignore` |
| F8 | MED | `node:20-alpine`: Node 20 reached end-of-life on 2026-04-30. | Escalated Q-05 (TD-13 area). No change until supervisors answer |
| F9 | LOW | Healthchecks hit `/api/health/` every 30 s per replica. If health issued device tokens, the table would fill with junk rows. | T-001: health must never create rows or set cookies (tested) |
| F10 | LOW | Migrate-on-boot + `--scale api=3` means concurrent migrations can race. | Follow-up T-025 (M4); not M1 |
| F11 | DOC | `technical-decisions.md`: TD-05 (`lib/engine/scoring.ts`), TD-06 (Auth.js) and TD-09 (`@react-pdf/renderer`) are Next-only leftovers that contradict the Django architecture. TD-13..15 sit below a duplicated "Standing rules" heading. "MIT/Apache-licensed" conflicts with Django (BSD) and psycopg (LGPL). | Escalated Q-03, Q-04. Senior does not edit TDs |
| F12 | DOC | `src/README.md` (and root README) say the app is built in `src/`. That contradicts `AGENTS.md`, `frontend/README.md` and `backend/README.md`. | Provisional decision D-S3: `frontend/` + `backend/` are canonical, `src/` untouched. Escalated Q-06 |

What's already right: exactly one published port; all 4 services have healthchecks; multi-stage builds; non-root
users (uid 10001); db/api/web are internal-only; Caddy has `admin off` + `auto_https off` (TLS terminates upstream);
the design token sources agree with each other.

## Integration notes

- Wave plan and merge order are in `reports/senior/M1-orders-1.md` §0. Short version: **T-000 → T-001 ∥ T-002 → T-003A ∥ T-003B → T-004**.
- Only T-000 and T-004 may touch `Makefile`, `docker-compose*.yml`, `docker/*` or `Caddyfile`. T-001/T-002/T-003x must not
  touch them (conflict avoidance). Anything a worker needs there goes to the message board.
- `STATUS.md` is edited by everyone. To keep squash merges trivial, workers touch **only their own board row** + append
  to Message board / Blockers.

## Next orders

| Task | Worker | Branch to create | Starts |
|---|---|---|---|
| T-000 infra blockers F2/F3/F4/F7 + fresh-clone gate transcript | worker-a | `w-a/T-000-m0-boot-check` | now |
| T-001 Django project + health + device token | worker-a | `w-a/T-001-django-skeleton` | right after T-000 is pushed + reported (pre-authorised) |
| T-002 Next.js shell + RTL + theme + fonts + W-01 | worker-b | `w-b/T-002-next-shell` | now |
| T-003A consent API + log + server gate | worker-a | `w-a/T-003A-consent-api` | after T-001 is merged |
| T-003B W-02 screen + /chat placeholder | worker-b | `w-b/T-003B-consent-screen` | after T-002 is merged |
| T-004 compose integration + `make check` + M1 acceptance | worker-a (worker-b on call) | `w-a/T-004-compose-integration` | after T-001..T-003B are merged |

## Risks / escalations to supervisors

- **B-01 / Q-01:** the senior sandbox can't run Docker. Until that's fixed, the Docker gates (`make up`, `make size`,
  compose build, runtime `verify-ports`) in my reviews rest on worker transcripts **plus one supervisor spot-run per
  milestone**. I label them "docker-gate: evidence-by-transcript". Everything else I re-run myself.
- **B-02:** this report + orders live on `arena/01a0da37-haleman`. Workers branch from `main`, so please merge this
  branch (docs-only: STATUS.md, reports/senior/, tech/questions.md) before the workers start.
- Q-02..Q-08 are in `tech/questions.md`.
