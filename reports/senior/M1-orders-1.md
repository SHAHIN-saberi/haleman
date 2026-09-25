# Senior orders — M0+M1 round 1 (full text; STATUS.md holds the summary)

- Date: 2026-09-25 · Author: senior · Basis: `main` @ c1381a6 + `reports/senior/M0-review-1.md`
- Applies to everyone: `tech/team.md` worker cycle, one task = one branch = one report,
  `make check`-level evidence pasted **verbatim** (no paraphrased "all green").

## 0. Waves, dependencies, file ownership

```
Wave 1  A: T-000 ──► A: T-001            B: T-002
Wave 2  A: T-003A (after T-001 merged)   B: T-003B (after T-002 merged)
Wave 3  A: T-004 (after T-001, T-002, T-003A, T-003B merged; B on call)
```

| Path | Who may change it in M1 |
|---|---|
| `Makefile`, `docker-compose*.yml`, `docker/*`, `Caddyfile`, `.env.example` | T-000, T-004 (worker-a) only. Exception: T-001/T-003A may **append** new env vars to `.env.example` |
| `backend/**` | worker-a |
| `frontend/**` | worker-b |
| `STATUS.md` | everyone: own board row + append-only sections |
| `tech/*.md`, `product/*`, `design/*`, `src/` | nobody (escalate) |

**Docker availability:** each worker states in their **first** report whether their harness runs Docker
(`docker version` + `docker compose version` output). If it doesn't, post it under Blockers **immediately**.

**Pre-approved dependencies** (anything else needs senior approval first, logged in your report):

- Backend prod: `Django` 5.2.x LTS (BSD-3), `djangorestframework` (BSD-3), `gunicorn` (MIT), `psycopg` 3.2.x +
  `psycopg-binary` same version (LGPL-3.0, used as an unmodified library; license wording escalated in Q-04) + their
  exact transitive pins (`asgiref`, `sqlparse`, `typing_extensions`, …).
- Backend dev: `pytest`, `pytest-django`, `pytest-cov`, `ruff`.
- Frontend: `next`, `react`, `react-dom`, `typescript`, `@types/node`, `@types/react`, `@types/react-dom`,
  `tailwindcss` (+ its official PostCSS plugin/`postcss`), `eslint`, `eslint-config-next`. **Exact** versions + committed
  `package-lock.json` (the Dockerfile uses `npm ci`).
- Forbidden: `next/font/google` or any runtime request to a third-party origin (privacy + Iran reachability).

## 1. API conventions (binding for A and B, decision D-S6)

- Every endpoint lives under `/api/` and **ends with a trailing slash** (`/api/me/`, not `/api/me`). The frontend client
  always sends the slash. That avoids Django's APPEND_SLASH 301 on POST.
- JSON only (`Content-Type: application/json`). No CORS headers at all: same-origin through Caddy only.
- Device cookie `hid`: opaque `secrets.token_urlsafe(32)`, **HttpOnly, SameSite=Lax, Path=/, Max-Age=31536000**.
  `Secure` comes from env `COOKIE_SECURE` (`.env.example`: `COOKIE_SECURE=0` with a comment "set 1 behind HTTPS").
  The DB stores only `sha256(token)` hex. The raw token is never logged, returned in a body or stored.
