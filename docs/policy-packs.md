# Policy Packs

Policy packs are the primary mechanism for defining guardrails that evaluate prompts and
responses. This guide explains how packs are structured, versioned, and promoted through the
Guardrail platform.

## Pack structure

A policy pack repository contains:

```
policy-pack.yaml      # metadata, dependencies, semantic version
rules/                # guardrail DSL files grouped by domain
filters/              # pre-built filters such as PII detection
artifacts/            # optional ML models or lookup tables
README.md             # operational notes for administrators
```

Metadata includes pack name, description, minimum runtime version, and supported tenants. Rule
files express allow/deny logic in the Guardrail DSL and can reference filters or external
artifacts.

## Versioning and channels

Packs are published as immutable versions, for example `customer-safety@1.4.0`. Enterprise
customers may receive canary channels such as `1.4.0-rc.1` that mirror the runtime release
process. Use semantic versioning: increment major for breaking changes, minor for new rules,
and patch for bug fixes or updated documentation.

## Promotion workflow

1. **Draft** – Authors clone the policy pack repository and develop rules locally. The CLI
   provides linting and unit testing helpers.
2. **Review** – Open a pull request for peer review. Automated checks validate syntax and
   required metadata.
3. **Stage** – Merge to the `main` branch to trigger the build pipeline. The pipeline creates
   a versioned artifact and publishes it to the Guardrail registry.
4. **Verify** – Run the [Verifier](verifier.md) to ensure the pack ships with signed SBOMs and
   attestation data.
5. **Promote** – Admins approve promotion within the Admin UI, making the pack available to
   eligible tenants.

## Installing packs

Use the CLI to list available packs and install them into a workspace:

```bash
guardrailctl packs list --workspace demo

guardrailctl packs install customer-safety@1.4.0 --workspace demo
```

The runtime monitors pack updates and reloads policies without requiring a restart.

## Rollback

Because packs are immutable, rollback is a matter of promoting a previously verified version.
Record the incident review in your change management system and attach the verifier evidence
for auditors.
