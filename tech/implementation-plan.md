# Implementation Plan — 5 milestones, senior review gates, supervisor merges

Each milestone ends with: senior consolidated report + green gates + supervisor merge to
`main` + milestone verdict in `STATUS.md`. Next milestone starts only after the verdict.

## M0 — Skeleton boot (infra exists; senior verifies, workers assist)

`make up` boots proxy+web+api+db on ONE port; `make verify-ports` + `make size` green
with placeholder apps. Exit: reviewable green `main`. (T-000)

## M1 — Foundations (device, consent, shell)

Django project + health + device-token model; Next.js shell (RTL/font/theme/tokens);
W-01/W-02 + consent API + log; `make check` wired. Exit: anonymous visitor reaches
consent, accepts, sees chat placeholder. (US-01, US-04, US-05 · T-001..T-004)

## M2 — Chat + screening engine

Chat UI; `/api/chat` + `engine/dialogue` state machine; bounded-autonomy prompts;
deterministic scoring API + pytest vectors; risk screener wiring; stop/resume.
Exit: scripted dialogues score exactly; risk-positive → crisis event same turn.
(US-06, US-07 · T-005..T-011)

## M3 — Result + safety

W-04 result (+no-test wrap-up branch); W-05 calming flow; `engine/risk` + W-10 overlay
on every route; full prompt/copy safety audit. Exit: keyword → overlay <1 message,
logged-out OK; audit signed. (US-08, US-09, US-10 · T-012..T-016)

## M4 — Identity + router + summary + launch-prep

Google + email-OTP login with device-data migration; therapist seed (≥10 verified) +
router + filters; summary + preview + consent log + share + PDF; trend + reminders +
unsub; Playwright smoke; cost-cap report; production compose + runbook.
Exit: end-to-end journey on the compose URL; ALL `tech/tests.md` green.
(US-02, US-03, US-11..US-16 · T-017..T-025)

## Out-of-plan (do NOT build)

Telegram adapter (phase 2), therapist panel, SMS, payments, native apps, second language.
