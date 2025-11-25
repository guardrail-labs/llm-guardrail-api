# API Summary

Use this page as a quick index into the runtime endpoints. See the [API Reference](../api-reference.md)
for full details and payload schemas.

| Area | Endpoints | Notes |
| --- | --- | --- |
| Decisions | [`POST /v1/runtime/invoke`](../api-reference.md#decision-endpoints) | Primary decision path with policy evaluation. |
| Health | [`GET /healthz`](../api-reference.md#health-and-status-endpoints) | Liveness probe for deployments and smoke tests. |
| Metrics | [`GET /metrics`](../api-reference.md#health-and-status-endpoints) | Prometheus metrics including usage counters. |
| Admin Usage | [`GET /v1/admin/usage/summary`](../api-reference.md#admin-and-usage-endpoints-core-160) | Core 1.6.0 aggregated usage for billing periods. |
| Events | [`/v1/events/subscriptions`](../api-reference.md#webhooks-and-events) | Manage webhook subscriptions for decision and admin events. |
---

**Guardrail Labs, LLC — Patent Pending**
