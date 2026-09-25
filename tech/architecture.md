# Architecture — Haleman (Next.js + Django + Docker, one port)

## Runtime (docker-compose, exactly ONE published port)

```
Internet ── :${APP_PORT:-80} ──▶ proxy (Caddy 2-alpine)
                                    ├─ /api/* ──▶ api  (Django 5 + DRF + gunicorn, :8000, internal)
                                    │                ├─ db (Postgres 16-alpine, :5432, internal, volume)
                                    │                └─ LLM API (external, server-side only)
                                    └─ /* ──────▶ web (Next.js standalone, :3000, internal)
```

- Compose is the deploy unit: identical locally, on preview, and on production.
- Scale-out: `docker compose up -d --scale api=3` — Caddy load-balances; `api` MUST stay
  stateless (opaque tokens in DB, no local uploads/sessions). Volumes: `pg_data` only
  (+ `caddy_data`). No Redis in MVP (OTP/reminders live in Postgres with expiry).

## Backend (`backend/` — Django 5 + DRF)

- `config/` settings 100% from env; `apps/accounts|chat|screening|safety|directory|summaries/`.
- `engine/` — PURE Python, zero Django imports: `dialogue, autonomy, prompts, scoring,
  risk, summary, redact, providers`. Importable by the future Telegram adapter as-is.
- API surface: `/api/health /api/auth/* /api/chat /api/screen /api/crisis /api/router
  /api/summary /api/me` — DRF, pagination, Jalali-aware serializers.
- Auth: opaque device token (httpOnly cookie `hid` + hashed DB row) → upgrade to account
  via Google OAuth (authlib) or email OTP (6-digit hashed, 10-min, ≤5/hr); migration moves
  anon rows to the user. "Delete my data" wipes owner rows (audit kept).

## Frontend (`frontend/` — Next.js App Router)

- Thin client: renders wireframe screens, zero business logic, all data via same-origin
  `/api/*` (Caddy-routed, cookies included). `output: 'standalone'` for the slim image.
- fa/RTL, Vazirmatn self-hosted, `[data-theme]` tokens, crisis overlay on every route.

## Data model (Postgres — sketch, Django models in apps)

- `anonymous_identities, users, consents, conversations, messages, assessments,
  summaries, shares, therapists, reminders, token_usage` (see brief for fields' purpose).
- Every LLM call logs `token_usage` (input/output tokens, model, usd) — the T6 cost gate.

## Key constraints (repeated because they break builds)

- One published port. Two more = failed task (`make verify-ports`).
- Scoring deterministic + server-side; LLM never computes clinical levels.
- Secrets only via env; PII redacted before any LLM call; share needs preview + consent row.
