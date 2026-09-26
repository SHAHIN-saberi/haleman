# Senior review — M1 round 3 (T-002F, post-merge)

- Date: 2026-09-26
- Reviewed: PR #8 — `arena/01a0dc47-haleman` @ `fad6bcc` ("T-002F: drop sharp/LGPL from standalone, exact eslint pin, no W-01 header brand, README env"), base `e66f3f8` (post PR #7), merged by the supervisor into `main` as **`fded81f`** (`git log`: `a554be4` = PR #9, the docs truth-up after it).
- Delta reviewed: 14 files, +429/−9 — `frontend/{README.md, app/layout.tsx, components/AppHeader.tsx (new), components/ThemeToggle.tsx, next.config.ts, package.json, package-lock.json}` + `reports/worker-b/**` + `STATUS.md`.
- Method: full delta read; **every claim of `reports/worker-b/T-002F.md` re-produced by me** in a fresh copy of `main` (`git archive HEAD frontend` → `/tmp/t002f-review`, and a clean rebuild in `/tmp/t002f-clean`), plus the "before" state rebuilt from `e66f3f8` in `/tmp/t002-before` for the size/license comparison. No worker number was adopted without re-running it.
- Environment: senior sandbox, Node **v22.22.3**, npm 10.9.8, Chromium **153.0.0** (npm `@sparticuz/chromium` + `playwright-core`, installed in `/tmp` outside the repo, D-S10) with the shim's `al2023` runtime libs. **No Docker engine** (`docker: command not found`) — B-01.

## Verdict

