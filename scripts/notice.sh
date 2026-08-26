#!/usr/bin/env bash
set -euo pipefail

if [ -n "${NOTICE:-}" ]; then
  echo "::notice title=${NOTICE_TITLE:-notice}::${NOTICE}"
fi
