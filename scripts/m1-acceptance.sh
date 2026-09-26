#!/usr/bin/env bash
# Haleman M1 acceptance (T-004 §4) — the six checks of the milestone exit criterion,
# driven through the ONE published port exactly as a browser does (Caddy -> api/web).
#
#   APP_PORT=8080 bash scripts/m1-acceptance.sh        # against a running stack
#   make acceptance                                    # same, reads APP_PORT from .env
#
# Exit codes: 0 = every check passed · 1 = a check FAILED (details printed) ·
# 2 = no stack reachable at $BASE — MISSING evidence, never a pass (D-S12).
#
# It talks HTTP only: no docker command, no database access, no source inspection.
# Bodies are parsed as JSON (`jget`) instead of string-matched, so a serialiser that
# reorders keys cannot make this gate lie in either direction.

set -uo pipefail

cd "$(dirname "$0")/.."

if [ -z "${APP_PORT:-}" ]; then
  APP_PORT=$(grep -E '^APP_PORT=' .env 2>/dev/null | head -1 | cut -d= -f2 | tr -d ' \r')
  APP_PORT="${APP_PORT:-80}"
fi
BASE="${BASE:-http://localhost:${APP_PORT}}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
JAR="$TMP/cookies.txt"

PASS=0
FAIL=0
ok() { printf 'ok   %s\n' "$1"; PASS=$((PASS + 1)); }
bad() { printf 'FAIL %s\n' "$1"; FAIL=$((FAIL + 1)); }
check() { # check <label> <expected> <actual>
  if [ "$2" = "$3" ]; then ok "$1 ($3)"; else bad "$1 — expected $2, got $3"; fi
}

jget() { # jget <file> <key> [dotted.path]
  python3 - "$1" "$2" <<'PY'
import json, sys
try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    print("<unparseable>")
    sys.exit(0)
for part in sys.argv[2].split("."):
    if isinstance(data, dict) and part in data:
        data = data[part]
    else:
        print("<missing>")
        sys.exit(0)
print(data)
PY
}

fetch() { # fetch <name> <url> [curl args...] -> status code (000 if unreachable)
  local name="$1" url="$2"; shift 2
  local code
  code=$(curl -sS -m 15 -D "$TMP/$name.h" -o "$TMP/$name.body" -w '%{http_code}' "$@" "$url" 2>/dev/null)
  printf '%s' "${code:-000}"
}

echo "M1 acceptance — base: $BASE"
echo

# ---------------------------------------------------------------- preflight
code=$(fetch health "$BASE/api/health/")
if [ "$code" = "000" ]; then
  echo "MISSING: nothing answers at $BASE (is the stack up? try \`make up\`)."
  echo "         No check was performed — this is MISSING evidence, not a pass (exit 2)."
  exit 2
fi

# ---------------------------------------------------------------- 1. shell serves
code=$(fetch index "$BASE/")
check "GET / -> 200" "200" "$code"
if grep -qi 'dir="rtl"' "$TMP/index.body"; then ok 'html carries dir="rtl"'; else bad 'html does not carry dir="rtl"'; fi

# ------------------------------------------- 2. health: healthy and identity-free
code=$(fetch health2 "$BASE/api/health/")
check "GET /api/health/ -> 200" "200" "$code"
check "health body ok=true" "True" "$(jget "$TMP/health2.body" ok)"
if grep -qi '^set-cookie' "$TMP/health2.h"; then bad "health issued a cookie (identity-free endpoint)"; else ok "health issued no cookie"; fi

# ------------------------------- 3. anonymous device token on the first visit
code=$(fetch me1 "$BASE/api/me/" -c "$JAR")
check "GET /api/me/ (first visit) -> 200" "200" "$code"
check "anonymous=true" "True" "$(jget "$TMP/me1.body" anonymous)"
check "is_new=true" "True" "$(jget "$TMP/me1.body" is_new)"
check "consent.informed=false before accepting" "False" "$(jget "$TMP/me1.body" consent.informed)"
if grep -qi '^set-cookie:.*hid=' "$TMP/me1.h"; then ok "device cookie issued"; else bad "no hid cookie issued"; fi
if grep -qi 'HttpOnly' "$TMP/me1.h"; then ok "cookie is HttpOnly"; else bad "cookie is not HttpOnly"; fi
if grep -qi 'SameSite=Lax' "$TMP/me1.h"; then ok "cookie is SameSite=Lax"; else bad "cookie is not SameSite=Lax"; fi
if grep -qi 'Max-Age=31536000' "$TMP/me1.h"; then ok "cookie Max-Age=31536000"; else bad "cookie Max-Age is wrong"; fi

# ------------------------------------------- 4. the chat gate must refuse first
code=$(fetch chat1 "$BASE/api/chat/" -b "$JAR")
check "GET /api/chat/ without consent -> 403" "403" "$code"
check "error code=consent_required" "consent_required" "$(jget "$TMP/chat1.body" code)"

# ------------------------------------------------- 5. accepting consent writes it
code=$(fetch consent "$BASE/api/consent/" -b "$JAR" -H 'Content-Type: application/json' \
  -d '{"kind":"informed","version":"v1"}')
check "POST /api/consent/ -> 201" "201" "$code"
check "consent echo kind=informed" "informed" "$(jget "$TMP/consent.body" kind)"
check "consent echo version=v1" "v1" "$(jget "$TMP/consent.body" version)"

# ------------------------------------------------- 6. the gate opens, the device resumes
code=$(fetch chat2 "$BASE/api/chat/" -b "$JAR")
check "GET /api/chat/ with consent -> 200" "200" "$code"
check "chat placeholder body" "True" "$(jget "$TMP/chat2.body" placeholder)"
code=$(fetch me2 "$BASE/api/me/" -b "$JAR")
check "GET /api/me/ (returning) -> 200" "200" "$code"
check "is_new=false on the second visit" "False" "$(jget "$TMP/me2.body" is_new)"
check "consent.informed=true after accepting" "True" "$(jget "$TMP/me2.body" consent.informed)"

# ---------------------------------------------------------------- verdict
echo
if [ "$FAIL" -eq 0 ]; then
  echo "M1 ACCEPTANCE: PASS ($PASS checks)"
  exit 0
fi
echo "M1 ACCEPTANCE: FAIL ($PASS passed, $FAIL failed)"
exit 1
