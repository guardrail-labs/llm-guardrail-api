# Release Verification

Use this runbook to validate Guardrail API release artifacts.

## Prerequisites

- GitHub token with access to the Enterprise releases when testing Enterprise builds.
- `guardrailctl` installed locally.

## Steps

1. List channels to confirm configuration:
   ```bash
   guardrailctl channels list
   ```
2. Verify checksum integrity, including the SOC2 bundle for Enterprise builds:
   ```bash
   guardrailctl verify --edition enterprise --tag v1.0.0-GA --soc2
   guardrailctl verify --edition core --tag v1.0.0-GA
   ```
3. Stage the release into a scratch directory and run smoke tests:
   ```bash
   guardrailctl upgrade --edition enterprise --tag v1.0.0-GA --from /tmp/guardrail-test
   docker compose -f /tmp/guardrail-test/docker-compose.yaml config
   ```
4. Document verification results and attach logs to the release ticket.
