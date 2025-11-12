# Policy Packs (v1.0.0)

Policy packs declare compliance rules and metadata via a **manifest**. Packs are validated in CI.

## Manifest (per pack)
`packs/<pack>/manifest.yaml`
```yaml
name: "GDPR Core"
id: "gdpr"
version: "1.0.0"
schema: "1.0.0"
status: "stable"     # stable|beta|deprecated
updated: "2025-11-11"
compat:
  core: ">=1.5.0"
  enterprise: ">=1.1.0"
summary: "Baseline GDPR enforcement."
```

Changelogs live in packs/<pack>/CHANGELOG.md.

Validation tool: python tools/validate_packs.py.
