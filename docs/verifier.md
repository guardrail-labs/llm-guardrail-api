# Verifier

The Guardrail Verifier is an assess-only service used when prompts are ambiguous or high-risk. It
reviews requests before they reach a model and issues allow, deny, or clarify guidance without
executing user-supplied code.

## When to use the Verifier

- Ingress requests that contain unclear intent or potentially unsafe instructions.
- Workloads that require an additional review step before invoking upstream models.
- Tenants that prefer clarify-first workflows to reduce false positives from strict blocking.

## Request flow

1. Core detects an ambiguous prompt and forwards the payload to the Verifier endpoint.
2. The Verifier evaluates the content using configured providers and returns an allow/deny/clarify
   decision with rationale.
3. Core applies the decision and records the result in decision logs for audit.

## Deployment notes

- Runs as a separate service (`guardrail-verifier:0.2.0`) alongside Core and Enterprise.
- Never executes user code or untrusted extensions; it performs assessments only.
- Exposes `/healthz`, `/metrics`, and `POST /verify` for status and decisions.

## Operations

Monitor `verifier_requests_total` and `verifier_latency_seconds` metrics to track throughput and
performance. Breaker state counters indicate when a provider has been taken out of rotation after a
failure.
---

**Guardrail Labs, LLC — Patent Pending**
