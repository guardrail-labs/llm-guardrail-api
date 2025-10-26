# Guardrail API Admin Guide

## User Management

- Local administrator account configured via `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`.
- Integrate with SSO providers through the Enterprise admin console.

## Policy Management

- Policies define prompt sanitization, output redaction, and rate limits.
- Use the admin console or REST API `/admin/policies` endpoints to manage policies.
- Version policies and store them alongside application configuration.

## Auditing

- Audit logs exported to the configured sink (S3, syslog, or local filesystem).
- Ensure log retention policies meet compliance requirements.

## Security Hardening

- Restrict access to the admin console via network ACLs.
- Rotate API keys and admin credentials quarterly.
- Enable SOC2 artifact builds for regulated workloads.
