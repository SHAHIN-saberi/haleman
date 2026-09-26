# Senior report — Step 0.3: decisions + design debt (Q-02 … Q-11)

- Date: 2026-09-26 · Author: senior (solo-senior mode) · Step: 0.3 (no feature code)
- Owner verdicts: the decision table in the session was **approved** ("تایید"), and within it option **(a)** for the
  contrast set with one change I recommended and he accepted: **`--primary-bg` (dark) stays `#223041`** and the dark
  Soft-button label uses `--text` instead.
- Branch `arena/01a0dcf9-haleman` · files touched: `design/brand-kit/palette.md`, `design/brand-kit/theme-preview.html`,
  `design/design-system.md`, `product/wireframes/index.html` (colour values only), `frontend/styles/tokens.css`,
  `frontend/components/ui/Button.tsx`, `tech/technical-decisions.md`, `tech/questions.md`, `README.md`, `src/` (deleted),
  `STATUS.md`, this report (+ evidence PNGs).

## 1. What changed, and why

| Item | Decision | Files |
|---|---|---|
| Q-02 | Confirm D-S1: M0's boot/size proof closes at the end of T-004 | `STATUS.md` (D-S1 already recorded) |
| Q-03 | TD-05 → `backend/engine/scoring.py`; TD-06 → Django device token + authlib Google + own email OTP; TD-09 → server-side PDF in Django; duplicate "Standing rules" heading merged | `tech/technical-decisions.md` |
| Q-04 | Licence rule = permissive OSS (MIT/BSD/Apache-2.0/ISC) + LGPL used unmodified; no GPL/AGPL/SSPL/commercial | `tech/technical-decisions.md` |
| Q-05 | `node:22-alpine` for the web image (Node 20 EOL 2026-04-30) — applied by **T-004** | recorded here + T-004 board row |
| Q-06 | `backend/` + `frontend/` canonical; `src/` deleted; root README row removed | `README.md`, `src/` removed |
| Q-07 | Interim always-visible «تماس با اورژانس ۱۱۵» `tel:115` link on every route from **T-003B** until W-10 | ordered into T-003B |
| Q-08 | Keep the `/terms` stub + non-navigating W-01 link; **owner supplies the final legal text before launch** | recorded; re-raise at the launch gate |
| Q-09 | Palette **v1.1** contrast fix (see §2) | `palette.md`, `theme-preview.html`, `wireframes/index.html`, `tokens.css`, `design-system.md`, `Button.tsx` |
| Q-10 | Process order confirmed (verdict → merge), with the recorded pre-review merges as D-S8 | `tech/questions.md` |
| Q-11 | 404 copy approved → `app/not-found.tsx` (lands in T-003B) | ordered into T-003B |

No product copy changed: the wireframe edit is `--soft/--sage/--clay/--card` values only. W-01/W-02 strings remain
byte-identical (verified by `git diff` on the text nodes — see §4).

## 2. Palette v1.1 — the measured numbers

Four tokens moved **darker, same hue and saturation** (no colour became louder, nothing new was invented):

| Token | v1.0 | v1.1 | Why (worst pair it must pass) |
|---|---|---|---|
| light `--soft` | `#6E7989` | **`#626B7A`** | body/caption text on `--surface2` (4.53:1) and `--bg` (4.81:1) |
| light `--clay` | `#A9715B` | **`#8D5E4C`** | the **W-10 115 button**: cream text on clay is now 4.89:1 (was 3.61:1 — the worst pair in the palette) |
| light `--sage` | `#7A918D` | **`#5D6E6B`** | sage on `--sage-bg` (4.52:1) |
| dark `--card` | `#1D2530` | **`#1B232E`** | `--primary` (used as text in ghost buttons/links) on the card surface (4.51:1) |

Deliberately **not** changed: dark `--primary-bg` (`#223041`). Darkening it to carry `--primary` would drop the
surface-to-background separation from 1.29:1 to 1.09:1 and make the dark Soft button read as flat text. Instead the
dark Soft **label** uses `--text` (10.73:1 measured) while the light one keeps `--primary` (5.78:1). The rule is in
`design/design-system.md` with the reason, so it cannot be "fixed" back by accident.

### Before → after (WCAG 2.x, computed by me; `tech/tests.md` §D needs ≥ 4.5:1 for body text)

