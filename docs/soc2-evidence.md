# SOC 2 Evidence

Guardrail API ships with tooling and documentation to simplify SOC 2 audits. This page
explains where to find required evidence and how to keep it current.

## Evidence bundle overview

The verifier produces an evidence bundle each time you validate a runtime release or policy
pack. The bundle contains:

* Signed attestation describing build provenance and release metadata.
* CycloneDX SBOMs for every container and policy artifact.
* Hash manifest summarizing digests validated during verification.
* `report.md` outlining the verification steps, timestamp, and operator identity.

Store bundles in a dedicated GRC repository or ticketing system. Tag releases with the change
request ID to make retrieval easy during audits.

## Operational controls

To demonstrate SOC 2 operational controls:

1. **Change Management** – Attach verifier reports to deployment tickets and capture approval
   from the required reviewers inside the Admin UI.
2. **Access Reviews** – Export RBAC assignments from the Admin UI or API. The `guardrailctl`
   CLI supports CSV exports you can hand to auditors.
3. **Monitoring** – Stream decision logs and administrative events into your SIEM. Retain logs
   for at least one year or your policy requirement.
4. **Incident Response** – Document runbooks in your operations knowledge base. Link incidents
   to affected policy packs and note remediation steps.

## Evidence refresh cadence

* **Quarterly** – Re-run the verifier on all production runtimes and packs. Confirm SBOM
  dependencies have no outstanding critical vulnerabilities.
* **Annually** – Rotate signing keys, review tenant access, and update incident response
  exercises.
* **On Change** – Whenever a runtime or pack changes, capture a new evidence bundle and attach
  it to the corresponding change request.

## Sharing with auditors

When auditors request evidence, provide:

* The zipped verifier bundle for the requested release.
* A screenshot or exported report from the Admin UI showing the approval trail.
* Links to monitoring dashboards that visualize guardrail decision logs.

These assets demonstrate that Guardrail maintains continuous compliance and that every release
is governed by rigorous verification.
