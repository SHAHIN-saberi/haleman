#!/usr/bin/env bash
# Haleman — Docker gate (Q-01). Produces the evidence NO team sandbox can produce.
#
#   bash scripts/docker-gates.sh
#
# Runs the real deploy unit end to end and writes every raw output to
#   ${GATE_OUT:-reports/docker-gates/<short-sha>}/
# Exit codes:  0 = every gate green · 1 = a gate FAILED · 2 = environment missing (Docker absent),
# which is MISSING evidence, never a pass.
#
# Gates, in order (each one prints its exact command and raw output):
#   1. one published port        make verify-ports      (static, compose config)
#   2. both images build         make build
#   3. image budgets             make size              (api <= 350 MB, web <= 250 MB, fails closed)
#   4. stack boots healthy       make up + docker compose ps
#   5. one port AT RUNTIME       parsed from `docker compose ps --format json` (strict)
#   6. live wire smoke           curl through Caddy on the published port
#   7. in-image pytest           only when the T-004 test stage exists, else MISSING
#   8. M1 acceptance script      only when T-004 lands it, else MISSING
#
# The CI wrapper (.github/gates.workflow.yml) calls this same script, so the local
# spot-run and the automated gate can never drift apart.

set -euo pipefail

cd "$(dirname "$0")/.."

SHA=$(git rev-parse --short HEAD 2>/dev/null || echo nogit)
OUT="${GATE_OUT:-reports/docker-gates/${SHA}}"
mkdir -p "$OUT"
LOG="$OUT/gate.log"
: > "$LOG"

# Every line of this run lands in gate.log and on stdout.
exec > >(tee -a "$LOG") 2>&1

FAILED=()
step() { printf '\n=== %s ===\n' "$*"; }
fail() { FAILED+=("$1"); printf 'FAIL: %s\n' "$1"; }
ok() { printf 'ok  : %s\n' "$1"; }

if ! command -v docker >/dev/null 2>&1; then
  printf 'MISSING: docker is not installed in this environment — this is MISSING evidence, not a pass.\n'
  printf '(Exit 2 so nobody mistakes it for a green gate.)\n'
  exit 2
fi

step "environment"
date -u '+%Y-%m-%dT%H:%M:%SZ'
echo "repo:   $(pwd)"
echo "commit: $(git log -1 --format='%h %s' 2>/dev/null || echo n/a)"
docker version
docker compose version
python3 --version
node --version 2>/dev/null || echo "node: n/a"

step "make env (never overwrites an existing .env)"
make env
# The published port: an explicit APP_PORT in the environment wins (compose gives shell
# env precedence over .env), otherwise take it from .env, otherwise 80.
if [ -n "${APP_PORT:-}" ]; then
  echo "APP_PORT from environment: $APP_PORT"
else
  APP_PORT=$(grep -E '^APP_PORT=' .env | head -1 | cut -d= -f2 | tr -d ' \r' || true)
  APP_PORT="${APP_PORT:-80}"
  export APP_PORT
  echo "APP_PORT from .env: $APP_PORT"
fi
BASE="http://localhost:${APP_PORT}"

step "1/8 one published port (static): make verify-ports"
make verify-ports && ok "verify-ports" || fail "verify-ports"

step "compose config validation"
docker compose config -q && ok "compose config" || fail "compose config"

step "2/8 build both images: make build"
make build && ok "make build" || fail "make build"

step "3/8 image budgets: make size"
docker images | grep -E 'REPOSITORY|haleman' || true
make size && ok "make size" || fail "make size"
for image in haleman-api haleman-web; do
  size=$(docker image inspect -f '{{.Size}}' "$image" 2>/dev/null || echo "?")
  echo "$image = $size bytes"
done

step "4/8 boot the stack: make up"
make up || true
docker compose ps || true
healthy=0
for i in $(seq 1 60); do
  healthy=$(docker compose ps --format json 2>/dev/null | grep -c '"Health":"healthy"' || true)
  echo "attempt $i/60: healthy services = ${healthy}/4"
  [ "$healthy" -ge 4 ] && break
  sleep 5
done
docker compose ps
docker compose ps --format json > "$OUT/compose-ps.json" 2>/dev/null || true
[ "$healthy" -ge 4 ] && ok "4 services healthy" || fail "not all services healthy (got ${healthy}/4)"

