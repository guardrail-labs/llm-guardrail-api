# Guardrail Verifier Service

The Verifier Service (v0.2.0) is an assess-only component used for ambiguous or high-risk
prompts. It reviews requests before execution and returns allow, deny, or clarify responses
without running user-supplied code.

- **Purpose:** Assess ambiguous intent with configurable provider failover; no code execution.
- **Fallback Chain:** Gemini → Claude → GPT (configurable).
- **Breaker:** Opens on provider failure; requests short-circuit to the next provider.

**Metrics**
- `verifier_requests_total`, `verifier_latency_seconds`, provider breaker state counters.

**API**
- `POST /verify` — assess-only request; returns allow/deny/clarify rationale.
