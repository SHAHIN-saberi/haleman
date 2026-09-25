/**
 * Same-origin API client (worker-b lane, M1).
 *
 * Contract (binding, `reports/senior/M1-orders-1.md` §1):
 * - every route lives under `/api/` and ends with a trailing slash (never rely on
 *   Django's APPEND_SLASH 301 on POST);
 * - JSON only, the `hid` device cookie travels with `credentials: "include"`;
 * - error body is `{ code, detail }` → thrown as `ApiError`.
 *
 * M1 note: these are client-side calls only. The Next server has no route to the
 * public host (no rewrites/proxy), so screens call `/api/*` from the browser and
 * Caddy routes it to Django. Zero business logic here — transport + types only.
 */

const API_PREFIX = "/api";

export type ConsentState = {
  informed: boolean;
  version: string | null;
};

/** `GET /api/me/` — `consent` is added by T-003A, absent in T-001 builds. */
export type Me = {
  anonymous: boolean;
  is_new: boolean;
  consent?: ConsentState;
};

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;

  constructor(status: number, code: string, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

/** `/api/me` → `/api/me/`, keeping any query string intact. */
export function withTrailingSlash(path: string): string {
  const pathname = path.startsWith("/") ? path : `/${path}`;
  const queryAt = pathname.indexOf("?");
  const bare = queryAt === -1 ? pathname : pathname.slice(0, queryAt);
  const query = queryAt === -1 ? "" : pathname.slice(queryAt);
  return `${bare.endsWith("/") ? bare : `${bare}/`}${query}`;
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body !== undefined) headers.set("Content-Type", "application/json");

  const response = await fetch(`${API_PREFIX}${withTrailingSlash(path)}`, {
    ...init,
    headers,
    credentials: "include",
    cache: "no-store",
  });

  if (!response.ok) {
    const body: unknown = await response.json().catch(() => null);
    const error = body as { code?: unknown; detail?: unknown } | null;
    throw new ApiError(
      response.status,
      typeof error?.code === "string" ? error.code : "unknown_error",
      typeof error?.detail === "string" ? error.detail : `HTTP ${response.status}`,
    );
  }

  return (await response.json()) as T;
}

/** One round-trip to `/api/me/`: resumes the anonymous device or has one issued. */
export function getMe(): Promise<Me> {
  return apiFetch<Me>("/me/");
}

let meRequest: Promise<Me> | null = null;

/**
 * `getMe()` exactly once per page load (W-01 order §6), shared between callers
 * (React strict-mode double effects included). A failed call clears the cache so
 * a later mount can retry.
 */
export function getMeOnce(): Promise<Me> {
  if (meRequest === null) {
    meRequest = getMe().catch((error: unknown) => {
      meRequest = null;
      throw error;
    });
  }
  return meRequest;
}
