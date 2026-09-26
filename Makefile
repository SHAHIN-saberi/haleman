# Haleman — supervisor shortcuts. Single entry gate: `make check`.
#
# Exit codes follow D-S12: 0 = every gate green · 1 = a gate FAILED ·
# 2 = this environment cannot produce the evidence (no Docker) — MISSING, never a pass.
SHELL := /bin/bash
.PHONY: env require-docker up down logs ps build check test-backend verify-ports size \
        acceptance migrate seed shell

# Create local configuration once. `scripts/init-env.py` fills the two secrets with
# fresh random values (T-004 amendment c); an existing .env is never overwritten.
env:
	@test -f .env || python3 scripts/init-env.py

# Every Docker target goes through here, so a missing engine is reported as MISSING
# evidence (exit 2) instead of a confusing "command not found".
require-docker:
	@command -v docker >/dev/null 2>&1 || { \
		echo "MISSING: docker is not available in this environment."; \
		echo "         Nothing was verified — this is MISSING evidence, not a pass (exit 2)."; \
		exit 2; }

up: env require-docker ## boot the full stack (only Caddy publishes a port)
	docker compose up -d --build
down: require-docker ## stop the stack
	docker compose down
logs: require-docker ## follow stack logs
	docker compose logs -f
ps: require-docker ## service status + health
	docker compose ps
build: env require-docker ## build both production images
	docker compose build

check: env require-docker ## THE gate: images + backend (ruff, pytest, coverage) + frontend + one port
	docker compose build
	docker compose -f docker-compose.yml -f docker-compose.test.yml build api
	$(MAKE) test-backend
	cd frontend && npm ci --no-audit --no-fund && npm run lint && npm run typecheck \
		&& npm run check:tokens && npm run build
	$(MAKE) verify-ports
	@echo "OK: make check green"

test-backend: env require-docker ## backend gate in the test image (ruff + pytest + coverage), real Postgres
	docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm api sh scripts/backend-gate.sh

verify-ports: env require-docker ## fail unless exactly ONE published port exists (static, from compose)
	@test $$(docker compose config --format json | python3 -c "import json,sys; print(sum(len(s.get('ports',[]) or []) for s in json.load(sys.stdin)['services'].values()))") = "1" && echo "OK: exactly one published port" || (echo "FAIL: published ports != 1"; exit 1)

size: env require-docker ## enforce api<=350MB and web<=250MB (fails closed)
	@for image in haleman-api haleman-web; do \
		size=$$(docker image inspect -f '{{.Size}}' $$image 2>/dev/null) || { echo "FAIL: image $$image is missing — run make build first"; exit 1; }; \
		mb=$$(python3 -c "print(round(int('$$size') / 1000000, 2))"); \
		echo "$$image: $${mb} MB"; \
		limit=350000000; test "$$image" = haleman-web && limit=250000000; \
		test "$$size" -le "$$limit" || { echo "FAIL: $$image exceeds $${limit} bytes"; exit 1; }; \
	done
	@echo "OK: image sizes within budgets"

acceptance: env ## M1 acceptance through the published port (stack must be up)
	bash scripts/m1-acceptance.sh

migrate: env require-docker ## apply migrations against the compose database
	docker compose run --rm api python manage.py migrate
seed: env require-docker ## seed therapists (needs T-019 data)
	docker compose run --rm api python manage.py seed_therapists
shell: env require-docker ## Django shell in the api image
	docker compose run --rm api python manage.py shell
