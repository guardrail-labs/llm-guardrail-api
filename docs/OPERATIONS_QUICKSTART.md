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

1. Verify the new release (use `--soc2` when required for audits):
   ```bash
   guardrailctl verify --edition enterprise --tag v1.1.0-GA --soc2
   ```
2. Upgrade in-place. The command downloads to a temp directory, verifies checksums, extracts into `/opt/guardrail/releases/<tag>`, then atomically moves the `current` symlink:
   ```bash
   guardrailctl upgrade --edition enterprise --tag v1.1.0-GA --from /opt/guardrail
   ```
3. Confirm the active build:
   ```bash
   guardrailctl current --root /opt/guardrail
   ```
4. Restart services (`docker compose` or Helm) to pick up the new release once you are ready to cut traffic over.

## Disaster Recovery

- Schedule Redis backups via `redis-cli --rdb` or managed service snapshots.
- Archive audit logs stored under `/opt/guardrail/logs`.