| Pair | v1.0 | v1.1 | |
|---|---|---|---|
| light `--soft` on `--bg` (W-01 subtitle) | 3.94 ✘ | **4.81 ✔** | |
| light `--soft` on `--card` | 4.30 ✘ | **5.24 ✔** | |
| light `--soft` on `--surface2` | 3.71 ✘ | **4.53 ✔** | |
| light `--on-primary` on `--clay` (**115 button**) | 3.61 ✘ | **4.89 ✔** | safety-critical |
| light `--clay` on `--clay-bg` | 3.33 ✘ | **4.51 ✔** | |
| light `--sage` on `--sage-bg` | 2.82 ✘ | **4.52 ✔** | |
| dark `--primary` on `--card` | 4.40 ✘ | **4.51 ✔** | |
| dark `--primary` on `--primary-bg` (Soft button) | 3.82 ✘ | **4.51 ✔** *(via `--text` label)* | keeps the surface soft |
| light `--text`/`--bg`, `--on-primary`/`--primary`, dark `--text`/`--card`, dark `--soft`/`--bg`, dark clay/sage pairs | 4.67–13.85 ✔ | 4.67–12.68 ✔ | unchanged or better |
| UI-only: light `--border` on `--bg` | 1.14 | 1.14 (unchanged) | see note |

**Border note (recorded, not silently dropped):** `--border` is a decorative hairline (1.14:1). Raising it to the
3:1 non-text minimum would need `#8A8C90`, which would make the whole UI look like a wireframe and contradict the
"soft, minimal" identity. Decision: keep the soft border and carry focus/affordance with the 2 px `--primary` focus
ring (6.31:1 light / 4.93:1 dark) and min-height-44 controls. If a stronger border is ever needed it is an owner call,
not an agent one.

### Measured in a real browser (not just arithmetic)

Built a throwaway page rendering the Soft and Primary buttons, then read the **computed** colours in Chromium 153:

```
light: theme=light
   soft    fg=rgb(61, 90, 128) bg=rgb(227, 233, 241)  contrast=5.78 (need >=4.5)
   primary fg=rgb(245, 242, 234) bg=rgb(61, 90, 128)  contrast=6.31
dark: theme=dark
   soft    fg=rgb(233, 230, 220) bg=rgb(34, 48, 65)  contrast=10.73 (need >=4.5)
   primary fg=rgb(21, 32, 48) bg=rgb(110, 140, 168)  contrast=4.67
light soft HOVER: fg=rgb(245, 242, 234) bg=rgb(51, 77, 110) contrast=7.73
dark soft HOVER: fg=rgb(21, 32, 48) bg=rgb(127, 154, 179) contrast=5.60
```

The dark-only rule was also checked at the **CSS** level, because `in-data-[theme=dark]:text-text` and
`focus-visible:outline-primary` are both single-class utilities — if Tailwind had emitted the dark rule *before*
`.text-primary`, colour would not win the cascade and the fix would silently do nothing:

```
.text-primary{color:var(--primary)}                                        pos = 6830
:where([data-theme=dark]) .in-data-\[theme\=dark\]\:text-text{color:var(--text)}          pos = 8237
:where([data-theme=dark]) .in-data-\[theme\=dark\]\:hover\:text-on-primary:hover{...}     pos = 8338
```

Source order decides at equal specificity → the utilities win, and the browser measurement above confirms it.

Evidence images: `reports/senior/img/palette-v11-{soft,primary}-{light,dark}.png` (button crops),
`palette-v11-probe-{light,dark}.png` (full probe screen) and `palette-v11-w01-{light,dark}.png` (the real W-01,
which shows the softened `--soft` on the subtitle/link and an unchanged CTA).

## 3. Gates after the change

| Gate | Result |
|---|---|
| `npm run check:tokens` | `OK: tokens 1:1 with palette.md, 17 files scanned, 0 stray hexes` — tokens.css ↔ palette.md row-for-row in both themes ✔ |
| `npm run lint` | exit 0 ✔ |
| `npm run typecheck` | exit 0 ✔ |
| `npm run build` | green (next build, 3 static pages) ✔ |
| browser | computed-contrast table above, both themes ✔ |
| backend | untouched by this step (last run: 19 passed, 95.25 %) |

## 4. Scope / safety notes

- **§C:** no prompt, engine, copy or API surface changed. The W-10 crisis button only got *more* legible (3.61 → 4.89).
  `<CrisisLayer/>` still mounted on every route.
- **Copy:** the wireframe file was edited for colour values only; the diff shows no text-node change. W-01/W-02 strings
  keep their ZWNJ characters.
- **§D:** RTL, both themes, tokens-only hexes (gate), 360 px (unchanged), keyboard (unchanged) — plus the contrast
  table now fully green for text pairs.

## 5. Still open / next

- **B-05 (owner action):** activate the CI workflow — `bash scripts/activate-ci-gate.sh` + push, or re-grant the Arena
  GitHub connection the `workflows` permission.
- **Q-08 reminder:** the final `/terms` legal text is owed by the owner before any public launch (recorded, launch gate).
- **T-003B carries three additions now:** Q-07 (interim 115 link), Q-11 (`app/not-found.tsx`), F-2 (focus-ring
  transition one-liner). Step 0.4 (retire the team roles in `AGENTS.md` / `tech/team.md` / `STATUS.md`) is the last
  Step-0 item.
