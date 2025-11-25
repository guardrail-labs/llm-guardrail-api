# Clarify-First Blocking Model

Guardrail evaluates every request with a clarify-first approach before allowing it to reach an
LLM. Ingress classifiers look for ambiguous intent, policy conflicts, and safety risks. When a
prompt is unclear, the request is routed to the Verifier Service for an assess-only review and
returns a clarifying response, a block decision, or approval to continue.

This flow keeps potentially unsafe prompts from executing while minimizing false positives. The
same pattern applies to egress responses so redaction and filtering can remove sensitive content
before it is delivered back to the caller.
