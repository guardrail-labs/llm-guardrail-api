# Guardrail API — Runtime Overview

> Guardrail Labs, LLC — Patent Pending  
> This document describes how the Guardrail Runtime evaluates LLM traffic,
> how the dual-arm architecture works, and how the Verifier and Policy Packs
> integrate with the enforcement pipeline.

The Guardrail Runtime powers both the open-source Core edition and the
enterprise-governance edition. It is designed to evaluate prompts (ingress)
and model responses (egress) independently while preserving performance
and policy alignment.

This document explains the lifecycle of a request through the runtime.

---

# 🧱 1. Dual-Arm Architecture

Guardrail evaluates AI traffic through two independent paths:

- **Ingress Arm** — evaluates incoming user prompts  
- **Egress Arm** — evaluates model-generated responses  

Both arms apply policy, sanitization, and clarification logic.  
They operate independently so egress protections continue even if ingress
is degraded or rate-limited.

### Summary

- Ingress focuses on **intent, safety, and ambiguity**  
- Egress focuses on **content, leakage, and compliance**  
- Arms do not rely on each other for correctness  
- Each maintains separate metrics and decisions  

---

# ✨ 2. Request Lifecycle (Ingress)

When a client sends a request through Guardrail, the runtime evaluates **all
modalities**, not just text. Guardrail inspects and applies policy to:

- text prompts  
- images  
- audio streams  
- uploaded files and documents  
- JSON payloads or structured inputs  
- model-specific tool-call or function-call envelopes  

All modalities pass through the same governance pipeline.

## Step 1 — Normalization & Sanitization
Guardrail performs modality-appropriate preprocessing, which may include:

- text: Unicode normalization, confusables detection, obfuscation signals  
- images: metadata stripping, format validation, safety category extraction  
- audio: transcription stream extraction (if enabled), metadata validation  
- files: MIME checking, structured content extraction, size and type limits  

Signals produced here feed into policy evaluation.

## Step 2 — Policy Pack Evaluation
Policy Packs determine:
- allowed or disallowed categories  
- modality-specific rules (e.g., image safety, file restrictions)  
- requirements for clarification  
- regulatory boundaries (e.g., PHI/PII constraints)  

Rules are applied consistently across all modalities.

## Step 3 — Clarify-First Workflow
If intent or content is ambiguous:
- The Verifier may be consulted for non-execution analysis  
- If ambiguity remains, the request is returned to the submitter  
- Guardrail does not guess or assume intent  

This applies equally to text, images, audio, and file-based inputs.

## Step 4 — Forward to LLM
Once evaluated and cleared, the request—regardless of modality—is forwarded to
the configured model provider through the runtime’s enforcement layer.


---

# 🔄 3. Response Lifecycle (Egress)

After the LLM generates a response, Guardrail evaluates **all output
modalities**, not just text. The egress arm inspects and evaluates:

- text responses  
- image outputs  
- audio outputs  
- file and document results  
- tool-call / function-call results  
- JSON-mode structured outputs  

Each modality goes through the same governance pipeline with
modality-appropriate checks.

## Step 1 — Output Normalization
Guardrail performs light normalization depending on modality, such as:

- text: normalization, metadata tagging  
- images: format validation, metadata stripping, safety signal extraction  
- audio: transcription-based safety checks (if enabled)  
- files: MIME validation, size and type checks, structured extraction  

Normalization feeds signal data into egress policy evaluation.

## Step 2 — Egress Policy Evaluation
Egress rules determine whether model output:

- contains disallowed content  
- could leak sensitive information  
- violates a regulatory profile  
- requires redaction before delivery  
- requires clarification (ambiguous or high-risk content)  

Rules may be modality-specific, such as:

- image safety categories  
- file type restrictions  
- audio transcription checks  
- structured output validation  

The egress arm evaluates output independently of the ingress arm.

## Step 3 — Enforcement Decision
Depending on policy outcome:

- The response is approved and returned to the client  
- The response is **blocked** with a policy decision  
- The system returns a **clarification request** to the submitter  
- The output is **redacted or transformed** (where allowed by policy)  

If content is ambiguous or high-risk, egress may route back to the
same clarify-first logic used on ingress.

## Step 4 — Return to Client
Once evaluated, the runtime returns:

- the approved model output, or  
- a structured policy decision (reason, category, tenant context)  

All outcomes are logged to audit streams, including modality metadata.


---

# 🧩 4. Verifier Integration

The Verifier is a separate microservice used only when intent is unclear.

It performs:
- Non-execution, instruction-level analysis  
- Classification of ambiguous or dual-use instructions  
- Support for policy-driven clarify-first logic  

If the Verifier cannot clearly classify:
- The runtime **returns the request to the submitter**  

If the Verifier provides a safe categorization:
- Policy evaluation continues normally  

The Verifier never executes untrusted content.

---

# 📦 5. Policy Packs

Policy Packs define the rules that govern the runtime.

Each pack includes:
- Safety categories  
- Regulatory profiles (GDPR, HIPAA, AI Act templates)  
- Pattern and category rules  
- Metadata, signatures, and checksums  

Policy Packs are:
- Versioned  
- Signed  
- Immutable once released  
- Tenant-scoped  
- Audited when activated or rolled back  

They provide the rule surface the runtime enforces.

---

# 🏛 6. Enterprise Runtime Differences

The open-source Core Runtime and the Enterprise Runtime share the same evaluation engine.  
Enterprise adds operational, governance, and compliance features.

### Enterprise adds:
- Admin Console (UI)  
- Tenant isolation controls  
- RBAC  
- Retention + evidence bundles  
- Audit dashboards  
- Signed artifacts and SBOMs  
- Advanced rate limiting and DLQ controls  

### Core provides:
- Dual-arm policy enforcement  
- Clarify-first workflows  
- Verifier integration  
- Policy Pack execution  
- All evaluation logic  

Enterprise enhances, not replaces, the core runtime.

---

# 🔐 7. Audit Logging

Every major action is logged with structured metadata:

- Sanitization notes  
- Policy decisions  
- Clarifications  
- Blocks and overrides  
- Egress-level decisions  
- Verifier involvement  
- Admin actions (Enterprise only)  

Audit logs serve as evidence for:
- Security teams  
- Compliance programs  
- Incident reviews  
- Governance reporting  

Enterprise deployments may export evidence bundles.

---

# 🌐 8. Runtime Configuration

Guardrail runtimes can be configured via environment variables:

Common settings include:
- LLM provider credentials  
- Redis connection  
- Policy pack paths  
- Tenant configuration  
- Verifier endpoint (optional)  

Enterprise deployments add:
- Retention settings  
- Admin UI configuration  
- Object storage endpoints  
- RBAC and IAM integration  

Configuration is declarative and designed for container-first deployment.

---

# 🧪 9. Runtime Guarantees (Clarifications)

Guardrail does **not** guarantee safety or compliance.  
But it does provide:

- A structured evaluation layer  
- Defense-in-depth against unsafe prompt patterns  
- Controls that reduce risk of model degradation  
- Oversight for dangerous or non-compliant outputs  
- A governance trail for investigations  

The runtime supports organizational policy, not a replacement for it.

---

# 🆘 10. Support

For runtime assistance or onboarding:

- **enterprise@guardrailapi.com**  
- **security@guardrailapi.com**

---

*This document describes runtime behavior for both the open-source Core
edition and the enterprise governance edition.*
