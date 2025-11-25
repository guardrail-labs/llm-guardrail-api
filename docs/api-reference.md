# API Reference

The Guardrail API exposes REST interfaces for runtime decisions, health/status checks, and
administrative usage reporting. Use the OpenAPI specification published with each runtime release
for exhaustive details.

**Outline**
- Decision endpoints
- Health and status endpoints
- Admin and usage endpoints (Core 1.6.0)

## Authentication

Requests require a workspace-scoped API token or a service account credential generated from the
Admin UI.

```
Authorization: Bearer <token>
X-Guardrail-Tenant: <workspace-id>
```

Tokens are short-lived. Use the `/v1/auth/token` endpoint to exchange long-lived refresh tokens
for access tokens when integrating with automation.

## Decision endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/v1/runtime/invoke` | Submit a prompt for policy evaluation and model routing. |
| `POST` | `/v1/runtime/test` | Execute a dry-run prompt against the configured policies. |
| `GET` | `/v1/runtime/logs` | Stream decision logs for monitoring and troubleshooting. |

Responses include the headers `X-Guardrail-Decision`, `X-Guardrail-Mode`, and
`X-Guardrail-Incident-ID` for correlation.

## Health and status endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/healthz` | Liveness probe for the service container. |
| `GET` | `/metrics` | Prometheus exposition for runtime counters and gauges. |
| `GET` | `/openapi.json` | Published OpenAPI document for the running version. |

## Admin and usage endpoints (Core 1.6.0)

Core 1.6.0 introduces aggregated usage metrics consumed by the Enterprise Console.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/v1/admin/usage/summary` | Aggregated usage by tenant and period for billing. |
| `GET` | `/v1/admin/usage/events` | Normalized decision events for audit and analytics. |

## Webhooks and events

Guardrail publishes structured events to your configured webhook endpoints. Events follow a JSON
schema with the fields `type`, `tenant`, `timestamp`, and `payload`.

Common event types include:

* `policy.pack.promoted`
* `policy.pack.rollback`
* `runtime.decision`
* `admin.role.assignment`

Subscribe via the `/v1/events/subscriptions` endpoint and acknowledge deliveries to maintain a
reliable feed.

## Rate limiting and quotas

The runtime enforces per-workspace rate limits. Default limits are suitable for testing and can be
increased through the Admin UI or API. Requests exceeding the limit receive a `429 Too Many
Requests` response with headers indicating when to retry.

## Error handling

Errors follow the RFC 7807 problem+json format. A sample error payload looks like:

```json
{
  "type": "https://docs.guardrail.ai/errors/invalid-policy",
  "title": "Policy violation",
  "status": 400,
  "detail": "Prompt blocked by customer-safety@1.4.0",
  "instance": "123e4567-e89b-12d3-a456-426614174000"
}
```

Use the `instance` identifier when contacting support. It maps directly to decision logs stored in
the event bus.
---

**Guardrail Labs, LLC — Patent Pending**
