# Haleman supervisor shortcuts
.PHONY: up down logs ps build check verify-ports size test-backend test-smoke migrate seed shell

up: ## boot full stack (one port)
	docker compose up -d --build
down: ## stop stack
	docker compose down
logs: ## follow logs
	docker compose logs -f
ps:
	docker compose ps
build:
	docker compose build
check: ## full gate: backend tests + frontend build (add lint/type as configured)
	docker compose run --rm api sh -c "python -m pytest -q"
	cd frontend && npm run build
verify-ports: ## fail unless exactly ONE published port exists
	@test $$(docker compose config --format json | python3 -c "import json,sys; print(sum(len(s.get('ports',[]) or []) for s in json.load(sys.stdin)['services'].values()))") = "1" && echo "OK: exactly one published port" || (echo "FAIL: published ports != 1"; exit 1)
size: ## show image sizes vs budgets (backend<=350MB, frontend<=250MB)
	@docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}' | grep -E 'haleman|REPOSITORY' || docker images | head -20
test-backend:
	docker compose run --rm api python -m pytest -q --cov=. --cov-report=term-missing
test-smoke: ## playwright smoke (needs frontend/ configured)
	cd frontend && npm run test:smoke
migrate:
	docker compose run --rm api python manage.py migrate
seed:
	docker compose run --rm api python manage.py seed_therapists
shell:
	docker compose run --rm api python manage.py shell
