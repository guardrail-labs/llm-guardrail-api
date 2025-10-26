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
3. Verify the target release (include `--soc2` if you need the audit bundle):
   ```bash
   guardrailctl verify --edition enterprise --tag v1.0.0-GA --soc2
   ```
4. Perform an in-place upgrade. This stages the new release and atomically flips the `current` symlink:
   ```bash
   guardrailctl upgrade \
     --edition enterprise \
     --tag v1.0.0-GA \
     --from /opt/guardrail
   ```
   Check the active release at any time with `guardrailctl current`.
5. Initialize Docker Compose assets and start the stack. Use `--profile full` to add Prometheus and Grafana stubs:
   ```bash
   guardrailctl compose init --profile full --dest /opt/guardrail
   guardrailctl compose env --write --dest /opt/guardrail
   docker compose -f /opt/guardrail/docker-compose.yaml up -d
   ```

For Kubernetes clusters, render manifests with merged values and apply them with `kubectl`:

```bash
guardrailctl helm render --values ./my-values.yaml --out ./manifests
kubectl apply -f ./manifests
```

## Tenant bootstrap

After the API is running, seed the first tenant and admin user with the Admin API helpers:

```bash
guardrailctl tenant create --id default --admin-user admin@example.com \
  --url http://localhost:8080 --token "$GUARDRAIL_TOKEN"
```

List tenants with either CLI flags or the `GUARDRAIL_URL`/`GUARDRAIL_TOKEN` environment variables:

```bash
guardrailctl tenant list --json
```
