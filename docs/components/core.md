# Guardrail Core Runtime

Guardrail Core (v1.6.0) is the enforcement engine that handles ingress and egress filtering,
executes policy packs, and emits decision events. It powers both standalone deployments and the
Guardrail Enterprise Console.

- **Purpose:** Ingress/egress enforcement, policy execution, audit events, and usage aggregation.
- **Status:** GA with usage aggregation and admin usage endpoints available in v1.6.0.
- **OpenAPI:** exposed by the core service at `/openapi.json`.

**Key Headers**
- `X-Guardrail-Decision` • `X-Guardrail-Mode` • `X-Guardrail-Incident-ID`

**Health & Metrics**
- `/healthz` • `/metrics` (Prometheus exposition)

**Admin and Usage (v1.6.0)**
- `/v1/admin/usage/summary` — aggregated tenant usage for billing periods.
- `/v1/admin/usage/events` — normalized decision events used by the Enterprise Console.