step "5/8 one published port AT RUNTIME (strict)"
python3 - "$OUT/compose-ps.json" <<'PY' || fail "runtime published ports != 1 (see above)"
import json, sys
path = sys.argv[1]
published = []
for line in open(path, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    try:
        svc = json.loads(line)
    except json.JSONDecodeError:
        continue
    for p in svc.get("Publishers") or []:
        if p.get("PublishedPort"):
            published.append((svc.get("Service"), p.get("URL"), p.get("PublishedPort"), p.get("TargetPort")))
print("published ports at runtime:", published)
if len(published) != 1:
    sys.exit("FAIL: expected exactly ONE published port, found %d" % len(published))
if published[0][0] != "proxy":
    sys.exit("FAIL: the single published port belongs to %r, not the proxy" % (published[0][0],))
print("OK: exactly one published port, owned by the proxy")
PY

step "6/8 live wire smoke through Caddy on ${BASE}"
jar="$OUT/cookies.txt"
rm -f "$jar"

# Bodies are parsed as JSON, never string-matched: the gate must not depend on
# whitespace or key order of the serialiser.
jget() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2]))' "$1" "$2" 2>/dev/null || echo "<unparseable>"; }
# fetch <name> <url> [curl args...]  -> prints the status code, always (000 if the port is dead)
fetch() {
  local name="$1" url="$2"; shift 2
  local code
  code=$(curl -sS -D "$OUT/$name.h" -o "$OUT/$name.body" -w '%{http_code}' "$@" "$url" 2>/dev/null) || true
  printf '%s' "${code:-000}"
}

echo "--- GET / ---"
code=$(fetch index "$BASE/")
echo "status=$code"
[ "$code" = "200" ] || fail "GET / returned $code"
grep -qi 'dir="rtl"' "$OUT/index.body" && ok 'html dir="rtl"' || fail 'missing dir="rtl"'
grep -qi 'lang="fa"' "$OUT/index.body" && ok 'html lang="fa"' || fail 'missing lang="fa"'
grep -q 'حال' "$OUT/index.body" && ok 'Persian brand copy served' || fail 'brand copy missing'

echo "--- GET /api/health/ (must never issue a cookie) ---"
code=$(fetch health "$BASE/api/health/")
echo "status=$code"; [ -f "$OUT/health.body" ] && cat "$OUT/health.body"; echo
[ "$code" = "200" ] || fail "health returned $code"
[ "$(jget "$OUT/health.body" ok)" = "True" ] && ok 'health body ok=true' || fail 'health body is not {"ok": true}'
if grep -qi '^set-cookie' "$OUT/health.h"; then fail "health set a cookie (F9 violated)"; else ok 'health issued no cookie'; fi

echo "--- GET /api/me/ (issues the anonymous device cookie) ---"
code=$(fetch me1 "$BASE/api/me/" -c "$jar")
echo "status=$code"; [ -f "$OUT/me1.body" ] && cat "$OUT/me1.body"; echo
[ "$code" = "200" ] || fail "first /api/me/ returned $code"
[ "$(jget "$OUT/me1.body" anonymous)" = "True" ] && ok 'anonymous=true' || fail 'anonymous flag missing'
[ "$(jget "$OUT/me1.body" is_new)" = "True" ] && ok 'first visit is_new=true' || fail 'first visit did not report is_new=true'
grep -qi '^set-cookie:.*hid=' "$OUT/me1.h" && ok 'device cookie issued' || fail 'no hid cookie issued'
grep -qi 'HttpOnly' "$OUT/me1.h" && ok 'cookie HttpOnly' || fail 'cookie not HttpOnly'
grep -qi 'SameSite=Lax' "$OUT/me1.h" && ok 'cookie SameSite=Lax' || fail 'cookie not SameSite=Lax'
grep -qi 'Max-Age=31536000' "$OUT/me1.h" && ok 'cookie Max-Age=31536000' || fail 'cookie Max-Age wrong'

