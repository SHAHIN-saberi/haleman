# Senior report — Step 0.4: retire the team roles (solo-senior mode)

- Date: 2026-09-26 · Author: solo senior · Step: 0.4 (docs only, last Step-0 item)
- Owner verdict: approved ("تایید") — this is the amendment, not a rewrite of history.
- Branch `arena/01a0dcf9-haleman` · no product code touched.

## What changed

| File | Change |
|---|---|
| `AGENTS.md` | Rewritten as the **solo-senior entry point**: identity, read order (unchanged list), stack summary (+ the Docker gate), the one-branch/plan-gate/done-gate protocol, and the non-negotiables (safety, honesty, privacy, budget, style, copy, git). The three-agent framing is gone. |
| `tech/team.md` | Rewritten as **Solo-senior mode**: roles (owner + solo senior), branching (session branch → one PR → owner squash-merge), the 5-step cycle, `STATUS.md` protocol, quality gates (unchanged), prohibitions (unchanged), and a `## History — the retired three-agent model` section below the line that keeps the former structure and the two process lessons (branch exclusivity by live remote state; post-merge verdicts, former D-S8/D-S11). |
| `STATUS.md` | Header roles line updated; board column `Worker` → `Lane`; dated milestone entry for this step; new decision **D-S16**; note that entries from before this step are the retired model's history and stay append-only. |
| `tech/tasks.md` | Title/queue wording; the "Lanes: A/B" footer now says *code placement only*. |
| `tech/technical-decisions.md` | **TD-15** marked superseded → solo senior, one branch, one PR, owner merges. |
| `backend/README.md`, `frontend/README.md` | Lane headers: "worker-a lane, senior reviews" → "backend/engine lane, solo senior" (same for frontend). |
| `reports/_TEMPLATE_WORKER.md` | Retitled "Task report" and the author line now reads *solo senior*, with a comment that Step reports combine this template with `_TEMPLATE_SENIOR.md`. Kept for history and for the per-task report shape. |

## What deliberately did **not** change

- **Gates** (backend coverage 90/80, ruff, engine purity, frontend lint/typecheck/tokens/build, one published port,
  image budgets, §C safety re-verification, §D UI/a11y) — identical text, still binding.
- **Product scope, stack, palette, copy rules, prohibitions.**
- **History**: `reports/worker-a/`, `reports/worker-b/`, all pre-2026-09-26 orders and entries in `STATUS.md`, and
  `reports/senior/M1-orders-1.md` are untouched — they are the audit trail of the retired model.

## Verification (this step is text-only)

```
$ git diff --stat            # see below
$ grep -rn "worker-a\|worker-b" --include="*.md" . | grep -v "^./reports/" | grep -v node_modules
   (only STATUS.md history lines, tech/team.md history section, templates and the M1 report names)
$ ./… gates                   # untouched by this step; last full run on this branch:
   pytest 19 passed / 95.25 % · ruff clean · lint · typecheck · check:tokens (17 files, 0 stray hexes) · build green
```

Diff (this commit): `AGENTS.md`, `tech/team.md`, `STATUS.md`, `tech/tasks.md`, `tech/technical-decisions.md`,
`backend/README.md`, `frontend/README.md`, `reports/_TEMPLATE_WORKER.md`, this report. No `.py`, `.ts`, `.tsx`,
`.css`, `.yml` or infra file.

## Step 0 — closed

| Step | Status | Evidence |
|---|---|---|
| 0.1 T-002F post-merge review | ✅ approve | `reports/senior/M1-review-3.md` |
| 0.2 Q-01 Docker gate | ✅ delivered (workflow activation pending owner, B-05) | `reports/senior/Q-01-docker-gate.md` |
| 0.3 Q-02..Q-11 decisions + palette v1.1 | ✅ applied | `reports/senior/step-0.3-decisions.md` |
| 0.4 retire the team roles | ✅ this report | `reports/senior/step-0.4-solo-mode.md` |

Next: **T-003A** (consent API + log + server-side gate, carrying N-1 from `M1-review-2`), then **T-003B** (W-02 +
`/chat` placeholder + Q-07 interim 115 link + Q-11 `not-found.tsx` + F-2 focus-ring fix), then **T-004**
(compose integration + amendments a–f + the first real Docker evidence).
