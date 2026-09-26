# Questions — async channel between build agent and supervisors

Build agent: append dated entries. Supervisors answer inline. Never stall silently.

## Open

- [2026-09-25] SENIOR Q-01 (blocker B-01): the senior sandbox can't run Docker. Every container registry,
  download.docker.com and apt are blocked; PyPI/npm/GitHub work. I **can** run pytest on real Postgres 16.2 (pgserver),
  `npm run build`, headless Chromium, and a static ports check. I **cannot** run `make up`, `make size`, `docker compose build`
  or runtime `verify-ports`. Ask: (a) give senior a Docker-capable environment, or (b) accept, for Docker-engine gates
  only, worker transcripts + one supervisor spot-run per milestone. Until you answer, I use (b) and label those lines
  "docker-gate: evidence-by-transcript".
- [2026-09-25] SENIOR Q-02: M0 as written can't be green. The Dockerfiles need app code, and the plan's "placeholder apps"
  don't exist. Provisional decision D-S1: T-000 = infra fixes only (`.env` bootstrap, POSTGRES_HOST, enforcing
  `make size`, `.dockerignore`); the boot/healthy/size proof moves to the end of T-004. Please confirm or override.
- [2026-09-25] SENIOR Q-03: `technical-decisions.md` TD-05 (`lib/engine/scoring.ts`), TD-06 (Auth.js) and TD-09
  (`@react-pdf/renderer`) contradict the Django architecture (`backend/engine/scoring`, authlib + custom OTP, T-021 PDF by
  worker-a in Django). TD-13..15 also sit below a duplicated "Standing rules" heading. Proposal: TD-05 → `backend/engine/scoring.py`;
  TD-06 → Django device token + authlib Google + custom email OTP; TD-09 → server-side PDF in Django, library picked at
  T-021 within the image budget. Not blocking M1.
- [2026-09-25] SENIOR Q-04: the license rule says "MIT/Apache-licensed", but the locked stack itself is BSD (Django, DRF)
  and every Postgres driver Django supports is LGPL (psycopg). Proposal: "permissive OSS (MIT/BSD/Apache/ISC) + LGPL
  libraries used unmodified; no GPL/AGPL/SSPL/commercial". I've pre-approved psycopg on that basis. Please confirm.
- [2026-09-25] SENIOR Q-05: `docker/Dockerfile.frontend` uses `node:20-alpine`. Node 20 reached end-of-life on 2026-04-30.
  Proposal: `node:22-alpine` (maintenance LTS until 2027-04) in T-004. That's the TD-13 area, so it needs your approval.
- [2026-09-25] SENIOR Q-06: `src/README.md` + root README say the app is built in `src/`, which contradicts `AGENTS.md` and the
  `frontend/`/`backend/` READMEs. Provisional D-S3: `frontend/` + `backend/` are canonical, `src/` untouched. Please
  delete or update `src/README.md` on `main`.
- [2026-09-25] SENIOR Q-07 (safety): AGENTS.md says "crisis protocol on EVERY screen", but the full W-10 overlay is scheduled
  for M3 (T-015). Should M1/M2 screens carry a minimal static «تماس با اورژانس ۱۱۵» (`tel:115`) link in the root layout
  in the meantime? Senior recommendation: **yes** once any screen goes on a public preview. For now worker-b mounts an
  empty `<CrisisLayer/>` only.
- [2026-09-25] SENIOR Q-08: link targets are missing. W-01 «چطور کار می‌کند؟» and W-02 «متن کامل قوانین و حریم خصوصی».
  Where does the terms/privacy text come from (the legal research docx is v1.0 and "needs a lawyer")? Interim: W-01 link is
  non-navigating; W-02 links to a `/terms` stub marked «متن نهایی به‌زودی». Must be resolved before any public launch.
- [2026-09-25] SENIOR Q-09 (a11y + safety): with the palette exactly as given, these pairs fail `tests.md` §D (≥4.5:1
  body text): light `--soft` on `--bg` 3.94:1 (W-01 subtitle, caption links), light `--soft` on `--card` 4.30:1, dark
  `--primary` on `--primary-bg` 3.82:1 (Soft buttons), and **light `--on-primary` on `--clay` 3.61:1, the W-10 «تماس با
  اورژانس ۱۱۵» button**. Options: (a) nudge `--soft` (light) and `--clay` (light) darker, and `--primary-bg` (dark), keeping
  hue; (b) restrict those pairs to large text (≥18.66 px bold / 24 px). Senior recommendation: (a) for `--clay` at least,
  because the crisis button must be legible to someone in distress. Needs a decision before T-015 (M3).
- [2026-09-25] SENIOR Q-10 (process): T-000 + T-002 were merged before the senior review (both workers flagged it). Post-merge
  verdicts are recorded (D-S8). Please confirm the intended order: senior verdict in STATUS.md → supervisor merge.

- [2026-09-26] SENIOR Q-11 (product copy, new): every unknown route serves Next's built-in error page — injected
  `body{background:#fff}` / `#000`, English copy "This page could not be found.", no Vazirmatn (measured in
  `reports/senior/M1-review-3.md` F-1). Fixing it needs new Persian user-facing copy, and §6 forbids inventing
  product copy, so this needs your line. My recommendation: title «این صفحه پیدا نشد», one line
  «شاید نشانی را اشتباه وارد کرده‌ای.», primary pill «بازگشت به خانه» → `/`. Alternatives: (b) you provide the
  copy, (c) keep Next's default English page (not recommended — breaks `tests.md` §D on that route). Lands in T-003B.

## Milestone reports

(none yet — file one after each milestone: what shipped, test results, preview URL, blockers)

## Answered

- [2026-09-26] SENIOR Q-01 → **ANSWERED by the owner (in-session): option (c) both** — automated per-push GitHub
  Actions gate **and** an independent owner spot-run at every milestone gate (the owner confirmed he has Docker).
  Delivered in Step 0.2 (`reports/senior/Q-01-docker-gate.md`): `scripts/docker-gates.sh` (the gate; exit 0 green /
  1 failed / 2 no-Docker = MISSING), `.github/gates.workflow.yml` (inert copy), `scripts/activate-ci-gate.sh`
  (one-command activation). **Caveat recorded:** the session's GitHub App has no `workflows` permission, so the
  workflow file cannot be pushed by the build agent (git push and the REST API both 403). Activation therefore
  needs either a one-command human push or a re-granted Arena GitHub connection. Until then: **no CI run exists —
  missing evidence, not a passing gate.**
