# Technical Decisions (locked by supervisors — D6)

| ID | Decision | Chosen | Why | Trade-off / review trigger |
|---|---|---|---|---|
| TD-01 | Frontend | Next.js (App Router, TypeScript) | Agent-standard, free hosting, RTL + fa ready, PWA path | Heavier than static; review if free tier limits hit |
| TD-02 | Backend | Django 5 + DRF (own code, containerized) | Supervisor choice: full control, Python engine, no BaaS lock-in | More agent hours than BaaS; lanes split the load (team.md) |
| TD-03 | Database | Postgres 16 (compose service, Django ORM); managed free-tier as fallback | Same Postgres everywhere: local = prod; Django-native | If a managed DB is ever needed, env-swap only (no code change) |
| TD-04 | AI engine | External LLM API (cheap chat model), capped per assessment | Fastest start; deterministic code does all scoring | Cost + dependency; T6 validates cap; hybrid/self-host is the documented escape hatch |
| TD-05 | Scoring | Deterministic functions in `lib/engine/scoring.ts` | Clinical arithmetic must never depend on LLM output | None — non-negotiable |
| TD-06 | Auth | Progressive: device token → Google One-Tap / email OTP (Auth.js + custom OTP) | Frictionless entry + identified progress (D11) | SMS deferred to phase 2 (budget) |
| TD-07 | Mail | Free SMTP (Resend free tier first, Gmail SMTP fallback) | OTP + reminders at $0 | Deliverability review at scale |
| TD-08 | Styling | Tailwind + CSS vars from `design/brand-kit/palette.md`; Vazirmatn self-hosted | Single token source; both themes via `[data-theme]` | No other font, no gradients, no vivid colors |
| TD-09 | PDF summary | Server-side `@react-pdf/renderer` (RTL-tested) | Shareable artifact for doctors | If RTL breaks, fallback: printable HTML → print-to-PDF |
| TD-10 | Deploy unit | Docker Compose anywhere (VPS/free Docker host) — host picked at D7 | One artifact from laptop to prod; no host lock-in | Free-Docker-host limits reviewed at D7 with sanctions/`.ir` |
| TD-11 | Language/locale | `fa` only, RTL, Jalali dates, Persian digits in UI | Target user is Iranian | No i18n framework until phase 2 |
| TD-12 | Testing | pytest (engine ≥90%, backend ≥80%) + Playwright smoke (5 paths) + supervisor acceptance | Coverage gates enforce "complete tests"; thin E2E | Senior re-runs gates per review round |

## Standing rules

- Free tiers only. Any new dependency must be free, MIT/Apache-licensed, and justified in a commit message.
| TD-13 | Containers | Multi-stage slim Dockerfiles + `.dockerignore` + non-root + healthchecks | Small, secure, cache-friendly images | Budgets enforced: backend ≤350MB, frontend ≤250MB (`make size`) |
| TD-14 | Single port | Caddy 2-alpine as sole entrypoint; `/api/*`→api, `/*`→web; nothing else publishes | One-port rule, auto load-balance on `--scale api=N` | Any second published port fails the task |
| TD-15 | Build team | 1 senior + 2 workers via git branches + STATUS.md + reports/ ; supervisors merge `main` | Parallel lanes with review gates; harness-neutral | Protocol in `tech/team.md`; senior breaks ties, supervisors override |

## Standing rules

- Free tiers / OSS only. New deps need senior approval + report entry.
- `main`: supervisors merge only. `technical-decisions.md` changes ONLY with supervisor approval.
