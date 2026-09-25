# Haleman supervisor shortcuts
.PHONY: env up down logs ps build check verify-ports size test-backend test-smoke migrate seed shell

# Create local configuration once; never overwrite an existing .env.
env:
	test -f .env || cp .env.example .env

up: env ## boot full stack (one port)
	docker compose up -d --build
down: ## stop stack
	docker compose down
logs:
	docker compose logs -f
ps:
	docker compose ps
build: env
	docker compose build
check: env ## full gate: backend tests + frontend build (add lint/type as configured)
	docker compose run --rm api sh -c "python -m pytest -q"
	cd frontend && npm run build
verify-ports: env ## fail unless exactly ONE published port exists
	@test $$(docker compose config --format json | python3 -c "import json,sys; print(sum(len(s.get('ports',[]) or []) for s in json.load(sys.stdin)['services'].values()))") = "1" && echo "OK: exactly one published port" || (echo "FAIL: published ports != 1"; exit 1)
size: env ## enforce backend<=350MB and frontend<=250MB
	@command -v docker >/dev/null 2>&1 || { echo "FAIL: docker is required"; exit 1; }; \
	for image in haleman-api haleman-web; do \
		size=$$(docker image inspect -f '{{.Size}}' $$image 2>/dev/null) || { echo "FAIL: image $$image is missing"; exit 1; }; \
		mb=$$(python3 -c "print(round(int('$$size') / 1000000, 2))"); \
		echo "$$image: $${mb} MB"; \
		limit=350000000; test "$$image" = haleman-web && limit=250000000; \
		test "$$size" -le "$$limit" || { echo "FAIL: $$image exceeds $${limit} bytes"; exit 1; }; \
	done
	echo "OK: image sizes within budgets"
test-backend: env
	docker compose run --rm api python -m pytest -q --cov=. --cov-report=term-missing
test-smoke: ## playwright smoke (needs frontend/ configured)
	cd frontend && npm run test:smoke
migrate: env
	docker compose run --rm api python manage.py migrate
seed: env
	docker compose run --rm api python manage.py seed_therapists
shell: env
	docker compose run --rm api python manage.py shell
