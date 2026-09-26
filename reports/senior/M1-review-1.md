# Senior review — M1 round 1 (T-000, T-002)

- Date: 2026-09-25
- Reviewed tree: `main` @ `b7f546e` ("Merge pull request #2 …"). Local clone is shallow, so the effective delta is
  `c1381a6 → b7f546e`: 41 files, +8476/−18 (T-000 infra + T-002 frontend + reports + my round-1 docs).
- Branches reviewed (as reported by the workers):
  - T-000 · worker-a · `arena/01a0da44-haleman` (merged as PR #2). The ordered name `w-a/T-000-m0-boot-check` wasn't
    possible under the worker's session harness. See D-S7.
  - T-002 · worker-b · `w-b/T-002-next-shell` @ `e96f168` (+ docs commit). Duplicate PRs #3 / #4, same head `81a466a`.
- Method: detached worktree of `main` (`git worktree add --detach`). Every command below was run by me.
- **Process note:** both tasks were merged to `main` **before** this review. Both workers flagged it correctly. These
  are therefore **post-merge verdicts**: anything I'd have requested becomes a follow-up task, and nothing is reverted.

## Verdicts

| Task / branch | Verdict | Notes + exact fixes |
|---|---|---|
| T-000 · worker-a · `arena/01a0da44-haleman` | **approve (post-merge)** | Scope exact (Makefile, `.env.example`, compose api env, 2× `.dockerignore`). All logic verified with a docker shim (below). Docker-engine evidence (`docker compose config -q`, fresh-clone `make up` failing at build, base-image pulls) couldn't be produced in either sandbox → **carried into T-004 acceptance**. Nits for T-004: `echo "OK…"` line lacks `@`; `logs`/`build` lost their `##` help comments; superseded templates `docker/.dockerignore.{backend,frontend}` should be deleted (two sources = drift). |
| T-002 · worker-b · `w-b/T-002-next-shell` | **approve (post-merge) + follow-up T-002F** | High-quality lane work, and the report's numbers reproduced exactly. Follow-ups (non-blocking, all in T-002F): **(1)** standalone bundle ships `sharp` + libvips (**LGPL-3.0**, **47 MB of the 65 MB bundle**) although `next/image` isn't used. The report's "all MIT/Apache/ISC" is true only for direct deps. **(2)** `eslint` pinned `^9.39.5`, not exact. **(3)** W-01 shows the brand twice (app header «حال‌من» + H1); the wireframe W-01 has no header brand. **(4)** document the dev-only `ALLOWED_DEV_ORIGINS` in `frontend/README.md`. |

Worker-b deviations D-1..D-8: **D-1** accepted (non-navigating focusable button until Q-08) · **D-2** accepted
(`skipTrailingSlashRedirect`, consistent with D-S6) · **D-3** accepted (no `theme-color`) · **D-4** accepted: the token gate
is a checkout gate, and T-004 adds `npm run check:tokens` to `make check` · **D-5** accepted (ESLint 9) but pin it exactly
· **D-6** confirmed by my own computation → escalated **Q-09**, with one more pair I found · **D-7** → T-024 direction D-S10
· **D-8** accepted: `npm start` stays out of every gate.

## Consolidated test evidence (I ran these myself)

Environment: senior sandbox, no Docker engine (B-01). Node 22.22.3 / npm 10.9.8, Chromium 131 (npm-shipped), Python 3.11.

### T-000

| Check | Result |
|---|---|
| `make env` on fresh copy | creates `.env` == `.env.example` ✔ |
| `make env` second run with a custom line appended | custom line preserved (never overwrites) ✔ · `.env` is git-ignored ✔ |
| `make size`, docker absent from PATH | `FAIL: docker is required`, exit 2 ✔ (was exit 0 before → F4 closed) |
| `make size` via docker shim: api 300 MB / web 200 MB | `OK: image sizes within budgets`, exit 0 ✔ |
| api **exactly** 350 000 000 B | OK, exit 0 ✔ (boundary inclusive, as specified) |
| api 350 000 001 B | `FAIL: haleman-api exceeds 350000000 bytes`, exit 2 ✔ |
| web 250 000 001 B | `FAIL: haleman-web exceeds 250000000 bytes`, exit 2 ✔ |
| web image missing | `FAIL: image haleman-web is missing`, exit 2 ✔ |
| published ports (static parse of merged compose) | proxy 1, web 0, api 0, db 0 → **TOTAL 1** ✔ |
| compose api env | `POSTGRES_HOST: ${POSTGRES_HOST:-db}`, `POSTGRES_PORT: ${POSTGRES_PORT:-5432}` ✔ (F3 closed) |
| `.dockerignore` files | backend + frontend present at the context roots; **`tests/` kept** (the old template excluded it, which would have broken T-004) ✔ (F7 closed) |

### T-002 (fresh `npm ci` in a clean worktree, no `node_modules`/`.next`)

| Check | Result |
|---|---|
| `npm ci` | 381 packages ✔ |
| `npm run lint` / `npm run typecheck` | exit 0 / exit 0 ✔ |
| `npm run check:tokens` | 10× ok, `OK: tokens 1:1 with palette.md, 16 files scanned, 0 stray hexes` ✔ |
| token gate mutation test | changed one hex (`#3D5A80→#3D5A81`) → **exit 1**; stray `#FF0000` in `lib/` → **exit 1**; restored → exit 0 ✔ (the gate has teeth) |
| `npm run build` | Next 16.3.6, routes `○ /`, `○ /_not-found`, exit 0 ✔ |
| standalone server (`node server.js`), Chromium | `lang=fa dir=rtl`; light bg `rgb(245,242,234)`=#F5F2EA, dark `rgb(21,27,36)`=#151B24; Vazirmatn loaded; no x-overflow at 390 and 360 px; 3 targets all 44 px; **exactly 1** `/api/me/` per load; **0 third-party requests** ✔ |
| theme matrix after hydration (OS × stored) | light×dark, dark×light, light×none, dark×none → theme, label and `aria-pressed` all consistent; click round-trips + persists ✔. Nit: before hydration the server-rendered label is always «تم تیره» (a sub-second label flash for stored-dark users). Optional fix. |
| W-01 vs wireframe (side-by-side screenshots) | brand / 2 soft lines / full-width primary pill / soft link: layout matches ✔. Deviation: extra app header brand (follow-up 3) |
| license scan, all `node_modules` | MIT 315, Apache-2.0 25, ISC 20, BSD 9, others permissive. MPL-2.0 ×4 (lightningcss, axe-core): build/dev only. LGPL ×3 (sharp/libvips) |
| license scan, `.next/standalone/node_modules` (what ships) | 18 pkgs. **LGPL-3.0: `@img/sharp-libvips-linux-x64`, `…-linuxmusl-x64`, `@img/sharp-wasm32`**, 47 MB total → follow-up 1 |
| env / secrets | only `NODE_ENV` + dev-only `ALLOWED_DEV_ORIGINS` read; no `NEXT_PUBLIC_*`; no `.env` tracked; no key patterns ✔ |

- coverage (`engine/` / backend): n/a (no backend code merged yet).
- `make verify-ports` / `make size`: static ports = 1 ✔. Size logic verified by shim ✔. **Real image sizes: docker-gate,
  evidence-by-transcript → none exists yet** (B-01 + worker-a + worker-b B-03: no sandbox has Docker). Worker-b's payload
  proxy: 66.7 MB runner + ~130 MB base ≈ 197 MB < 250 MB. After T-002F drops sharp, expect roughly −20…−47 MB.
- **Safety §C:** C1 n/a (no screening) · C2 `<CrisisLayer/>` is mounted on every route but empty per order; the overlay is M3 and the
  interim 115 link awaits Q-07 · C3 no diagnosis/treatment/therapist wording in any UI string or metadata ✔ · C4 n/a · C5
  no keys or env in client code ✔. **No §C regression.**

### Contrast (tests.md §D), computed by me with WCAG 2.x relative luminance

| Pair | Ratio | §D |
|---|---|---|
| light `--soft` on `--bg` (W-01 subtitle 13 px + «چطور کار می‌کند؟» 12 px) | 3.94:1 | ✘ body text |
| light `--soft` on `--card` | 4.30:1 | ✘ body text |
| dark `--primary` on `--primary-bg` (Soft button) | 3.82:1 | ✘ body text |
| **light `--on-primary` on `--clay` (M3 «تماس با اورژانس ۱۱۵» button)** | **3.61:1** | ✘ body text. **New, safety-critical control** |
| light CTA, dark CTA, text/bg both themes, dark soft/bg, dark clay/clay-bg | 4.67–11.10:1 | ✔ |

The palette is the design source of truth, so workers change nothing here → **Q-09** to supervisors.

## Erratum (my M0-review-1)

F7 said "no `.dockerignore`". Precisely: `docker/.dockerignore.backend` / `.frontend` existed at `c1381a6` as
**templates** ("place a copy there as .dockerignore"). Docker doesn't read them in that location, so the finding held
in effect, but my wording was wrong. My `ls` hid dotfiles. The templates are now superseded → delete in T-004.

## Integration notes

- `main` now builds the frontend. The backend is still empty, so `make up` still fails at the api build until T-001 lands (expected).
- Merge order from here: **T-001 → T-003A**, **T-002F → T-003B**, then **T-004**. T-002F and T-003B both touch
  `frontend/`: T-002F owns `package.json`, `package-lock.json`, `next.config.ts`, `app/layout.tsx`; T-003B owns `app/consent`, `app/terms`,
  `app/chat`, and `lib/api.ts` (additions only).
- Supervisors: please **close whichever of PR #3 / #4 is still open**. Both carry the same commit.

## Next orders

| Task | Worker | Branch to create | Start |
|---|---|---|---|
| T-001 Django skeleton (unchanged, order in `M1-orders-1.md`) | worker-a | `w-a/T-001-django-skeleton` | now (was pre-authorised; no branch seen yet) |
| T-002F shell follow-ups (4 items below) | worker-b | `w-b/T-002F-shell-followups` | now |
| T-003B W-02 + `/terms` stub + `/chat` placeholder (unchanged) | worker-b | `w-b/T-003B-consent-screen` | once T-002F is pushed + reported (pre-authorised; branch from `main`) |
| T-003A consent API | worker-a | `w-a/T-003A-consent-api` | after T-001 is merged |
| T-004 integration (+ amendments below) | worker-a | `w-a/T-004-compose-integration` | after T-001, T-002F, T-003A, T-003B are merged |

**T-002F** (worker-b), acceptance per item:

1. Drop `sharp` from the runtime: `images: { unoptimized: true }` + `outputFileTracingExcludes: { "*": ["node_modules/sharp/**",
   "node_modules/@img/**"] }` (or the Next 16 equivalent). Evidence: `du -sh .next/standalone` before/after, license scan of
   `.next/standalone/node_modules` → only permissive licenses, standalone server still serves `/` + fonts, build green.
2. `eslint` exact `9.39.5` in `package.json` (lockfile consistent, `npm ci` clean).
3. W-01: no app-header brand text on `/` (wireframe W-01 has none). Keep `<ThemeToggle/>` reachable. Other routes keep
   the header. Screenshot light+dark.
4. `frontend/README.md`: one line documenting dev-only `ALLOWED_DEV_ORIGINS`.
   Optional: remove the pre-hydration toggle-label flash. No other changes.

**T-004 amendments** (worker-a), added to the round-1 order:

- a. Delete `docker/.dockerignore.backend` / `.frontend` (superseded templates). Add `@` to the size `echo`; restore the `##` help comments.
- b. `make check` also runs `npm run check:tokens` (from the checkout, per D-4). Keep `npm start` out of all gates (D-8).
- c. **Default secrets:** `make env` must generate a random `DJANGO_SECRET_KEY` (≥50 chars) and `POSTGRES_PASSWORD`
  when it creates `.env` (python3 `secrets`, never overwriting an existing file). Settings refuse any value starting with
  `change-me` when `DJANGO_DEBUG=0`, with a test.
- d. T-004 acceptance now also carries T-000's Docker evidence: `docker compose config -q` on a fresh clone and real
  `make size` numbers for **both** images (closes worker-b B-03).

## Risks / escalations to supervisors

- **Merged before review (process):** please wait for the senior verdict in `STATUS.md` before merging (`tech/team.md`
  supervisor cycle step 1). Post-merge review works, but any request-changes then costs an extra follow-up branch.
- **No Docker anywhere (B-01 + worker-a + B-03):** no sandbox in this team has a Docker engine. T-004 **can't** meet
  its acceptance in any sandbox we have. It needs a Docker-capable runner (supervisor machine or CI). Please answer Q-01 before T-004 starts.
- **Q-09 (new):** contrast. Four palette pairs fail §D's 4.5:1 body text, including the light-theme 115 crisis button (3.61:1).
  Needs a palette/typography decision before T-015.
- Q-02..Q-08 still open (Q-07 matters as soon as any public preview exists).
