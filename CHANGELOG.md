# Changelog

## 1.0.0 — GA (2025-11-02)
- Unified documentation portal (mkdocs-material) for Core, Enterprise, and Verifier.
- Quickstart (Compose), Admin UI usage, RBAC model, Policy Packs, SOC2 evidence.
- Links to per-repo READMEs and release assets.

## What’s New
2025-11-24
### Guardrail Core API — v1.6.0
Core 1.6.0 introduces the infrastructure required for accurate multi-tenant usage
tracking and billing. The release adds aggregated usage metrics, period summaries,
and admin-level usage endpoints used by the Enterprise Console. Internal
improvements were made to stabilize ingestion, normalize event records, and
prepare for downstream billing integrations.

### Guardrail Enterprise — v1.5.0
Enterprise 1.5.0 ships the first fully integrated Admin Console. This version
includes tenant management, usage summaries, traffic views, and the new billing
interface powered by the Core 1.6.0 metrics. The console now exposes a unified
operational view of tenants, policies, clarifications, and usage history,
forming the basis for Enterprise-grade administration and reporting.
