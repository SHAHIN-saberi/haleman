# M1 final gate — Foundations (step 0 → T-004)

- Author: solo senior · Date: 2026-09-26 · Branch: `arena/01a0dcf9-haleman`, head **`77ee464`**
- Milestone exit criteria: `tech/tests.md` §B (M1) + §C/§D, and the acceptance of `reports/senior/M1-orders-1.md` §T-004.
- Owner-facing verdict requested at the bottom. **Everything marked MISSING is missing because this sandbox has no
  Docker engine (B-01) — it is never counted as a pass.**

## 1. Verdict

**M1 is code-complete and every gate producible in this environment is green.** The M1 exit criterion of
`tech/tests.md` §B — *a fresh visitor gets an anonymous token, is asked for informed consent, accepts, and lands on the
chat placeholder (US-01/04/05)* — was reproduced end to end in a real browser on this commit (20/20 checks, §4 below),
and the milestone's own acceptance script passes 23/23 against a live stack.

What is **not** proven here: the Docker half of the pipeline (`make up`, image builds, healthchecks, image sizes, the
in-image test run, and the same acceptance through Caddy). Those need a Docker engine; §7 lists them and gives the
owner one command to close them.

## 2. What M1 delivered

| Task | Commit | Deliverable |
|---|---|---|
| 0.1–0.4 | `95e4346`, `7f91666`, `0c5aa0a` + `121b02f`, `7e60631` | housekeeping, the Docker gate script + CI wrapper + palette v1.1 + solo-senior mode |
| T-003A | `42f4bf9` | `Consent` (append-only, no PII) · `POST /api/consent/` · `GET /api/me/` consent block · server gate on `/api/chat/` · N-1 error envelope · N-2 “no identity for methods a view does not implement” |
| T-003B | `33fe7ff` | W-02 `/consent` (byte-exact copy) · `/chat` placeholder (server-gated) · `/terms` stub · Persian 404 · always-visible 115 line · F-2 focus-ring fix |
| T-004 | `77ee464` | compose test stage + `node:22-alpine` · `make check` as the single gate · `scripts/m1-acceptance.sh` · random `.env` + placeholder guard · real `.dockerignore`s |

Backend: Django 5.2.17 + DRF + gunicorn + psycopg3 on PostgreSQL 16, stateless, JSON-only `/api/*` with trailing
slashes. Frontend: Next 16.3.6 (standalone), React 19, Tailwind 4, tokens v1.1, self-hosted Vazirmatn, `fa`/RTL.

## 3. Gates (§5) — fresh run on `77ee464`

| Gate | Command | Result |
|---|---|---|
| backend tests | `pytest` (PostgreSQL 16.2) | **51 passed** in 0.60 s ✔ |
| coverage | `pytest --cov=. --cov-fail-under=80` | **96.43 %** (617 statements, 22 missed) ✔ |
| lint | `ruff check .` | `All checks passed!` ✔ |
| Django | `manage.py check` | `System check identified no issues (0 silenced).` ✔ |
| migrations | `makemigrations --check --dry-run` | `No changes detected` ✔ |
| engine purity | `pytest tests/test_engine_purity.py` | 3 passed — `engine/` still imports no Django ✔ |
| frontend lint/types | `npm run lint`, `npm run typecheck` | clean ✔ |
| tokens | `npm run check:tokens` | `OK: tokens 1:1 with palette.md, 21 files scanned, 0 stray hexes` ✔ |
| frontend build | `npm run build` | `✓ Compiled successfully`; routes `/` `/_not-found` `/chat` `/consent` `/terms` prerendered ✔ |
| one published port | YAML parse of both compose files | `docker-compose.yml`: **1** (owner `proxy`); `docker-compose.test.yml`: **0** ✔ |
| stateless | settings (code lines only) + `test_settings.py` | no session app, no session/CSRF middleware ✔ |
| image budgets | `make size` | **MISSING** — no Docker here (B-01) |
| env hygiene | `make env` / placeholder guard | `.env` 0600 with random secrets; `change-me*` refuses to boot at `DEBUG=0` ✔ |

## 4. M1 acceptance criterion, reproduced in a browser (20/20)

Harness: real Django (gunicorn :8123) + real PostgreSQL 16.2 + the **production standalone** Next build (:3000) behind
a one-port proxy (:3300) — the same topology `docker-compose.yml` + `Caddyfile` produce. Raw output:
`reports/senior/m1-final-probe.json`; screenshots `reports/senior/img/senior-m1final-*.png`.