- Lax cookie + JSON-only body is the M1 CSRF posture (a cross-site form can't send JSON without preflight). Documented in
  the T-003A report.
- Error body shape: `{"code": "<snake_case>", "detail": "<fa or en short text>"}`.
- Endpoints in M1:

| Method + path | Auth | Issues `hid` if missing/invalid | Response |
|---|---|---|---|
| `GET /api/health/` | none | **never** (no row, no Set-Cookie) | `200 {"ok": true}` |
| `GET /api/me/` | device | yes | `200 {"anonymous": true, "is_new": bool, "consent": {"informed": bool, "version": "v1"\|null}}` (`consent` added in T-003A; T-001 returns the first two keys) |
| `POST /api/consent/` | device | yes | body `{"kind":"informed","version":"v1"}` → `201 {"kind","version","accepted_at"}` · unknown kind/version → `400 {"code":"invalid_consent"}` · GET → 405 |
| `GET /api/chat/` | device + consent | yes | consented → `200 {"placeholder": true}` · not consented → `403 {"code":"consent_required"}` |

---

## T-000 — M0 infra blockers + fresh-clone gate (worker-a) · branch `w-a/T-000-m0-boot-check`

Scope (infra only, **no app code, no placeholder apps**; decision D-S1):

1. **F2** `make env`: `test -f .env || cp .env.example .env` (never overwrite). Make it a prerequisite of `up`, `build`,
   `verify-ports`, `check`, `test-backend`, `migrate`, `seed`, `shell`.
2. **F3** add `POSTGRES_HOST=db` and `POSTGRES_PORT=5432` to `.env.example`, and as defaults in compose
   `api.environment` (`POSTGRES_HOST: ${POSTGRES_HOST:-db}` …).
3. **F4** make `make size` enforcing: `docker image inspect -f '{{.Size}}' haleman-api haleman-web`. Fail (exit 1) if
   docker is missing, if an image is missing, if api > 350 000 000 B or web > 250 000 000 B. Print both sizes in MB.
4. **F7** `backend/.dockerignore` (`.venv`, `__pycache__`, `*.pyc`, `.pytest_cache`, `.coverage`, `htmlcov`, `.env*`,
   `.git`) and `frontend/.dockerignore` (`node_modules`, `.next`, `out`, `coverage`, `.env*`, `.git`,
   `playwright-report`, `test-results`). Do **not** exclude `tests/` (T-004 runs pytest in the image).
5. `make verify-ports` unchanged in logic. It must pass on a fresh clone thanks to (1).

Acceptance + evidence to paste:

- Fresh clone (`git clone … /tmp/fresh && cd /tmp/fresh && git checkout w-a/T-000-m0-boot-check`):
  `make verify-ports` → `OK: exactly one published port`; `docker compose config -q` → exit 0.
- `make size` with no images built → **non-zero exit** + clear message (proves it fails closed).
- `make up` → expected to fail at the **build** step because app code is missing (F1). Paste the first failing lines,
  so we know it fails there and nowhere earlier.
- `docker pull python:3.12-slim node:20-alpine postgres:16-alpine caddy:2-alpine` + `docker images` sizes (budget
  baseline).
- No change to published ports; `git diff --stat` touches only the files above.

## T-001 — Django project + health + device token (worker-a) · branch `w-a/T-001-django-skeleton`

Pre-authorised to start as soon as T-000 is pushed + reported. Branch from `main` (not from T-000). Don't touch
Makefile/compose/Dockerfiles.

1. Layout exactly per `backend/README.md`: `manage.py`, `requirements.txt`, `requirements-dev.txt` (`-r requirements.txt`
   + dev deps), `pytest.ini`, `config/{settings,urls,wsgi}.py`, `apps/accounts/`, `engine/__init__.py` (empty package),
   `tests/`. Create **only** the apps M1 needs (`accounts`; `summaries` comes in T-003A).
2. **F6** `requirements.txt` fully pinned incl. transitive deps. Evidence: in a clean venv,
   `pip install --no-deps -r requirements.txt && pip check` → `No broken requirements found.`
3. Settings 100% from env. `DJANGO_SECRET_KEY` is required: raise `ImproperlyConfigured` if missing/empty. `DJANGO_DEBUG`
   (default 0), `DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` (append to `.env.example`), `POSTGRES_DB/USER/PASSWORD/
   HOST/PORT` (**Postgres only**, no sqlite fallback; TD-03 local = prod), `COOKIE_SECURE`. `USE_TZ=True`,
   `TIME_ZONE="UTC"`, `LANGUAGE_CODE="fa"`. `SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")`.
   No `django.contrib.admin`, no sessions middleware for the device flow (stateless).
4. `GET /api/health/` → `200 {"ok": true}`, no auth, **no DB row, no Set-Cookie** (F9).
5. `AnonymousIdentity` (apps/accounts): `id` UUID pk, `token_hash` char(64) unique+indexed, `created_at`, `last_seen_at`.
   No user FK yet (T-017). One service function (e.g. `accounts.device.resolve_or_issue(request) -> (identity, new_token|None)`)
   plus a DRF authentication class, reused by every device-auth endpoint. Unknown/garbage cookie → new identity + new
   cookie (never 401).
6. `GET /api/me/` per §1 (without the `consent` key).
7. Guard test `tests/test_engine_purity.py`: walks `engine/**/*.py` and fails on any `import django` / `from django` /
   `rest_framework`. It's cheap now and protects the Telegram reuse later.

Tests (pytest-django, real Postgres): first visit → 1 row + cookie flags exactly as §1; revisit with cookie → same row,
count 1, `last_seen_at` advanced, `is_new=false`; garbage cookie → new row; DB `token_hash` ≠ cookie value and
== sha256(cookie); health → 0 rows + no Set-Cookie; missing SECRET_KEY → ImproperlyConfigured; `ruff check` clean.
Backend coverage ≥ 80 % (`pytest --cov=. --cov-fail-under=80`). Report `docker compose build api` output + api image size (≤ 350 MB).

## T-002 — Next.js shell + RTL + theme + fonts + W-01 (worker-b) · branch `w-b/T-002-next-shell`

Branch from `main`. Don't touch Makefile/compose/Dockerfiles. If `Dockerfile.frontend` needs a change, ask on the message board.

1. `frontend/`: Next.js App Router (current stable major, exact pins), TypeScript `strict: true`, Tailwind,
   `next.config` with `output: 'standalone'`. `package.json` scripts: `dev`, `build`, `start`, `lint` (eslint CLI),
   `typecheck` (`tsc --noEmit`). T-004 wires these into `make check`, so they must exist and pass now.
2. `<html lang="fa" dir="rtl">`. Fonts: copy `design/brand-kit/fonts/Vazirmatn-{Regular,Medium,Bold}.ttf` →
   `public/fonts/` **byte-identical** (paste `sha256sum` of both sides). `@font-face` (or `next/font/local`),
   `font-display: swap`. `public/` must exist (the Dockerfile copies it).
3. `styles/tokens.css`: `:root[data-theme="light"]` / `:root[data-theme="dark"]` with exactly these vars:
   `--bg --card --surface2 --text --soft --border --primary --primary-h --on-primary --primary-bg --sage --sage-bg --clay
   --clay-bg --shadow`. Hexes 1:1 from `design/brand-kit/palette.md`. `--shadow` light `0 10px 30px rgba(43,53,66,.08)`,
   dark `0 10px 30px rgba(0,0,0,.35)` (from wireframe). Evidence: a script diffing the tokens.css hex set vs palette.md → identical.
   Tailwind theme maps to the vars (`bg-card`, `text-soft`, `bg-primary` …). No hard-coded hex anywhere else.
4. Theme: default = system (`prefers-color-scheme`), persisted in `localStorage['haleman-theme']` (`light|dark`).
   Tiny inline pre-hydration script in `<head>` so there's no wrong-theme flash. `<ThemeToggle/>` pill per design-system.
5. `lib/api.ts`: same-origin relative URLs, `credentials: 'include'`, JSON, trailing slash, typed `getMe()`. **Client-side
   calls only** in M1 (the Next server has no route to the public host). `lib/format.ts`: `toFaDigits()` (presentation
   only, not business logic).
6. `/` = W-01: frame max-width 480 px centered, 360 px OK. Copy **exactly** (keep the ZWNJ U+200C in «حال‌من» and
   «گفت‌وگو»): «حال‌من» (display 26 bold), «حالت چطوره؟», «قدم اول، ناشناس و امن», primary pill «شروع گفت‌وگو» → `/consent`
   (route may 404 until T-003B), ghost link «چطور کار می‌کند؟» (non-navigating for now, target open → Q-08). On mount, call
   `getMe()` once (this is what issues the device token). If it fails, W-01 still renders.
7. Root layout mounts an empty `<CrisisLayer/>` placeholder (renders nothing yet) so T-015 slots in without touching every
   page. Whether M1 shows a minimal 115 link is escalated (Q-07). Don't add one on your own.
8. Buttons min-height 44 px, pill radius, keyboard-focusable with a visible focus ring.

Evidence: `npm ci && npm run lint && npm run typecheck && npm run build` output; W-01 screenshots at 390×844 **light and
dark** next to the wireframe W-01 crop (commit small PNGs under `reports/worker-b/img/`); `docker compose build web` output
+ web image size (≤ 250 MB); `grep -rn "fonts.googleapis\|http://\|https://" frontend/app frontend/components frontend/lib`
→ no third-party origins.

## T-003A — consent API + log + server-side gate (worker-a) · branch `w-a/T-003A-consent-api`

Starts after T-001 is merged. Branch from updated `main`.

1. `apps/summaries` with a `Consent` model (placement per `backend/README.md`, decision D-S4): `id`, `identity` FK →
   AnonymousIdentity (`null=True, on_delete=SET_NULL` so audit rows survive a future "delete my data"; final policy is
   T-022), `kind` (choices `informed`, `share`; only `informed` used now), `version` (char), `created_at`. **Append-only**:
   no update/delete code paths. No IP, no user-agent, no free text (minimal data).
2. `CURRENT_CONSENT = {"informed": "v1"}` in one place. `POST /api/consent/` and `GET /api/me/` (+`consent`) per §1.
   Every accept creates a new row, repeats included.
3. DRF permission `HasInformedConsent` (identity has a row with the current version) + `GET /api/chat/` placeholder per §1.
   The **server** is the gate. The frontend only follows it.

Tests: no consent → `me.consent.informed=false`, `/api/chat/` 403 `consent_required`; POST → 201 + 1 row; POST twice →
2 rows; then chat 200; wrong version/kind → 400 + 0 rows; device B can't see device A's consent; GET /api/consent/ → 405;
POST without cookie → issues `hid` and logs against the new identity. Coverage ≥ 80 %, ruff clean, CSRF posture paragraph in report.

## T-003B — W-02 consent screen + /chat placeholder (worker-b) · branch `w-b/T-003B-consent-screen`

Starts after T-002 is merged. Branch from updated `main`. Build against the §1 contract. Until T-003A merges, test with a
mocked `fetch`, never with client-side logic standing in for the server.

1. `/consent` = W-02, copy **exactly**: title «قبل از شروع»; three ✓ cards:
   «اینجا با یک ابزار هوشمند حرف می‌زنی، نه درمانگر. این گفت‌وگو تشخیص و درمان نیست.» ·
   «ناشناسی؛ هیچ‌چیز بدون اجازه‌ات برای کسی ارسال نمی‌شود.» · «در بحران، فوراً راه کمک اضطراری می‌گیری.»;
   primary «فهمیدم، شروع کن»; link «متن کامل قوانین و حریم خصوصی» → `/terms` stub (heading only + visible
   "متن نهایی به‌زودی"; real text blocked on Q-08).
2. Primary button → `POST /api/consent/ {"kind":"informed","version":"v1"}` (constants live in `lib/api.ts`).
   Disabled while pending. On 201 → `router.replace('/chat')`. On error → inline retry message, stay on page.
3. `/chat` placeholder: on mount `GET /api/chat/`. On 403 `consent_required` → `router.replace('/consent')`. On 200 →
   header «حال‌من» + one bot bubble «سلام! امروز روزت چطور گذشت؟» + a **disabled** input. **No** consent flag in
   localStorage/cookies/state as a source of truth. The server decides.
4. Both themes, 360 px, keyboard-reachable primary action.

Evidence: lint/typecheck/build output; screenshots of W-02 light+dark vs wireframe; a short screen recording **or**
step screenshots of: `/chat` without consent → bounced to `/consent` → accept → `/chat` placeholder.

## T-004 — compose integration + `make check` + M1 acceptance (worker-a; worker-b on call) · branch `w-a/T-004-compose-integration`

Starts after T-001, T-002, T-003A, T-003B are merged.

1. **F5** `Dockerfile.backend`: add a `test` stage (`FROM final`, install `requirements-dev.txt` as root, back to `appuser`).
   The `final` stage stays byte-for-byte the prod image. `docker-compose.test.yml` override: `api.build.target: test`,
   `image: haleman-api-test`, **no `ports`**.
2. `make check` = `make env` → `docker compose build` → backend `ruff check .` + `pytest -q --cov=. --cov-fail-under=80`
   (+ `--cov=engine --cov-fail-under=90` once `engine/` has code) inside `haleman-api-test` with `db` up → frontend
   `npm ci && npm run lint && npm run typecheck && npm run build` → `make verify-ports`. Any failure → non-zero exit.
3. Migrate-on-boot stays in the prod CMD. Record the `--scale` migration race as a known M4 item (T-025), don't fix now.
4. `scripts/m1-acceptance.sh` (curl through Caddy on `APP_PORT`, cookie jar): `/` 200 + contains `dir="rtl"`;
   `/api/health/` 200 without Set-Cookie; `/api/me/` sets `hid` (HttpOnly; SameSite=Lax); `/api/chat/` 403; POST consent
   201; `/api/chat/` 200; second `/api/me/` → `is_new=false`. Exit non-zero on any mismatch.

Acceptance = fresh clone → `make up` → `make check` → `make verify-ports` → `make size` → `scripts/m1-acceptance.sh`, all
green, full transcript pasted. Plus `docker compose ps` showing proxy/web/api/db **healthy**. That closes the M0 exit
(T-000's original boot criterion) and the M1 exit.
