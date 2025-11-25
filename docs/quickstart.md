# Quickstart — Hello Guardrail

Spin up Guardrail Core, Enterprise, and Verifier locally, create a tenant identifier, and send a
first decision request through the API.

## Prereqs
- Docker (or podman with the `docker` alias)
- curl
- jq (for inspecting the OpenAPI document)

## Start services
```bash
docker run -d --rm --name guardrail-core -p 8080:8080 \
  ghcr.io/guardrail-labs/guardrail-core:1.6.0

docker run -d --rm --name guardrail-enterprise -p 8081:8081 \
  -e GUARDRAIL_CORE_URL=http://host.docker.internal:8080 \
  ghcr.io/guardrail-labs/guardrail-enterprise:1.5.0

docker run -d --rm --name guardrail-verifier -p 8082:8082 \
  ghcr.io/guardrail-labs/guardrail-verifier:0.2.0
```

## Health checks
```bash
curl -sS http://127.0.0.1:8080/healthz
curl -sS http://127.0.0.1:8081/healthz
curl -sS http://127.0.0.1:8082/healthz
```

## Create or select a tenant
Use a tenant identifier such as `local-dev` to scope requests. For local smoke tests, set the
header directly without provisioning:
```bash
export GUARDRAIL_TENANT=local-dev
```

## Send a decision request
```bash
curl -sS -X POST http://127.0.0.1:8080/v1/runtime/invoke \
  -H "Content-Type: application/json" \
  -H "X-Guardrail-Tenant: ${GUARDRAIL_TENANT}" \
  -d '{"prompt": "Tell me a fun fact about space."}'
```
The response contains `X-Guardrail-Decision` and `X-Guardrail-Incident-ID` headers along with the
policy-evaluated result.

## Check usage and metrics
Core 1.6.0 emits aggregated usage metrics for billing and tenant visibility. After sending a few
requests, review the metrics and admin usage endpoints:
```bash
curl -sS http://127.0.0.1:8080/metrics | head
curl -sS "http://127.0.0.1:8080/v1/admin/usage/summary?tenant=${GUARDRAIL_TENANT}"
```
The Enterprise Console surfaces the same data in its usage and billing views.

## OpenAPI presence
```bash
curl -sS http://127.0.0.1:8080/openapi.json | jq '.info.version'
curl -sS http://127.0.0.1:8081/openapi.json | jq '.info.version'
```

## Note
- Versions used above: Core `1.6.0`, Enterprise `1.5.0`, Verifier `0.2.0`.
- If you change ports or run behind a proxy, update the curl targets accordingly.
---

**Guardrail Labs, LLC — Patent Pending**
