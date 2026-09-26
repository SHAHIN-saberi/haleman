# Build Tasks — the queue; the solo senior executes one task per step, with a plan gate and a report per task

Status lives in `STATUS.md` board (`⬜ → 🔄 → ✅ pending-review → merged`).
Done = acceptance holds on the compose stack + gates in `tech/team.md` green.

## M0 — Skeleton

- **T-000** M0 boot check | acc: `make up` → proxy+web+api+db healthy; `make verify-ports`
  + `make size` green; report confirms one port + budgets (any lane)

## M1 — Foundations

- **T-001** Django project: settings-from-env, DRF, `/api/health`, device-token model +
  cookie issue/resume, pytest harness | acc: first visit creates anon row; revisit resumes;
  engine cov n/a yet (US-01, US-04) [lane: A]
- **T-002** Next.js shell: `fa`/RTL, Vazirmatn copied from brand-kit, tokens.css 1:1 from
  palette, `<ThemeToggle/>`, api client | acc: W-01 matches wireframe both themes; hexes
  exact (US-01) [lane: B]
- **T-003** W-02 consent + `POST /api/consent` + consent log | acc: chat unreachable
  without consent; log row per accept (US-05) [A: api, B: screen — senior splits or pairs]
- **T-004** Compose integration: Dockerfiles build app code, migrate-on-boot, `make check`
  (pytest + next build) | acc: fresh clone → `make up` → `make check` all green [A+B]

## M2 — Chat + screening engine

- **T-005** Chat UI: bubbles, chips, progress, input, stop/resume | acc: W-03 both themes (B)
- **T-006** `engine/dialogue` state machine + `POST /api/chat` wiring (echo → live) | acc:
  greeting → picture → test? → result reachable via API (A)
- **T-007** `engine/providers` (LLM adapter, one interface) + redact + token logging +
  per-assessment cost cap | acc: no key client-side; every call in `token_usage`; cap
  enforced (A)
- **T-008** Bounded-autonomy prompts v1 (gentle/fa) + prompt safety self-audit | acc:
  friendly tone; never therapist-role; fixed guards hold (A, senior re-audits)
- **T-009** `engine/scoring` (PHQ-9/GAD-7/PHQ-4 + levels) + pytest vectors ≥90% cov | acc:
  100% boundary vectors incl. edges (US-06) (A)
- **T-010** Risk screener (2Q) + background detector wiring | acc: any positive → crisis
  event same turn (US-07) (A)
- **T-011** M2 integration: 3 scripted dialogues (mild/moderate/test-refused) end-to-end
  green via compose | acc: scores exact, persisted (A+B)

## M3 — Result + safety

- **T-012** W-04 result + no-test wrap-up branch | acc: level + plain words +
  "not a diagnosis" + next steps; matches wireframe (US-08) (B + A api)
- **T-013** W-05 calming flow, skippable | acc: completable + skippable, returns to result (B)
- **T-014** `engine/risk` detector (recall-first) + pytest trigger list | acc: all
  `tests.md` signals trigger (US-09) (A)
- **T-015** W-10 overlay on every route + 115 button + flow pause | acc: <1 message
  signal→overlay, logged-out OK (US-10) (B + A api)
- **T-016** Full safety audit: prompts + result copy + engine paths vs tests.md §C | acc:
  signed checklist in senior report; zero diagnosis/therapist claims (senior-led, A+B fix)

## M4 — Identity + router + summary + launch-prep

- **T-017** Google One-Tap login + device-data migration | acc: anon history visible
  post-login (US-02) (A + B screen W-06)
- **T-018** Email OTP (6-digit hashed, 10-min, ≤5/hr) + free SMTP | acc: login by code;
  abuse limits hold (US-03) (A)
- **T-019** Therapist seed (≥10 manually-verified) + `seed_therapists` + router API (A)
- **T-020** W-07 router + filters (city/budget/gender/mode) | acc: filters exact, license
  badges shown (US-11, US-12) (B)
- **T-021** Summary builder + preview API + PDF (RTL-tested) | acc: preview == shared ==
  PDF bytes-content (US-13) (A)
- **T-022** W-08 share flow + consent log + "delete my data" | acc: zero sends without
  consent row; delete wipes owner data (US-14) (A+B)
- **T-023** W-09 trend + week-1 reminder + tokenized one-click unsub | acc: chart from
  real data; unsub works logged-out (US-15, US-16) (A+B)
- **T-024** Playwright smoke (5 paths) + cost-cap report + size/ports re-verify | acc: all
  green; p95/assessment under cap; budgets hold (B + A)
- **T-025** Production compose hardening + runbook + M4 final report | acc: public URL
  serves full journey; fresh-clone setup <15 min; senior files final report (senior-led)

Lanes: A = backend/engine, B = frontend — **code placement only** (the worker lanes were retired on 2026-09-26;
see `tech/team.md` §Solo-senior mode). Status lives in the `STATUS.md` board.
