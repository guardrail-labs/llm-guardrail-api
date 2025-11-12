# Quickstart — Hello Guardrail

Spin up the Guardrail Core, Enterprise, and Verifier services locally and confirm that the
basics respond as expected.

## Prereqs
- Docker (or podman with the `docker` alias)
- curl
- jq (for inspecting the OpenAPI document)

## Start services
```bash
docker run -d --rm --name guardrail-core -p 8080:8080 \
  ghcr.io/guardrail-labs/guardrail-core:1.5.0
docker run -d --rm --name guardrail-enterprise -p 8081:8081 \
  ghcr.io/guardrail-labs/guardrail-enterprise:1.4.0
docker run -d --rm --name guardrail-verifier -p 8082:8082 \
  ghcr.io/guardrail-labs/guardrail-verifier:0.2.0
```

## Health checks
```bash
curl -sS http://127.0.0.1:8080/healthz
curl -sS http://127.0.0.1:8081/healthz
curl -sS http://127.0.0.1:8082/healthz
```

## Metrics checks
```bash
curl -sS http://127.0.0.1:8080/metrics | head
curl -sS http://127.0.0.1:8081/metrics | head
curl -sS http://127.0.0.1:8082/metrics | head
```

## OpenAPI presence
```bash
curl -sS http://127.0.0.1:8080/openapi.json | jq '.info.version'
curl -sS http://127.0.0.1:8081/openapi.json | jq '.info.version'
```

## Note
- Versions used above: Core `1.5.0`, Enterprise `1.4.0`, Verifier `0.2.0`.
- If you change ports or run behind a proxy, update the curl targets accordingly.
