# Tests — what "done" means (compose stack is the test bed)

## A. Gates (every task — `make check` + team gates)

- Backend: `pytest -q` green; `engine/` coverage ≥ 90%, backend overall ≥ 80%.
- Frontend: `npm run build` green (lint + typecheck as configured in T-002/T-004).
- `make verify-ports` green (exactly one published port). `make size` within budgets
  (backend ≤ 350MB, frontend ≤ 250MB).
- No secrets in repo; `.env.example` covers every new var; compose boots healthy.

## B. Acceptance (per milestone, condensed)

- M0: `make up` healthy; one port; budgets hold.
- M1: fresh visitor → anon token → consent required → accept → chat placeholder (US-01/04/05).
- M2: scripted dialogues (mild / moderate / test-refused) score exactly (US-06);
  risk-positive → crisis event same turn (US-07).
- M3: result correct incl. no-test branch (US-08); crisis keyword anywhere → overlay <1
  message, logged-out OK (US-09/10).
- M4: Google login migrates history (US-02); OTP login + limits (US-03); router + badges
  (US-11/12); preview == shared == PDF (US-13); no share without consent (US-14);
  trend + reminder + unsub (US-15/16); smoke 5 paths green.

## C. Safety-critical (must-pass, no exceptions, senior re-verifies after ANY related change)

1. Risk screener runs in EVERY screening, including model-led chats.
2. Crisis overlay reachable from every route within 1 message; 115 button dials.
3. No screen/prompt/message claims diagnosis, treatment, or therapist identity.
4. Every shared summary was fully previewed + explicit consent logged.
5. PII redacted before every LLM call; keys server-side only.

## D. UI / i18n / a11y

- RTL everywhere; Persian digits user-facing; Jalali dates; theme hexes exact per palette.
- Contrast ≥ 4.5:1 body / 3:1 large; keyboard-reachable primary actions; 360px wide OK.

## E. Cost + scale (T6 gate)

- `token_usage` per assessment; p95 under supervisor-set cap (target < $0.05).
- `api` stateless: `--scale api=3` serves correctly (senior verifies at M4).
