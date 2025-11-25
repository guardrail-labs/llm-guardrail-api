# Policy Packs (v1.0.0)

Policy packs are versioned bundles of guardrail rules, filters, and metadata. They are validated in
CI and loaded by Guardrail Core to enforce safety and compliance requirements. Enterprise Console
uses the same packs to drive approvals, usage views, and tenant-specific policy selection.

## Manifest layout
`packs/<pack>/manifest.yaml`
```yaml
name: "GDPR Core"
id: "gdpr"
version: "1.0.0"
schema: "1.0.0"
status: "stable"     # stable|beta|deprecated
updated: "2025-11-11"
compat:
  core: ">=1.6.0"
  enterprise: ">=1.5.0"
summary: "Baseline GDPR enforcement."
```

Manifests declare the pack identity, compatible runtime ranges, and publication status. Packs follow
semantic versioning; increment major for breaking rule changes, minor for new rules, and patch for
fixes.

## Loading packs
- **Core:** Install pack artifacts into the runtime using `guardrailctl` or the API. Core watches for
  new versions and reloads policies without restart.
- **Enterprise:** The Admin Console displays available packs, stages promotions, and records
  approvals. It reads compatibility fields to ensure packs align with Core 1.6.0 deployments.

## Schema validation
Validation tooling (for example, `python tools/validate_packs.py`) enforces manifest presence and
schema conformance before packs are published.
---

**Guardrail Labs, LLC — Patent Pending**