```
M1-1  fresh visitor → /api/me/ in the page: {"anonymous":true,"is_new":true,"consent":{"informed":false,"version":"v1"}}
      cookie hid: HttpOnly=true SameSite=Lax Path=/          ← issued by the app on first paint
M1-1  no consent on record yet                              ✔
M1-2  «شروع گفتوگو» → /consent; W-02 copy byte-exact vs the wireframe (5 strings, ZWNJ intact) ✔
M1-3  direct GET /chat (fresh device) → redirected to /consent; the gate answered
      403 {"code":"consent_required"} — the SERVER decides, not the client ✔
M1-4  press «فهمیدم، شروع کن» → 201 → /chat shows the W-03 opening line with an inert input;
      /api/me/ now {"is_new":false,"consent":{"informed":true,"version":"v1"}} ✔

§C2  the 115 line is on all 5 routes (/, /consent, /chat, /terms, /404)                ✔
§C3  no screen claims diagnosis/treatment/therapist identity; the “not a diagnosis” disclaimer is served on
     /consent and /terms                                                                ✔
§C5  zero third-party origins at runtime; no key/provider pattern in the shipped client bundle ✔
§D   light #F5F2EA / dark #151B24 render the v1.1 tokens; clay 115 button both themes; Persian digits ۱۱۵;
     360 px has no horizontal overflow; Tab → toggle → primary → terms → 115, every stop shows an instant
     2 px `--primary` ring                                                             ✔
§5   Django stateless (no session/CSRF middleware, no sessions app)                     ✔
```

Milestone acceptance script (`scripts/m1-acceptance.sh`, the order's §4 checks) against the same live stack:
**`M1 ACCEPTANCE: PASS (23 checks)`**, and pointed at a wrong port it **fails** (`FAIL (3 passed, 20 failed)`, exit 1) —
the gate is not vacuous.

## 5. §C safety-critical re-verification (after all M1 changes)

| # | Item | Status in M1 |
|---|---|---|
| C1 | Risk screener runs in EVERY screening | **n/a** — no screening exists yet (M2/T-009/T-010 build it; the engine purity test and the `/api/chat/` contract are the hooks). |
| C2 | Crisis path reachable from every route within 1 message; 115 dials | **Partial by design:** the always-visible `tel:115` line («تماس با اورژانس ۱۱۵», byte-exact) is on every route (verified). The full W-10 overlay — empathy card, flow pause, ghost «حالا امنم، ادامه میدهم» — is **T-015**, not in M1 scope. |
| C3 | No screen/prompt/message claims diagnosis, treatment or therapist identity | **Pass** — audited all five served routes: the only occurrences of «تشخیص/درمان/درمانگر» are the disclaimers («اینجا با یک ابزار هوشمند حرف میزنی، نه درمانگر. این گفتوگو تشخیص و درمان نیست.»). |
| C4 | Every shared summary was previewed + consent logged | **n/a** — no summary/share endpoint exists (M4/T-021/T-022). The consent log that will carry it is already append-only with no PII. |
| C5 | PII redacted before every LLM call; keys server-side only | **Pass for M1 scope** — no LLM call exists yet; verified zero third-party origins at runtime and no key/API pattern in the shipped bundle. The redaction layer itself is T-007. |

## 6. Risks / carry-overs (all pre-existing or newly explicit)

| Item | Owner action |
|---|---|
| **B-01 Docker evidence missing** (this file §7) | run the one-line spot-run below, or activate the CI gate (B-05). |
| **Q-08 legal text** for `/terms` and the consent wording | you + the lawyer; the stub says «متن کامل پس از تأیید حقوقی منتشر میشود.» |
| **B-05 CI activation** (the App that pushes this branch has no `workflows` scope) | `bash scripts/activate-ci-gate.sh` + its printed push commands (your push, not mine). |
| **T-007 LLM provider + key** | you must choose the free provider/key — never guessed. |
| **D7 deploy target** (T-025) | your decision before M4's production compose. |
| migrate-on-boot race under `--scale api=N` | recorded as T-025 work, not fixed now (order §T-004-3). |
| `/terms` is a dead end in M1 (no in-page control) | deliberate; the real page arrives with Q-08. |

## 7. MISSING evidence (not a pass) + how to close it in one command

Missing here: `make build` / `make up` (4/4 healthy) / `make size` (api ≤ 350 MB, web ≤ 250 MB) /
in-image `make test-backend` / `make acceptance` through Caddy / `docker compose … config`.

```bash
git checkout arena/01a0dcf9-haleman     # head 77ee464
make up && make check && make verify-ports && make size && make acceptance && docker compose ps
```

Green signals to expect, in order: `make check` → `All checks passed!` · `51 passed` ·
`Required test coverage of 80% reached. Total coverage: 96.43%` · `OK: tokens 1:1 …` · `OK: make check green`;
`make size` → `haleman-api: … MB` + `haleman-web: … MB` + `OK: image sizes within budgets`;
`make acceptance` → `M1 ACCEPTANCE: PASS (23 checks)`; `docker compose ps` → proxy/web/api/db **healthy**.
Any exit code `2` means “no Docker” = MISSING, not a pass. `bash scripts/docker-gates.sh` performs the same set and
writes raw evidence to `reports/docker-gates/<sha>/` (gitignored).

## 8. Owner verdict requested

Pick one (the third keeps M2 moving while you test):

- **الف) M1 approved — start M2/T-005.** I begin the chat UI (W-03) on this branch; the Docker spot-run stays with you
  whenever convenient.
- **ب) M1 approved, but hold M2** until you have run the Docker spot-run and seen the four green signals.
- **ج) Run the spot-run first, then decide.** I wait; no code moves until your verdict.

Whatever you choose, T-007 (LLM adapter) will come with a provider/key question — that one cannot proceed without you.
