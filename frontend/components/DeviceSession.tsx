"use client";

import { useEffect } from "react";
import { getMeOnce } from "@/lib/api";

/**
 * DeviceSession — issues/resumes the anonymous device token (US-01/US-04).
 *
 * W-01 order §6: exactly one `GET /api/me/` on mount; this is the request that
 * makes the backend create the `AnonymousIdentity` row and set the `hid` cookie.
 * Any failure is swallowed — the screen must render regardless (M1 has no
 * backend on a standalone frontend build).
 *
 * No state is stored client-side: the server's cookie is the only source of truth.
 */
export default function DeviceSession() {
  useEffect(() => {
    getMeOnce().catch((error: unknown) => {
      if (process.env.NODE_ENV !== "production") {
        console.warn("[haleman] /api/me/ unavailable — anonymous session not started yet", error);
      }
    });
  }, []);

  return null;
}
