#!/usr/bin/env bash
set -euo pipefail

if [ -n "${NOTICE:-}" ]; then
  echo "::notice title=${NOTICE_TITLE:-finish}::${NOTICE}"
fi

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
git add -A
git diff --staged --quiet || git commit -m "${COMMIT_MESSAGE:-chore: automated changes [skip ci]}"
git push
