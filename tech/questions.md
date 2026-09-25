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

## Milestone reports

(none yet — file one after each milestone: what shipped, test results, preview URL, blockers)

## Answered

(none yet)
