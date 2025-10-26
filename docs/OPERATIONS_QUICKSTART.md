# Operations Quickstart

This quickstart outlines the operational workflows once Guardrail API is deployed.

## Configuration

- Update `/opt/guardrail/.env` with environment-specific settings.
- Restart services after configuration changes:
  ```bash
  docker compose -f /opt/guardrail/docker-compose.yaml restart
  ```

## Monitoring

- Prometheus metrics exposed on `:8080/metrics` when enabled.
- Review logs via `docker logs guardrail_guardrail_1`.

## Upgrading

1. Verify the new release:
   ```bash
   guardrailctl verify --edition enterprise --tag v1.1.0-GA
   ```
2. Install to a staging directory:
   ```bash
   guardrailctl install --edition enterprise --tag v1.1.0-GA --dest /opt/guardrail-v1.1.0
   ```
3. Drain traffic, swap symlinks or update Compose/Helm manifests, then restart services.

## Disaster Recovery

- Schedule Redis backups via `redis-cli --rdb` or managed service snapshots.
- Archive audit logs stored under `/opt/guardrail/logs`.
