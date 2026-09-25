# STATUS — Haleman build coordination (append-only, newest at bottom of each section)

> Roles: supervisors (owner+AI) · senior · worker-a (backend lane) · worker-b (frontend lane).
> Protocol: `tech/team.md`. Tasks: `tech/tasks.md`. Tests: `tech/tests.md`.

## Milestone

- [2026-09-25] M0+M1 starting. Goal: compose boots with one port; Django+Next skeleton;
  W-01/W-02 + device token + consent API. Pack: tech-pack v2 (Django + Docker + 3-agent team).

## Task board

| Task | Worker | Branch | Status | Report |
|---|---|---|---|---|
| T-000 verify compose skeleton | unassigned | — | ⬜ todo | — |
| T-001 Django project + health + device model | unassigned | — | ⬜ todo | — |
| T-002 Next.js shell + RTL + theme + fonts | unassigned | — | ⬜ todo | — |
| T-003 W-01 + W-02 + consent API + log | unassigned | — | ⬜ todo | — |
| T-004 compose integration + make check | unassigned | — | ⬜ todo | — |

(Further milestones: senior extends the board from `tech/tasks.md` when assigning.)

## Orders (senior → workers)

- [2026-09-25] SUPERVISORS → SENIOR: pack v2 is locked. Read `AGENTS.md` + `tech/team.md`,
  verify M0 skeleton yourself, then post the first orders (T-000..T-004 split across A/B).

## Message board

- [2026-09-25] SUPERVISORS: welcome, team. Step by step, tests always green, one port,
  small images. Senior: you own the plan's daily truth here.

## Decisions

- [2026-09-25] Stack locked: Next.js + Django/DRF + Postgres 16 + Caddy, single published
  port, image budgets backend ≤350MB / frontend ≤250MB. (TD-01..TD-16)

## Blockers

- (none)
