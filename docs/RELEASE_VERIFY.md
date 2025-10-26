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
2. Verify checksum integrity:
   ```bash
   guardrailctl verify --edition enterprise --tag v1.0.0-GA
   guardrailctl verify --edition core --tag v1.0.0-GA
   ```
3. Perform a clean install to a temporary directory and run smoke tests:
   ```bash
   guardrailctl install --edition enterprise --tag v1.0.0-GA --dest /tmp/guardrail-test
   docker compose -f /tmp/guardrail-test/docker-compose.yaml config
   ```
4. Document verification results and attach logs to the release ticket.
