# Design System — Haleman Web (v1.0)

Source of truth for color: `design/brand-kit/palette.md` (v1.1) (+ `theme-preview.html`).
This file maps tokens to code + components.

> v1.1 (2026-09-26): four tokens moved slightly darker so every text/surface pair meets
> `tech/tests.md` §D (>= 4.5:1). Hue and saturation unchanged — no colour became louder.
> light `--soft #626B7A`, `--clay #8D5E4C`, `--sage #5D6E6B`; dark `--card #1B232E`.
> `--primary-bg` (dark) deliberately kept `#223041`; instead the dark **Soft** button label
> uses `--text` (10.4:1) while the light one keeps `--primary` (5.78:1). Evidence:
> `reports/senior/step-0.3-decisions.md`.

## Tokens → CSS

Implement as CSS vars on `:root[data-theme="light"|"dark"]`: `--bg --card --surface2
--text --soft --border --primary --primary-h --on-primary --primary-bg --sage --sage-bg
--clay --clay-bg --shadow`. Persist theme in `localStorage`, default: system.

Tailwind: extend theme to reference the vars (e.g. `bg-card`, `text-soft`,
`bg-primary`) so both themes work with zero conditional classes.

## Typography (Vazirmatn, self-hosted from `brand-kit/fonts/`)

- Display/brand 26 Bold · H1 22 Bold · H2 17 Bold · Body 13.5–14 Regular · Caption 12
  (soft color) · Line-height 2.0 for chat/political-readability, 1.8 elsewhere.

## Components (anatomy + states)

- **Button**: pill radius 999, Primary filled / Ghost (1.5px primary border) / Soft
  (`--primary-bg` fill); hover → `primary-h`; disabled 40% opacity. Min height 44px.
  **Soft label colour:** light `--primary` (5.78:1 on `--primary-bg`), dark `--text`
  (10.4:1) via `in-data-[theme=dark]:text-text` — see the v1.1 note above. Hover goes to
  `primary-h` + `on-primary` in both themes (7.73:1 light, 5.60:1 dark).
- **Chips** (quick replies / filters): pill, primary border+text; `.on` = primary fill.
- **Bubble**: bot = card bg + border, radius 16 (4px at tail); user = primary fill +
  on-primary text. Max-width 88%.
- **Card/Box**: card bg + border, radius 12–14; `.sage` / `.clay` variants for
  positive / crisis meanings only.
- **Input**: pill field + pill Send; field = bg + border; Send = primary.
- **Progress**: 8px track (surface2) + primary fill, radius 99.
- **DocCard** (therapist): name + specialty + license badge (sage ✓) + Call/Book buttons.
- **TrendChart**: CSS bars, primary-border + primary-bg fill.
- **Overlay** (crisis): full-screen card, clay box + clay Call-115 button + ghost "I'm safe".
- **ThemeToggle**: pill button, primary.

## Rules

- Radius: bubbles/cards 14–18px; buttons/chips pill. Shadows: `--shadow` only, never harsh.
- 60-30-10: neutrals / surface-2 / primary; sage+clay for meaning only.
- No gradients, no vivid colors, no pure black/white surfaces.
- Spacing scale 4/8/12/16/24; phone frame max-width 480px centered on desktop.
