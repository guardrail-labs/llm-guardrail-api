# Install Guardrail API Enterprise

This guide walks through installing Guardrail API Enterprise via the `guardrailctl` CLI.

## Requirements

- Python 3.11+
- Access to the Guardrail API Enterprise GitHub release artifacts (requires `GH_TOKEN`).
- Docker Engine (for Compose) or a Kubernetes cluster (for Helm).

## Steps

1. Install the CLI using `pipx` or a virtual environment:
   ```bash
   pipx install git+https://github.com/WesMilam/llm-guardrail-api.git
   ```
2. Export a GitHub token with release download permissions:
   ```bash
   export GH_TOKEN=ghp_yourtoken
   ```
3. Verify the target release:
   ```bash
   guardrailctl verify --edition enterprise --tag v1.0.0-GA
   ```
4. Install the release to the destination path:
   ```bash
   guardrailctl install --edition enterprise --tag v1.0.0-GA --dest /opt/guardrail
   ```
5. Initialize Docker Compose assets and start the stack:
   ```bash
   guardrailctl compose init --dest /opt/guardrail
   docker compose -f /opt/guardrail/docker-compose.yaml up -d
   ```

For Kubernetes clusters, use `guardrailctl helm render --out ./manifests` and apply the manifests with `kubectl`.
