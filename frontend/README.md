# frontend/ — Next.js contract (frontend lane, solo senior)

Build here per `tech/tasks.md` (T-002 first). Must satisfy `../docker/Dockerfile.frontend`
contract: `package.json`, `next.config` with `output: 'standalone'`, `npm run build` green.

## Required setup

- Next.js App Router + TypeScript strict + Tailwind. `lang=fa dir=rtl` on `<html>`.
- Tokens: `styles/tokens.css` copied 1:1 from `../design/brand-kit/palette.md`
  (`[data-theme]` vars); `<ThemeToggle/>` persisted, default system.
- Fonts: copy `../design/brand-kit/fonts/*.ttf` to `public/fonts/` (T-002), self-hosted.
- API client `lib/api.ts`: `credentials: 'include'`, base = same origin (`/api/*` via proxy).
- Routes mirror wireframe: `/` (W-01) `/consent` (W-02) `/chat` (W-03) `/result` (W-04)
  `/calm` (W-05) `/login` (W-06) `/doctors` (W-07) `/summary` (W-08) `/me` (W-09);
  crisis overlay component mounted on every route.

## Environment

- `ALLOWED_DEV_ORIGINS` (**dev-only**, optional): comma-separated hostnames `next dev` accepts for
  cross-origin `/_next/*` requests, e.g. a proxied preview host. Read in `next.config.ts`; ignored by
  `next build` / the standalone server, never set in `.env.example`, compose or production.

## Rules

- No business logic in components — every screen works through `/api/*`.
- Components per `../design/design-system.md`; Persian digits + Jalali in UI.
- `npm run test:smoke` (Playwright, 5 paths from `tech/tests.md`) must exist by M4.
