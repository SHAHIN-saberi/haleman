#!/usr/bin/env bash
# Activate the Docker gate workflow (Q-01).
#
# Why this exists: the Arena GitHub App token used by the build session may not create
# files under `.github/workflows/` ("refusing to allow a GitHub App to create or update
# workflow ... without `workflows` permission"). A human push from the repository owner
# has no such limit, so this script does the copy and prints the two commands to finish.
#
#   bash scripts/activate-ci-gate.sh
#
set -euo pipefail

cd "$(dirname "$0")/.."

SRC=".github/gates.workflow.yml"
DST=".github/workflows/gates.yml"

test -f "$SRC" || { echo "FAIL: $SRC is missing"; exit 1; }

mkdir -p .github/workflows
if [ -f "$DST" ]; then
  if cmp -s "$SRC" "$DST"; then
    echo "$DST is already up to date with $SRC"
  else
    echo "$DST exists and differs from $SRC — diff:"
    diff -u "$DST" "$SRC" || true
    echo
    echo "Not overwriting. Review the diff, then copy manually if you agree."
    exit 1
  fi
else
  cp "$SRC" "$DST"
  echo "created $DST"
fi

cat <<'EOF'

Finish with (this push must come from a human account — that is the only reason
the build session cannot do it):

  git add .github/workflows/gates.yml
  git commit -m "ci: activate the Docker gate workflow (Q-01)"
  git push

Then open the Actions tab: every push runs
  make verify-ports -> make build -> make size -> make up -> runtime port check ->
  live smoke -> in-image pytest (once T-004 adds the test stage) -> acceptance script
and uploads the raw evidence as an artifact.

No Docker on your machine? `bash scripts/docker-gates.sh` runs the identical gate
locally and writes its evidence to reports/docker-gates/<commit>/.
EOF
