# backend/ — Django API contract (backend/engine lane, solo senior)

Build here per `tech/tasks.md` (T-001 first). Must satisfy `../docker/Dockerfile.backend`
contract: `requirements.txt` (pinned, prod-only), `manage.py`, `config/wsgi.py`,
`GET /api/health/` (no auth, `{"ok": true}`).

## Required layout

```
manage.py  requirements.txt  requirements-dev.txt  pytest.ini
config/settings.py  config/urls.py  config/wsgi.py   # all settings from env, no secrets
apps/accounts/   # AnonymousIdentity, OTP code, Google OAuth, user link/migrate
apps/chat/       # conversations, messages
apps/screening/  # assessments (PHQ-9/GAD-7/PHQ-4)
apps/safety/     # risk events, crisis payload
apps/directory/  # therapists (seed via seed_therapists command)
apps/summaries/  # summaries, shares, consents
engine/          # PURE python — NO django imports (dialogue, autonomy, prompts,
                 # scoring, risk, summary, redact, providers). Reused by Telegram later.
tests/           # pytest: test_engine_* (≥90% cov) + test_api_* (overall backend ≥80%)
```

## Container contract (T-004)

- `.dockerignore` lives **here** (context is `./backend`). It keeps the caches out but
  keeps `tests/`, `pytest.ini` and `ruff.toml`, because the image has a `test` stage.
- `docker/Dockerfile.backend` ends with `FROM final AS test` (dev tooling only). The
  production layer is byte-identical; `docker-compose.test.yml` builds `haleman-api-test`
  and publishes nothing. Gates run inside it: `make test-backend` →
  `scripts/backend-gate.sh` (ruff, pytest, coverage ≥ 80 %, engine ≥ 90 % once `engine/`
  has modules).
- With `DJANGO_DEBUG=0` a `change-me…` secret or DB password stops the boot
  (`config/settings.py`, T-004 amendment c); `make env` generates real random values.

## Rules

- DRF for `/api/*`; opaque tokens (hashed in DB, httpOnly cookies), revocable.
- OTP: 6-digit hashed, 10-min expiry, ≤5/hour per email. Google OAuth via authlib.
- Scoring server-side only, deterministic. All LLM calls server-side via `engine/providers/`,
  PII redacted pre-call, every call logged (`token_usage`).
- Stateless: no local sessions/files that break `--scale api=N`. Timezone UTC, fa/Jalali
  formatting happens in API serializers or frontend — never naive datetimes.