echo "--- GET /api/me/ again with the cookie (must resume) ---"
code=$(fetch me2 "$BASE/api/me/" -b "$jar")
echo "status=$code"; [ -f "$OUT/me2.body" ] && cat "$OUT/me2.body"; echo
[ "$code" = "200" ] || fail "second /api/me/ returned $code"
[ "$(jget "$OUT/me2.body" is_new)" = "False" ] && ok 'resumed (is_new=false)' || fail 'resume broken (is_new not false)'
if grep -qi '^set-cookie' "$OUT/me2.h"; then fail "revisit re-issued a cookie"; else ok 'revisit issued no new cookie'; fi

echo "--- probe /api/chat/ (INFO; 403 consent_required only after T-003A, 404 before) ---"
code=$(fetch chat "$BASE/api/chat/" -b "$jar")
echo "status=$code body=$([ -f "$OUT/chat.body" ] && cat "$OUT/chat.body" || echo "(no body)")"

step "7/8 in-image pytest (activates with the T-004 test stage)"
if [ -f docker-compose.test.yml ]; then
  docker compose -f docker-compose.yml -f docker-compose.test.yml build api \
    && docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm api sh -c \
       'python -m pytest -q --cov=. --cov-fail-under=80' \
    && ok "in-image pytest" || fail "in-image pytest"
else
  echo "MISSING: docker-compose.test.yml (T-004 adds the test stage) — in-image pytest NOT produced."
fi

step "8/8 M1 acceptance script (activates when T-004 lands it)"
if [ -f scripts/m1-acceptance.sh ]; then
  APP_PORT="$APP_PORT" bash scripts/m1-acceptance.sh && ok "m1-acceptance" || fail "m1-acceptance"
else
  echo "MISSING: scripts/m1-acceptance.sh (T-004) — the live smoke above covers today's subset."
fi

step "collecting evidence"
# `docker compose config` (resolved) is deliberately NOT collected: it prints every env
# value, including POSTGRES_PASSWORD and DJANGO_SECRET_KEY. Names only.
docker compose config --services > "$OUT/services.txt" 2>&1 || true
docker compose ps > "$OUT/ps.txt" 2>&1 || true
docker compose logs --no-color --tail=600 > "$OUT/compose.log" 2>&1 || true
docker images > "$OUT/images.txt" 2>&1 || true
for image in haleman-api haleman-web; do
  docker image inspect "$image" > "$OUT/image-$(echo "$image" | cut -d- -f2).json" 2>/dev/null || true
done

# Redact any secret that appears in .env from every collected artefact (§7 git hygiene).
python3 - "$OUT" .env <<'PY' || true
import os, pathlib, sys
out, envfile = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
secrets = []
if envfile.exists():
    for line in envfile.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 8 and any(k in key.upper() for k in ("PASSWORD", "SECRET", "KEY", "PASS", "TOKEN")):
            secrets.append(value)
redacted = 0
for path in out.rglob("*"):
    if not path.is_file() or path.suffix == ".png":
        continue
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        continue
    original = text
    for value in secrets:
        text = text.replace(value, "***REDACTED***")
    if text != original:
        path.write_text(text, encoding="utf-8")
        redacted += 1
print(f"redaction: values hidden = {len(secrets)}, files rewritten = {redacted}")
PY

docker compose down > "$OUT/down.txt" 2>&1 || true

step "summary"
{
  echo "commit:    $(git log -1 --format='%h %s' 2>/dev/null || echo n/a)"
  echo "when:      $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "runner:    $(uname -sm)"
  echo "app port:  $APP_PORT"
  echo "api size:  $(docker image inspect -f '{{.Size}}' haleman-api 2>/dev/null || echo '?') bytes (budget 350000000)"
  echo "web size:  $(docker image inspect -f '{{.Size}}' haleman-web 2>/dev/null || echo '?') bytes (budget 250000000)"
  echo "evidence:  $OUT"
  echo
  if [ "${#FAILED[@]}" -eq 0 ]; then
    echo "GATE: PASS"
  else
    echo "GATE: FAIL"
    for f in "${FAILED[@]}"; do echo "  - $f"; done
  fi
  echo
  echo "Evidence directory: $OUT"
  echo "Hand it back: paste the block above (and $OUT/summary.txt) into the report/STATUS."
} | tee "$OUT/summary.txt"

[ "${#FAILED[@]}" -eq 0 ] || exit 1
