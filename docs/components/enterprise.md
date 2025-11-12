> Guardrail Labs, LLC — Patent Pending

# Enterprise Admin Console (v1.4.0)

- **Purpose:** Multi-tenant admin, compliance registry, observability.
- **Security:** CSRF-protected session auth; tenant-scoped RBAC (owner/admin/auditor).
- **Compatibility:** Core ≥ 1.5.0.

**Endpoints (selection)**
- `/admin/compliance/packs` CRUD (CSRF required)
- `/metrics` includes enterprise counters/histograms aligned to core modes
