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
  // T-002F(1): no image optimisation at runtime. The app ships no raster images
  // through `next/image`, and `sharp` + `@img/sharp-libvips-*` (LGPL-3.0, ~46 MB)
  // would otherwise be traced into `.next/standalone`. `unoptimized` makes any
  // future `next/image` serve the original file; the excludes keep the native
  // binaries out of the standalone runtime (and so out of the web image).
  images: { unoptimized: true },
  outputFileTracingExcludes: {
    "*": ["**/node_modules/sharp/**/*", "**/node_modules/@img/**/*"],
  },
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
