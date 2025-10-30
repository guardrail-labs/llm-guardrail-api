# Verifier

The Guardrail Verifier is a command-line workflow that validates runtime and policy pack
artifacts before they are promoted to regulated environments. It provides cryptographic
attestation, SBOM generation, and evidence packaging aligned with SOC 2 requirements.

## When to run the Verifier

* Before promoting a new runtime release to staging or production.
* When adding or updating policy packs that contain new rules or dependencies.
* Prior to a quarterly SOC 2 control review to ensure evidence is complete.

## Requirements

* Access to the artifact registry that hosts Guardrail images or policy pack bundles.
* The `guardrailctl` CLI or standalone verifier binary.
* Trusted root certificates used to validate Guardrail signing keys.

## Running the verifier

```bash
guardrailctl verify --edition enterprise --tag v1.0.0-GA --output ./evidence
```

The command performs the following checks:

1. Downloads the manifest for the requested release.
2. Validates container signatures and compares digests.
3. Generates a CycloneDX SBOM for each artifact.
4. Writes an attestation bundle (`attestation.json`) and summary report (`report.md`).

The evidence directory can be uploaded to your change request ticket, stored in a GRC tool, or
attached to an internal audit package.

## Automating verification

Integrate the verifier into CI/CD pipelines to block deployments when evidence is missing or
signatures are invalid. The CLI exits with a non-zero status if any check fails, making it easy
to wire into GitHub Actions, GitLab CI, or Jenkins pipelines.

## Troubleshooting

* **Signature mismatch** – Ensure your verifier has the latest Guardrail public keys. Rotate
  keys annually and distribute them through your secrets manager.
* **Missing SBOM** – Rebuild the artifact with the SBOM generation flag enabled. Enterprise
  pipelines enforce this automatically.
* **Connectivity failures** – If operating in a restricted network, mirror the artifacts to an
  internal registry and point the verifier to the mirror URL.
