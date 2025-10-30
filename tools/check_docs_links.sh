#!/usr/bin/env bash
set -euo pipefail
bad=$(grep -RIn "\\.\\./" docs || true)
if [[ -n "$bad" ]]; then
  echo "ERROR: Found parent-directory links in docs (not allowed by MkDocs):"
  echo "$bad"
  exit 1
fi
