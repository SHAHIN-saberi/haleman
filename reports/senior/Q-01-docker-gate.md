# Senior report — Step 0.2: Docker-capable gate (Q-01)

- Date: 2026-09-26 · Author: senior (solo-senior mode, §3 of the kickoff)
- Type: Step-0 decision item (no feature code). Owner's verdict in-session: "I have Docker myself — approved",
  i.e. option **(c) both**: an automated per-push gate *and* an independent owner spot-run at each milestone gate.
- Branch: `arena/01a0dcf9-haleman` · commit: `3726fa7` (workflow copy) + this commit.

## What this closes

B-01 has blocked every Docker gate since M0: `make up`, `make size`, runtime `make verify-ports`, in-image pytest
and the image-size budgets were **never produced** by any team sandbox — missing evidence, not passing evidence.
Q-01 asked for a runner. This step delivers it in two independent ways:

1. **GitHub Actions** (`.github/workflows/gates.yml`): free and unmetered for public repositories on standard
   runners — this repo is public and no minutes are billed. Runs the gate on every push.
2. **Owner spot-run**: `bash scripts/docker-gates.sh` runs the *identical* gate on a machine that has Docker.

Both call the same script, so the automated gate and the human spot-run cannot drift apart.

## What was built

| File | Purpose |
|---|---|
| `scripts/docker-gates.sh` | The gate itself: `verify-ports` (static) → `compose config` → `make build` → `make size` → `make up` → **runtime** published-port check → live wire smoke through Caddy → in-image pytest (activates with T-004's test stage) → M1 acceptance script (activates when T-004 lands it) → evidence collection + summary. Exit `0` green, `1` a gate failed, `2` **no Docker engine present** (explicitly MISSING evidence, never a pass). |
| `.github/gates.workflow.yml` | The workflow, kept **inert at this path** on purpose (see the permission note below). Thin wrapper: checkout → `bash scripts/docker-gates.sh` → step summary → artifact upload (30 days) → a second, `continue-on-error` job that reports `make check` until T-004 wires it. |
| `scripts/activate-ci-gate.sh` | One-command activation: copies the file to `.github/workflows/gates.yml`, prints the two git commands that finish the job. |
| `.gitignore` | `/reports/docker-gates/` — local evidence directories are never committed (they contain container logs). |

Design points worth review:

- **The gate is a script, not workflow YAML.** YAML-only gates cannot be run by a human with Docker, cannot be
  tested without a runner, and drift from what the owner runs. One script removes all three problems.
- **Runtime port check is stricter than `make verify-ports`.** `make verify-ports` reads the compose file
  (static). The script additionally parses `docker compose ps --format json` and fails unless exactly one
  container publishes a port **and** that container is `proxy`.
- **JSON bodies are parsed, not string-matched.** The first draft grepped `"is_new":false`; my stub test below
  proved that whitespace in a serialiser would have broken the gate. All body assertions now go through
  `json.load`.
- **No secrets in evidence.** The resolved `docker compose config` (which prints `POSTGRES_PASSWORD` and
  `DJANGO_SECRET_KEY`) is deliberately not collected; only `config --services` (names). A redaction pass then
  removes every `.env` value whose key looks like a secret from all collected artefacts.
- **Fail-closed language.** Anything that cannot run prints `MISSING: …` in those words, so the project rule
  ("missing evidence is never passing evidence") is enforced by the tooling.

## Evidence I produced (no Docker engine in this sandbox)

`docker: command not found` here, so I could not run the gate against real containers. Instead I built a stub
Docker CLI + a stub of the M1 API contract (§1 of `M1-orders-1.md`) **outside the repo** (`/tmp`) and exercised the
gate in six scenarios — three of them must fail:

```
PASS  ok: exit=0 as expected
        GATE: PASS
PASS  health-cookie: exit=1 as expected
        FAIL: health set a cookie (F9 violated)
PASS  no-resume: exit=1 as expected
        FAIL: resume broken (is_new not false)
PASS  two-ports: exit=1 as expected
        FAIL: published ports != 1
        FAIL: verify-ports
        FAIL: expected exactly ONE published port, found 2
        FAIL: runtime published ports != 1 (see above)
PASS  unhealthy: exit=1 as expected
        FAIL: not all services healthy (got 3/4)
PASS  dead-port: exit=1 as expected
        FAIL: GET / returned 000   (…and the summary is still written)
```

Green-path excerpt from the same harness (all gates green, MISSING items labelled):

```
OK: exactly one published port
ok  : verify-ports
ok  : compose config
ok  : make build
ok  : make size
ok  : 4 services healthy
published ports at runtime: [('proxy', '0.0.0.0', 8080, 80)]
OK: exactly one published port, owned by the proxy
ok  : html dir="rtl" · lang="fa" · Persian brand copy served
ok  : health body ok=true · health issued no cookie
ok  : anonymous=true · first visit is_new=true · device cookie issued
ok  : cookie HttpOnly · SameSite=Lax · Max-Age=31536000
ok  : resumed (is_new=false) · revisit issued no new cookie
MISSING: docker-compose.test.yml (T-004 adds the test stage) — in-image pytest NOT produced.
MISSING: scripts/m1-acceptance.sh (T-004) — the live smoke above covers today's subset.
api size:  250000000 bytes (budget 350000000)
web size:  150000000 bytes (budget 250000000)
GATE: PASS
```

Also verified: `bash -n` clean on both scripts; with no Docker present the gate exits **2** and prints
`MISSING: docker is not installed in this environment — this is MISSING evidence, not a pass.`

## Blocking finding: the session's GitHub App cannot create workflow files

Pushing the workflow was rejected:

```
! [remote rejected] arena/01a0dcf9-haleman -> arena/01a0dcf9-haleman (refusing to allow a GitHub App to create
  or update workflow `.github/workflows/gates.yml` without `workflows` permission)
error: failed to push some refs
```

The REST API gives the same answer (`403 Resource not accessible by integration`), and
`gh api repos/…/actions/permissions` is also 403 — the App's installation has no `workflows` permission and I
cannot grant it. Consequences and the workaround:

- The workflow content is therefore committed **inert** at `.github/gates.workflow.yml`.
- Either the owner runs `bash scripts/activate-ci-gate.sh` and pushes the two-line commit (a human push has full
  permission), or Arena's GitHub connection is re-granted with the `workflows` permission, after which I can
  activate it myself. **Until one of those happens, no CI run exists** — recorded as missing evidence, not as a
  passing gate.
- GitHub Actions itself appears enabled (no "Actions disabled" error anywhere; `actions/runs` is readable and
  returns 0 runs because no workflow file exists yet). The first real run will confirm it.

## Missing evidence (explicit, per project rule)

| Item | Status |
|---|---|
| A real `make up` / `make size` / runtime `make verify-ports` / live smoke against containers | **MISSING** — no Docker here; needs the owner's spot-run or the activated workflow. Nothing above should be read as those gates passing. |
| Web/api image sizes vs budget | **MISSING** (last estimate: web ≈148 MB, api unknown; both well inside budget by construction, but not measured). |
| In-image pytest, `scripts/m1-acceptance.sh` | **MISSING** by design — they activate in T-004 and the script says so. |

## Next orders / amendments

- **T-004 amendment (e):** add a `make gates` target → `bash scripts/docker-gates.sh`, and a README line
  ("Docker gate: `make gates` locally, Actions on every push"). T-004 owns `Makefile`/README, so it belongs there.
- **T-004 amendment (f):** once the workflow runs, delete `continue-on-error` from the `make-check` job and make
  `make check` the single entry gate (it can pass only when the test stage exists).
- **Owner action (one of):** `bash scripts/activate-ci-gate.sh` + push, **or** reconnect GitHub in Arena with the
  `workflows` permission.
- `reports/docker-gates/<sha>/summary.txt` is the artefact to hand back from any spot-run.
