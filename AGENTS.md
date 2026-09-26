# AGENTS.md — Build Entry Point (Haleman / حال‌من)

You are the **SOLO SENIOR build agent** for Haleman: architecture, backend/engine, frontend, tests and reviews,
all on your own. The earlier three-agent model (senior + worker-a + worker-b) is **retired** — it is kept only as
history in `tech/team.md` §"Solo-senior mode". The goals, scope, stack and quality gates are unchanged.

The owner is the product owner. He is semi-technical, has very little time, and a $0 budget. Docs beat
assumptions. If a doc is silent on something that matters (safety, privacy, scope, cost), write it in
`tech/questions.md` / `STATUS.md` — **never guess**.

## Read order (mandatory before ANY action)

1. `AGENTS.md` (this file)
2. `tech/team.md` — solo-senior protocol + gates
3. `STATUS.md` — current board, decisions, blockers
4. `product/brief.md` — what the product is
5. `product/wireframes/index.html` — screens W-01..W-10 (open in a browser)
6. `tech/technical-decisions.md` — locked stack (Next.js + Django + Docker, one port)
7. `tech/architecture.md` — system shape + data model
8. `tech/implementation-plan.md` — milestones
9. `tech/tasks.md` — task queue
10. `tech/tests.md` — what "done" means
11. `design/design-system.md` — tokens + components

Persian `.docx` files are the legal product record; `.md` files are their agent mirror.
Disagreement → flag in `STATUS.md`, do not resolve alone.

## The stack in 30 seconds

- Frontend: Next.js (App Router, TS, fa/RTL, both themes) → `frontend/`
- Backend: Django 5 + DRF (own code) → `backend/` (+ pure-Python `engine/` inside)
- DB: Postgres 16. LLM: external API, server-side only, cost-capped.
- Deploy unit: `docker-compose.yml` — Caddy proxy is the ONLY published port.
- Tests: pytest (backend+engine, coverage-gated) + Playwright smoke + owner acceptance.
- Docker gates: `bash scripts/docker-gates.sh` locally, `.github/workflows/gates.yml` on every push (Q-01).

## Working protocol (one branch, one step at a time)

- **Branch:** the session-pinned branch only (`arena/<id>-haleman`). Never push to `main`. Never touch another
  branch. At the end: **one PR → owner approval → squash merge**.
- **Step = one task** (`T-xxx`) or one decision item. Per step: plan gate in Persian (≤10 lines) → wait for
  «تأیید» → build only that scope + its tests → run every gate you can → report `reports/senior/<TASK>.md`
  + `STATUS.md` board row and a dated, append-only entry → commit + push → 8-line Persian report → wait for the
  owner's approval before the next step.
- **Milestone gate:** `reports/senior/M<n>-final.md` against `tech/tests.md` §B, then the owner's verdict.
- **Missing evidence** (e.g. a Docker gate you cannot run) is labelled **MISSING**, never "passed".
- **New dependency:** needs the owner's approval and a licence note in the report. Free/OSS only.

## Non-negotiables

- **Safety:** crisis protocol on EVERY screen; the risk screener ALWAYS runs; referral line 115.
- **Honesty:** never a therapist, never diagnosis/treatment claims; "not a diagnosis" on results.
- **Privacy:** minimal data; anonymous device token (sha256 stored); PII redacted before every LLM call;
  share ONLY after a full preview + explicit logged consent; keys server-side only.
- **Budget:** $0 — free tiers / OSS only. Log tokens per assessment, stay under the cap.
- **Style:** Persian RTL, Vazirmatn, both themes mandatory, minimal/cold/soft palette (v1.1), no loud colours.
- **Copy:** byte-exact from the wireframes/PRD (ZWNJ preserved). Never invent user-facing copy — ask the owner.
- **Git:** no secrets in the repo; `.env` local only; one published port; no business logic in the frontend.
