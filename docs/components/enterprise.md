# Guardrail Enterprise Console

Guardrail Enterprise (v1.5.0) provides the web console for managing tenants, reviewing traffic,
and working with aggregated usage metrics emitted by Core 1.6.0.

- **Purpose:** Multi-tenant administration, compliance registry, observability, and billing views.
- **Security:** CSRF-protected session auth; tenant-scoped RBAC (owner/admin/auditor).
- **Compatibility:** Core ≥ 1.6.0 for usage aggregation endpoints.

**Endpoints (selection)**
- `/admin/compliance/packs` CRUD (CSRF required)
- `/admin/tenants` for tenant lifecycle operations
- `/metrics` includes enterprise counters and histograms aligned to core modes
