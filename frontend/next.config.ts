import type { NextConfig } from "next";

/**
 * Haleman web (worker-b lane) — standalone output keeps the image ≤ 250 MB
 * (contract: docker/Dockerfile.frontend, tech/technical-decisions.md TD-13).
 */
const nextConfig: NextConfig = {
  output: "standalone",
  reactStrictMode: true,
  poweredByHeader: false,
  // Decision D-S6: every `/api/*` path is called WITH its trailing slash and must
  // never be rewritten. In the compose stack Caddy routes `/api/*` to Django first,
  // but when Next serves these paths itself (`next dev`, standalone preview) its
  // default is a 308 that strips the slash — so it is disabled here.
  skipTrailingSlashRedirect: true,
  // The frontend talks to the backend only through same-origin `/api/*`
  // (Caddy proxy, M1-orders-1.md §1). No rewrites, no CORS, no third-party origins.
  //
  // Dev-only escape hatch for proxied preview hosts (`next dev` blocks
  // cross-origin /_next/* requests). Unused in production builds.
  allowedDevOrigins: (process.env.ALLOWED_DEV_ORIGINS ?? "")
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean),
};

export default nextConfig;
