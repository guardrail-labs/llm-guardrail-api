# Release Notes

This page summarizes the latest changes across the Guardrail platform. Each release listed below
includes links to verifier evidence and policy pack compatibility notes.

## Core API 1.6.0
- Introduced aggregated usage metrics and period summaries for multi-tenant billing.
- Added admin usage endpoints consumed by the Enterprise Console.
- Improved event normalization and ingestion stability for high-volume workloads.

## Enterprise 1.5.0
- Shipped the Enterprise Admin Console for tenant-level operations.
- Added usage and billing views backed by Core 1.6.0 metrics.
- Improved navigation across tenants, traffic, and clarifications.

## 2024-06-15 — Docs Refresh
- Introduced the MkDocs-based documentation portal hosted via GitHub Pages.
- Added guidance for the multi-repo layout, tenants & RBAC, policy packs, and SOC 2 evidence.
- Updated the Quickstart with Helm and Docker Compose rendering examples.

## 2024-05-20 — Verifier Enhancements
- Verifier now exports CycloneDX SBOMs for every runtime container.
- Added support for uploading evidence bundles directly to Guardrail Admin UI.
- Improved error messages when signatures do not match expected digests.

## 2024-04-01 — Policy Pack Channels
- Introduced canary channels so teams can test new rules in isolation.
- Added CLI commands for listing pack promotion history and rollback actions.
- Hardened Admin UI approvals with dual-authorization support.

Refer to the Guardrail release calendar or the individual runtime repositories for more granular
changelog entries.