| Branch / PR | Verdict (approve / request-changes) | Notes + exact fixes |
|---|---|---|
| T-002F · worker-b · `arena/01a0dc47-haleman` @ `fad6bcc` (PR #8 → `main` @ `fded81f`) | **approve — post-merge, no rework required** | Scope exact (verified by a path filter over the whole delta: 0 files outside `frontend/`, `reports/worker-b/`, `STATUS.md`; `Makefile`/compose/`docker/`/`Caddyfile`/`.env.example`/`backend/`/`tech/`/`product/`/`design/`/`src/` untouched). All 4 ordered items + the optional fix are present and every material claim reproduces here. Two evidence-scope notes (F-4) and two non-blocking findings (F-1 route-level §D gap, F-2 focus-ring transition) are recorded below; neither is a T-002F regression and neither blocks M1. Docker-gate evidence stays **MISSING** (B-01/Q-01), not passing. |

Worker-reported results were **not taken on trust**: the size delta, the licence scan, the runtime proof, the theme matrix and the pre-hydration fix were all re-run by me (tables below). One worker **harness artefact** of my own is worth recording: blocking all of `/_next/static/chunks/**` also blocks the CSS (it is served from that path), which makes the CSS-driven toggle labels look broken. Re-running with **only `*.js` blocked** (the worker's method) gives their result. The first screenshot of that mistaken run was deleted from the repo; the correct one is `senior-t002f-prehydration-dark-js-only.png`.

## Claim-by-claim reproduction

| # | Worker claim | My independent result | ✓ |
|---|---|---|---|
| 1 | `images.unoptimized` + tracing excludes: `.next/standalone` 65 049 164 B → 16 891 486 B (−74 %) | Rebuilt both heads myself: **before `65 049 150` B → after `16 891 486` B** (−48.16 MB, −74.0 %). `du -sh` = 65M → 19M | ✓ |
| 2 | runner payload (standalone + `.next/static` + `public`) 66.0 MB → 17.9 MB | **17 871 029 B** (standalone 16 891 486 + static 610 911 + public 368 632); the report's 17 867 075 B differs by **+3 954 B (0.02 %)**, rebuild noise — same conclusion | ✓ |
| 3 | shipped packages 18 → 7, **0 LGPL/GPL**, 0 native `.node` | My walker finds **12 npm packages after** (7 top-level + 5 nested under `next/dist/compiled/*` that the worker's list omits) and **23 before**; licences after: **11 MIT + 1 Apache-2.0**, **0 LGPL/GPL**, **0 `*.node`**, no path matching `sharp|libvips|@img` | ✓ |
| 4 | file-level scan of `next/dist/compiled/*`: 44 MIT · 2 Apache-2.0 · 2 BSD-3-Clause · 2 ISC · 1 BlueOak-1.0.0 · 1 CC0-1.0 | **Exact match**, reproduced character-for-character from my own walk of `.next/standalone` (1 106 files) | ✓ |
| 5 | standalone serves `/` + the 3 fonts; `/_next/image` no longer exists | `200` for `/` and all three `.ttf`; `/_next/image?…` → **404** (optimizer route gone, sharp never required) | ✓ |
| 6 | served fonts byte-identical to `design/brand-kit/fonts/` | `sha256` served == brand-kit for all three: Regular `b69fd4c6…`, Medium `b986623e…`, Bold `f635fdbe…` | ✓ |
| 7 | `eslint` exact `9.39.5`; lockfile 1-line diff; `npm ci` clean | `package.json`/`package-lock.json` root spec only; `npm ci` → "added 381 packages" exit 0; `npm ls eslint` → `eslint@9.39.5`; **every** direct dep exact (0 non-exact specs) | ✓ |
| 8 | no header brand on `/`, toggle kept, other routes keep the brand, correct in the **served HTML** | `curl /` → `<header … justify-end>` with the toggle `<button>` only (0 brand spans); `curl /unknown-route` → `<header … justify-between>` with `<span>حال‌من</span>` + toggle | ✓ |
| 9 | `ALLOWED_DEV_ORIGINS` is dev-only and documented | Read the installed Next: `allowedDevOrigins` is consumed by `server/lib/router-utils/block-cross-site-dev.js` (dev-server path only). The string also appears in the *compiled prod runtime* (`next-server/server.runtime.prod.js`) as a dead code path — behaviourally dev-only, as documented. README entry present | ✓ |
| 10 | pre-hydration toggle label fixed (no «تم تیره» flash for stored-dark users) | With **only `*.js` blocked** (7 chunks), stored=dark + OS=light → `data-theme=dark`, rendered spans `[تم تیره: display none, تم روشن: block]`, visible `«تم روشن»` — **correct before hydration**; OS=light/no storage → light + «تم تیره»; OS=dark → dark + «تم روشن». Their remaining nit also reproduces: `aria-pressed` is still the server value `false` until hydration | ✓ |
| 11 | theme matrix consistent after hydration | click → `dark` + `localStorage['haleman-theme']=dark` + label «تم روشن» + `aria-pressed=true`; reload keeps dark | ✓ |
| 12 | 390 px and 360 px, both themes, no horizontal overflow, toggle 44 px | `scrollWidth == innerWidth` (390/390, 360/360) both themes; toggle box `h=44` (`w=77` light, `w=88` dark), `x=16` (inline-end) | ✓ |
| 13 | W-01 copy exact incl. ZWNJ | Codepoint comparison of every string against `product/wireframes/index.html` W-01: «حال‌من», «حالت چطوره؟», «قدم اول، ناشناس و امن», «شروع گفت‌وگو», «چطور کار می‌کند؟» — **all five byte-equal**, ZWNJ (U+200C) present in brand, button and link | ✓ |
| 14 | W-01 renders both themes as the wireframe does | Rendered the wireframe's own W-01 phone frame (light+dark) and my app screenshots side by side: `senior-t002f-comparison.png`. Light bg `#F5F2EA`, dark bg `#151B24`, primary pill + ghost link in the wireframe's positions | ✓ |

### Gates re-run by me (all on `main` @ `HEAD` = `a554be4`, frontend = PR #8 head tree)

| Check | Command | My result |
|---|---|---|
| install | `npm ci` (fresh archive copy) | `added 381 packages`, exit 0 ✔ |
| lint | `npm run lint` | exit 0, no output ✔ |
| typecheck | `npm run typecheck` | exit 0, no output ✔ |
| tokens | `npm run check:tokens` (repo checkout) | `OK: tokens 1:1 with palette.md, 17 files scanned, 0 stray hexes` ✔ (17 = 16 + the new `AppHeader.tsx`) |
| tokens, fail-closed proof | same script in a copy without `design/` | exit **1**, "FAIL cannot read design/brand-kit/palette.md" ✔ (D-S9 behaviour confirmed both ways) |
| build | `npm run build` | `✓ Compiled successfully`, 3/3 static pages ✔ |
| runtime | `node server.js` (runner layout), curl | `/` 200 `text/html`; 3 fonts 200; `/_next/image` 404; `/api/me/` 404 (expected: no Caddy/backend in this harness) ✔ |
| browser | Chromium 153, 390×844 and 360×844, light+dark | 13 requests, **0 third-party origins**, RTL (`lang=fa dir=rtl`), Vazirmatn loaded in both themes ✔ |
| backend (unchanged by T-002F, re-run for context) | `pytest --cov` on Postgres 16.2 | 19 passed, 95.25 %, `ruff` clean ✔ |
| **Docker gates** | `docker compose build web`, real `make size` (web ≤ 250 MB), runtime `make verify-ports`, in-image pytest | **NOT RUNNABLE — `docker: command not found`** (B-01/Q-01). **Missing evidence, not passing evidence**; carried into T-004 per amendment (d) |
| static ports check (substitute, unchanged file) | YAML parse of `docker-compose.yml` | proxy 1, web 0, api 0, db 0 → **TOTAL 1** ✔ (T-002F changed no infra file) |

### §C / §D status for this delta

- **§C:** no copy, prompt, engine or API change in T-002F → C1/C4/C5 n/a; **C2** `<CrisisLayer/>` is still mounted in the root layout on every route (verified in `layout.tsx`), still an empty placeholder → the interim 115 link remains **Q-07** (blocking on the owner, not on this task); **C3** no diagnosis/treatment/therapist wording added; the metadata/description string is unchanged. **No §C regression.**
- **§D:** RTL ✔, both themes ✔, hexes exact (token gate) ✔, 360 px ✔, keyboard: first tab stop = `<ThemeToggle/>` (44 px), then CTA, then ghost link — all `:focus-visible` with a 2 px `--primary` ring ✔. Persian digits/Jalali: n/a on W-01 (no digits, no dates). Contrast: unchanged by T-002F and still tracked under **Q-09**; two new *measurements* are added below (F-2).

## Findings

| # | Sev | Finding | Disposition |
|---|---|---|---|
| F-1 | MEDIUM (route-level §D, pre-existing since T-002 — **not** a T-002F regression) | Unknown routes render Next's built-in error page with its own injected style, measured verbatim from the DOM: `body{color:#000;background:#fff;margin:0}… @media (prefers-color-scheme:dark){body{color:#fff;background:#000}…}`. Measured `body` background = `rgb(255,255,255)` in light and `rgb(0,0,0)` in dark, `document.fonts.check("13.5px Vazirmatn")` = **false**, copy "This page could not be found." in English, `<h1>` = `404`. The app header (brand + toggle) on that route is correct, as the worker said. So one route violates §D (theme hexes, fa copy, Vazirmatn) — pure black/white are explicitly excluded by the palette ("بدون مشکی خالص و سفید خالص در سطوح بزرگ"). | Confirmed worker-b's observation with exact evidence (screenshots `senior-t002f-404-{light,dark}.png`). Fix = `frontend/app/not-found.tsx` on tokens with fa copy. **The fa copy is new user-facing product copy, which §6 says must not be invented** → logged as **Q-11** to the owner (my proposed line + alternatives), to land in **T-003B**. |
| F-2 | LOW (a11y, pre-existing; visible in T-002F's own evidence) | The shared button base uses `transition-colors` (150 ms), which includes **`outline-color`**. Measured timeline after Tab onto the primary CTA (light): `8 ms → rgb(245,242,234)`, `20 ms → rgb(239,237,231)`, `36 ms → rgb(213,215,215)`, `53 ms → rgb(161,173,186)`, then settling on `rgb(61,90,128)`. In other words the ring starts at the text colour (cream) on a cream background — **≈1.06:1, i.e. invisible — for roughly the first 100 ms**, then becomes the correct `--primary` ring (light **6.31:1** on `--bg`, dark **4.93:1**). Steady state is compliant; the transient is not, and a screenshot taken immediately after Tab (exactly what the T-002F report shows) can capture it. | Exact fix (one line, shared): replace `transition-colors` with `transition-[color,background-color,border-color]` in `frontend/components/ui/Button.tsx` `BASE` and in `components/ThemeToggle.tsx` (and the W-01 ghost link), so `outline-color` is never animated. **Proposed as a small ordered addition to T-003B** (see the plan gate; `Button.tsx` is not in T-003B's original path list, so it needs your nod). Evidence: `senior-t002f-focus-transient-cta.png` vs `senior-t002f-focus-settled-cta{,-dark}.png`. |
| F-3 | LOW (harness-only, disappears with T-003B) | In the standalone-only harness (no Caddy, no backend) the page logs two console 404s: `/api/me/` (expected — T-001's API is not behind this server) and `/consent?_rsc=…` (Next prefetching the CTA target, which does not exist until T-003B). | No action; recorded so the next reader does not mistake them for regressions. |
| F-4 | INFO (evidence scope) | Two of the worker's numbers describe a **narrower scope than the sentence suggests**: (a) "shipped packages 18 → 7" counts **top-level** packages only — with the nested `next/dist/compiled/*` set included it is 23 → 12; (b) runner payload 17 867 075 B vs my 17 871 029 B (+0.02 %). Their separate file-level scan (claim 4) does cover the nested set and matches me exactly, so the **material** claims (0 LGPL/GPL, 0 native binaries, only permissive licences, −74 %) all hold. | No rework; recorded for accuracy in the next report. |
| G-1 | ENVIRONMENT (carried) | `docker compose build web`, real `make size`, runtime `make verify-ports`, `make check`, in-image pytest: **not runnable here** (B-01 family, every team sandbox). The web image size therefore remains an **estimate** (worker: ≈148 MB with a `node:20-alpine` base), not a measured value. | Carried into T-004 amendment (d) + Q-01. |
| G-2 | ENVIRONMENT (note) | My browser evidence uses Chromium 153 from npm with the shim's bundled `al2023` runtime libs (the pack ships them; `setupLambdaEnvironment()` is a no-op here). Rendering of both themes and RTL is unaffected. | No action. |

Positives worth recording: the fix is exactly the kind the senior order asked for and nothing more (7 app files + report + own board rows); the licence problem is genuinely solved rather than declared (`sharp`/`libvips`/`@img` and their support packages are gone, 0 native binaries, `/_next/image` now 404s); the pin is exact in both `package.json` and the lock root spec with a one-line diff; the header change is invisible in the served HTML (no hydration flash); the pre-hydration label fix uses CSS rather than JS so it holds with scripts blocked; and the report itself separates produced evidence from missing evidence honestly, including a self-flagged out-of-scope 404 observation that turned out to be a real finding (F-1).

## Integration notes

- Nothing to re-merge: PR #8 is already on `main`; `git diff fad6bcc HEAD -- frontend/` = **empty**, so the reviewed tree is exactly what `main` ships.
- **Sequencing:** T-003A (consent API) and T-003B (W-02 + `/chat`) remain unblocked — the start conditions in `M1-orders-1` §Wave 2 are met (T-001 merged by PR #6, T-002F merged by PR #8).
- T-003B will graft onto `AppHeader`/`ThemeToggle`/`Button` cleanly: the header is now one component and the toggle's label logic is CSS-driven, so adding the W-02 screen touches none of it. `layout.tsx` is the only shared file and T-002F already moved its header markup out.
- T-004 keeps everything it had: amendment (a) templates, (b) `check:tokens` in `make check`, (c) generated secrets, (d) carried Docker evidence (T-000/T-001/T-002/T-002F image sizes) + Q-01.
- **Registry of small add-ons now waiting for the owner's nod (plan gates):** F-1/`not-found.tsx` + Q-11 copy → T-003B; F-2 focus-ring transition → T-003B; Q-07 interim 115 link → T-003B (recommended "yes").

## Risks / escalations to supervisors

- **Q-01 is still the M1 critic-path blocker**: without a Docker-capable runner, no sandbox on this team can produce `make up` / `make size` / runtime `make verify-ports` / in-image pytest. T-004's acceptance and the M1 exit cannot close on evidence, only on absence of evidence.
- **Q-11 (new, owner input needed):** Persian copy for the 404 route. My recommendation, minimal and in the product's voice: title «این صفحه پیدا نشد», one line «شاید نشانی را اشتباه وارد کرده‌ای.», one primary pill «بازگشت به خانه» → `/`. Alternatives: (b) the owner supplies the line; (c) keep Next's English default — **not** recommended, it breaks §D on that route and puts English text in front of a Persian-speaking user in distress-adjacent contexts.
- Q-09 (contrast) is unchanged and still blocks T-015; F-2 adds one more measurement to that file, not a new decision.

## Evidence files added by this review (`reports/senior/img/`)

| File | Shows |
|---|---|
| `senior-t002f-comparison.png` | wireframe W-01 · app W-01 light · app W-01 dark · wireframe W-01 dark |
| `senior-t002f-w01-light-390.png` / `senior-t002f-w01-dark-390.png` | W-01, both themes, 390×844 @2× |
| `senior-t002f-w01-light-360.png` / `senior-t002f-w01-dark-360.png` | 360 px, both themes (no overflow) |
| `senior-t002f-404-light.png` / `senior-t002f-404-dark.png` | F-1: injected off-palette `#fff` / `#000` 404 page |
| `senior-t002f-prehydration-dark-js-only.png` | stored-dark user, JS chunks blocked: correct «تم روشن» before hydration |
| `senior-t002f-focus-transient-cta.png` / `senior-t002f-focus-settled-cta.png` / `senior-t002f-focus-settled-cta-dark.png` | F-2: ring immediately after Tab vs settled, light and dark |

## Next orders

| Task | Branch | Start |
|---|---|---|
| T-003A consent API + log + server-side gate (+ N-1 envelope) | this session branch | after the owner's **تأیید** of the step plan |
| T-003B W-02 + `/terms` stub + `/chat` placeholder (+ F-1 `not-found.tsx` once Q-11 is answered, + F-2 one-line transition fix, + Q-07 interim 115 link if approved) | this session branch (same session, one task at a time) | after T-003A |
| T-004 compose integration + amendments a–d + carried Docker evidence | this session branch | after T-003A/T-003B **and Q-01** |
