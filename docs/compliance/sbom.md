# Software Bill of Materials (SBOM)

SBOMs are generated in CI at release and attached to GitHub Releases for:
- Core Runtime
- Enterprise Admin Console
- Verifier Service

Use these SBOMs for supplier risk reviews and compliance audits. If you need to regenerate them in
your environment, run the verifier workflow against the release artifacts and export the CycloneDX
files alongside the attestation bundle.

To obtain an SBOM:
1. Download the release asset from your Guardrail artifact registry or GitHub Release page.
2. Verify the signature with the published Guardrail keys.
3. Extract the bundled CycloneDX document or generate a fresh one using the verifier when running in
   a private registry.
