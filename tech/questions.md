# Questions — async channel between build agent and supervisors

Build agent: append dated entries. Supervisors answer inline. Never stall silently.

## Open

- (none — Q-01..Q-11 are answered below. New questions go here as Q-12+.)

## Answered

- [2026-09-26] Q-01 Docker gate → **owner: option (c) both** — GitHub Actions on every push **and** an owner
  spot-run at every milestone gate (owner has Docker locally). Delivered: `scripts/docker-gates.sh`,
  `.github/gates.workflow.yml` (inert), `scripts/activate-ci-gate.sh`. Report: `reports/senior/Q-01-docker-gate.md`.
  **Pending owner action:** activate the workflow (the session's GitHub App has no `workflows` permission, B-05).
- [2026-09-26] Q-02 M0 re-scope → **confirm D-S1**: T-000 = infra fixes only, the boot/healthy/size proof closes at
  the end of T-004. Recorded in `STATUS.md` (D-S1).
- [2026-09-26] Q-03 technical-decisions vs architecture → **fixed in the docs**: TD-05 `backend/engine/scoring.py`,
  TD-06 Django device token + authlib + own OTP, TD-09 server-side PDF in Django; the duplicated "Standing rules"
  heading is merged into one.
- [2026-09-26] Q-04 licence wording → **permissive OSS (MIT/BSD/Apache-2.0/ISC) + LGPL used unmodified; no
  GPL/AGPL/SSPL/commercial.** `psycopg` (LGPL-3.0, unmodified) stays. Recorded in `technical-decisions.md`.
- [2026-09-26] Q-05 Node 20 EOL → **`node:22-alpine`** for `docker/Dockerfile.frontend`; T-004 applies it.
- [2026-09-26] Q-06 `src/` vs `backend/`+`frontend/` → **`backend/` + `frontend/` are canonical**: `src/` deleted,
  the `src/` row removed from the root README. (D-S3 final.)
- [2026-09-26] Q-07 interim crisis layer → **yes**: an always-visible minimal «تماس با اورژانس ۱۱۵» `tel:115` link
  in the root layout on every route, from T-003B until W-10 (T-015) replaces it with the full overlay.
- [2026-09-26] Q-08 `/terms` + «چطور کار می‌کند؟» → **keep the interim `/terms` stub** (heading + «متن نهایی به‌زودی»)
  and the non-navigating W-01 link. **The owner supplies the final legal text (or the lawyer's opinion) before any
  public launch** — re-raise at the launch gate; no agent may write that text (§6).
- [2026-09-26] Q-09 contrast (§D) → **fix the tokens, don't restrict to large text.** Palette **v1.1**:
  light `--soft #6E7989→#626B7A`, `--clay #A9715B→#8D5E4C`, `--sage #7A918D→#5D6E6B`; dark `--card #1D2530→#1B232E`.
  Dark `--primary-bg` stays `#223041` (darkening it flattens the surfaces); the dark **Soft** button label uses
  `--text` instead (10.4:1). Hue/saturation unchanged; no colour became louder. Numbers + measurements:
  `reports/senior/step-0.3-decisions.md`.
- [2026-09-26] Q-10 process order → **confirmed**: a verdict first, then a merge — with the recorded exception that
  T-000/T-002/T-002F were merged before review (D-S8 post-merge verdicts; the T-002F debt is now closed by
  `reports/senior/M1-review-3.md`).
- [2026-09-26] Q-11 404 copy → **approved**: `app/not-found.tsx` with title «این صفحه پیدا نشد», line
  «شاید نشانی را اشتباه وارد کرده‌ای.» and a primary pill «بازگشت به خانه» → `/`. Lands in T-003B.


- [2026-09-26] SENIOR Q-01 → **ANSWERED by the owner (in-session): option (c) both** — automated per-push GitHub
  Actions gate **and** an independent owner spot-run at every milestone gate (the owner confirmed he has Docker).
  Delivered in Step 0.2 (`reports/senior/Q-01-docker-gate.md`): `scripts/docker-gates.sh` (the gate; exit 0 green /
  1 failed / 2 no-Docker = MISSING), `.github/gates.workflow.yml` (inert copy), `scripts/activate-ci-gate.sh`
  (one-command activation). **Caveat recorded:** the session's GitHub App has no `workflows` permission, so the
  workflow file cannot be pushed by the build agent (git push and the REST API both 403). Activation therefore
  needs either a one-command human push or a re-granted Arena GitHub connection. Until then: **no CI run exists —
  missing evidence, not a passing gate.**
