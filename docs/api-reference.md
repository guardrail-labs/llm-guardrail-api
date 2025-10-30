# API Reference

The Guardrail API exposes REST and event-based interfaces for managing tenants, policy packs,
and runtime operations. This page summarizes the most commonly used endpoints. Consult the
OpenAPI specification published with each runtime release for exhaustive details.

## Authentication

Requests require a workspace-scoped API token or a service account credential generated from
the Admin UI.

```
Authorization: Bearer <token>
X-Guardrail-Tenant: <workspace-id>
```

Tokens are short-lived. Use the `/v1/auth/token` endpoint to exchange long-lived refresh tokens
for access tokens when integrating with automation.

## Tenants

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/v1/tenants` | List organizations and workspaces visible to the caller. |
| `POST` | `/v1/tenants` | Create a new workspace within the caller's organization. |
| `PATCH` | `/v1/tenants/{workspace}` | Update metadata, notification channels, or runtime quotas. |
| `POST` | `/v1/tenants/{workspace}/members` | Invite a member and assign an RBAC role. |

## Policy packs

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/v1/packs` | List available packs and their deployment status. |
| `POST` | `/v1/packs/promote` | Promote a verified pack version into the selected workspace. |
| `POST` | `/v1/packs/rollback` | Roll back to a previous pack version. |
| `GET` | `/v1/packs/{pack}/history` | Retrieve promotion history and verifier evidence. |

## Runtime operations

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/v1/runtime/test` | Execute a dry-run prompt against the configured policies. |
| `POST` | `/v1/runtime/invoke` | Submit a prompt for policy evaluation and model routing. |
| `GET` | `/v1/runtime/logs` | Stream decision logs for monitoring and troubleshooting. |
| `POST` | `/v1/runtime/tokens` | Rotate API tokens for workspace applications. |

## Webhooks and events

Guardrail publishes structured events to your configured webhook endpoints. Events follow a
JSON schema with the fields `type`, `tenant`, `timestamp`, and `payload`.

Common event types include:

* `policy.pack.promoted`
* `policy.pack.rollback`
* `runtime.decision`
* `admin.role.assignment`

Subscribe via the `/v1/events/subscriptions` endpoint and acknowledge deliveries to maintain a
reliable feed.

## Rate limiting and quotas

The runtime enforces per-workspace rate limits. Default limits are suitable for testing and can
be increased through the Admin UI or API. Requests exceeding the limit receive a `429 Too Many
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

Use the `instance` identifier when contacting support. It maps directly to decision logs stored
in the event bus.
