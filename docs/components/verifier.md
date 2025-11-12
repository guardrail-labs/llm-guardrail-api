> Guardrail Labs, LLC — Patent Pending

# Verifier Microservice (v0.2.0)

- **Purpose:** Assess ambiguous intent with provider failover; no code execution.
- **Fallback Chain:** Gemini → Claude → GPT (configurable).
- **Breaker:** Opens on provider failure; requests short-circuit to next provider.

**Metrics**
- `verifier_requests_total`, `verifier_latency_seconds`, provider breaker state counters.

**API**
- `POST /verify` — assess-only request; returns allow/deny/clarify rationale.
