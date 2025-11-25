# Guardrail Architecture

Guardrail API is designed as a modular control plane that mediates large language model requests,
enforces policy, and produces audit evidence. The platform is composed of the following services
and artifacts.

## Runtime services

* **API Gateway** – receives inference or orchestration requests from client applications
  and applies policy pack evaluations before forwarding prompts to upstream models.
* **Policy Engine** – executes policy pack rules, drawing on tenant configuration, RBAC
  assignments, and contextual metadata to determine allow, redact, or deny outcomes.
* **Event Bus** – publishes structured decision logs that downstream observability systems
  can consume for audit or analytics use cases.
* **Storage** – persists policy pack definitions, tenant metadata, and verifier attestations.

The Core runtime ships with reference Docker Compose and Helm assets so you can deploy the
services to a local environment or production cluster. Enterprise customers receive hardened
container images, FIPS-compliant builds, and extended observability integrations.

## Admin experience

The Admin UI provides a web-based front end. It connects to the same runtime services and is
responsible for operations tasks such as tenant onboarding, role assignment, and policy pack
publishing. The UI interacts with the API Gateway through authenticated service accounts and
records every administrative action for compliance tracking.

## Policy packs

Policy packs are versioned bundles containing:

* Guardrail rules expressed in the Guardrail DSL.
* Prompt and response filters for offensive content, PII, or custom business policies.
* Metadata describing allowed deployment targets and dependencies.

Packs are delivered through the Policy Pack repository or as private artifacts for Enterprise
customers. They can be staged, promoted, and rolled back without redeploying the runtime.

## Release verification

The Verifier workflow validates every runtime and policy pack artifact. It checks the build
provenance, verifies signed attestations, and ensures SBOMs are attached. Verified releases
are eligible for promotion into regulated environments such as SOC 2 audited production
clusters.

## Multi-repo model

The Guardrail platform intentionally splits code across repositories so each artifact can be
versioned and governed independently. Review the [Overview](index.md) page for a description of
how this repository coordinates runtime, UI, verifier, and policy pack updates.

---

**Guardrail Labs, LLC — Patent Pending**
