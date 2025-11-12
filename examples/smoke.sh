#!/usr/bin/env bash
set -euo pipefail

urls=(
  "http://127.0.0.1:8080/healthz"
  "http://127.0.0.1:8081/healthz"
  "http://127.0.0.1:8082/healthz"
  "http://127.0.0.1:8080/metrics"
  "http://127.0.0.1:8081/metrics"
  "http://127.0.0.1:8082/metrics"
)

for u in "${urls[@]}"; do
  echo "→ $u"
  curl -fsS "$u" >/dev/null
done
echo "✅ smoke ok"
