#!/bin/sh
# Backend gate — runs INSIDE the api test image (`make test-backend`), working dir /app.
#
# One definition, used by both `make check` and `scripts/docker-gates.sh`, so the local
# gate and the CI gate can never drift apart (D-S12).
#
# Gates: ruff clean · pytest green · coverage >= 80 % · engine coverage >= 90 % once
# `engine/` holds real modules (M2/T-009). Any failure exits non-zero.
set -eu

echo "=== ruff check . ==="
ruff check .

echo "=== pytest (coverage gate: backend >= 80 %) ==="
python -m pytest -q --cov=. --cov-fail-under=80 --cov-report=term-missing

engine_modules=$(find engine -name '*.py' ! -name '__init__.py' 2>/dev/null | wc -l | tr -d ' ')
if [ "$engine_modules" -gt 0 ]; then
  echo "=== engine coverage gate: engine/ has ${engine_modules} module(s) -> >= 90 % ==="
  python -m coverage report --include='engine/*' --fail-under=90
else
  echo "NOTE: engine/ has no modules yet, so the >= 90 % engine gate is dormant"
  echo "      (it activates with the first engine module, M2/T-009)."
fi

echo "OK: backend gate green"
