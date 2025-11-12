# Core Runtime (v1.5.0)

- **Purpose:** Enforcement engine (ingress/egress), policy execution, audit events.
- **Status:** GA, feature-complete; patches/hotfixes only.
- **OpenAPI:** exposed by core service at `/openapi.json` (CI smoke verified).

**Key Headers**
- `X-Guardrail-Decision` • `X-Guardrail-Mode` • `X-Guardrail-Incident-ID`

**Health & Metrics**
- `/healthz` • `/metrics` (Prometheus exposition)
