# AGENTS.md — Build Team Entry Point (Haleman / حال‌من)

You are ONE of three build agents: **senior**, **worker-a**, or **worker-b**.
Supervisors (product owner + AI supervisor) own `main`, merge branches, and give direction.
You build ONLY from this repo. Docs beat assumptions. If a doc is silent on something
that matters (safety, privacy, scope, cost), write it in `STATUS.md` / `tech/questions.md`
— never guess.

## Read order (mandatory before ANY action)

1. `AGENTS.md` (this file)
2. `tech/team.md` — YOUR role card + the team protocol (read it fully)
3. `STATUS.md` — current board, orders, and messages
4. `product/brief.md` — what the product is
5. `product/wireframes/index.html` — screens W-01..W-10 (open in a browser)
6. `tech/technical-decisions.md` — locked stack (Next.js + Django + Docker, one port)
7. `tech/architecture.md` — system shape + data model
8. `tech/implementation-plan.md` — milestones
9. `tech/tasks.md` — task queue (senior assigns, workers execute)
10. `tech/tests.md` — what "done" means
11. `design/design-system.md` — tokens + components

Persian `.docx` files are the legal product record; `.md` files are their agent mirror.
Disagreement → flag in `STATUS.md`, do not resolve alone.

## The stack in 30 seconds

- Frontend: Next.js (App Router, TS, fa/RTL, both themes) → `frontend/`
- Backend: Django 5 + DRF (own code) → `backend/` (+ pure-Python `engine/` inside)
- DB: Postgres 16. LLM: external API, server-side only, cost-capped.
- Deploy unit: `docker-compose.yml` — Caddy proxy is the ONLY published port.
- Tests: pytest (backend+engine, coverage-gated) + Playwright smoke + supervisor acceptance.

## Non-negotiables (all roles)

- **Safety:** crisis protocol on EVERY screen; risk screener ALWAYS runs.
- **Honesty:** never a therapist, never diagnosis/treatment claims; "not a diagnosis" on results.
- **Privacy:** minimal data; anonymous device token; share ONLY with preview + explicit consent.
- **Budget:** $0 — free tiers / OSS only. Log tokens per assessment, stay under cap.
- **Git:** `main` is supervisors-only. Workers push ONLY their own `w-a/*` / `w-b/*` branches.
  Senior reviews, never merges to `main`. One task = one branch = one report.
- **Steps:** milestone by milestone, task by task, tests green before any "done".
