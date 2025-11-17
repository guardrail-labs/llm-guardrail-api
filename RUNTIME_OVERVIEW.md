# Guardrail API — Runtime Overview

> Guardrail Labs, LLC — Patent Pending  
> This document describes how the Guardrail Runtime evaluates LLM traffic,
> how the dual-arm architecture works, and how the Verifier and Policy Packs
> integrate with the enforcement pipeline.

The Guardrail Runtime powers both the open-source Core edition and the
enterprise-governance edition. It evaluates AI traffic across all supported
modalities and applies policy-driven governance at both ingress (prompts) and
egress (model responses).

Guardrail does not modify the underlying model. It provides a transparent,
policy-aligned layer that organizations control.

---

# 🧱 1. Dual-Arm Architecture

Guardrail evaluates AI traffic through two independent enforcement paths:

- **Ingress Arm** — evaluates user-provided prompts and inputs  
- **Egress Arm** — evaluates model-generated responses  

Both arms:

- Apply sanitization and governance rules  
- Support clarify-first workflows  
- Maintain independent SLAs and circuit states  
- Log structured audit events  

Egress continues to function even if ingress is degraded, rate-limited, or
temporarily unavailable.

---

# ✨ 2. Request Lifecycle (Ingress)

Guardrail supports **all modalities**, not just text. Every inbound request is
evaluated according to its content type:

- text prompts  
- images  
- audio streams  
- uploaded files and documents  
- structured JSON or function-call payloads  
- model/agent tool-call envelopes  

All modalities pass through a unified enforcement pipeline with
modality-appropriate analysis.

## Step 1 — Normalization & Sanitization

Depending on modality, Guardrail may perform:

- **Text:** Unicode normalization, confusables detection, obfuscation signals  
- **Images:** metadata stripping, format validation, category extraction  
- **Audio:** optional transcription-based metadata extraction  
- **Files:** MIME/type checks, extraction, size and structure validation  
- **JSON/Tools:** schema validation, unsafe field detection  

The runtime attaches modality and sanitization signals to the evaluation context.

## Step 2 — Policy Pack Evaluation

Policy Packs provide the rule surface for ingress governance:

- allowed/disallowed categories  
- ambiguity indicators  
- modality-specific rules (image safety, file restrictions, structured validation)  
- regulatory checks (GDPR, HIPAA, AI Act profiles, etc.)  

If a rule indicates ambiguity, proceed to clarifications.  
If a rule blocks content, the request is denied with a structured decision.

## Step 3 — Clarify-First Workflow

If intent or meaning is unclear:

- The Verifier may be consulted for **non-execution** classification  
- If ambiguity remains, Guardrail returns the request to the submitter  
- Guardrail does not guess user intent  

Clarify-first applies equally to text, images, audio, documents, and structured data.

## Step 4 — Forward to LLM

If allowed, Guardrail forwards the sanitized, policy-evaluated request to the
configured LLM provider.

---

# 🔄 3. Response Lifecycle (Egress)

After the LLM generates output, Guardrail evaluates **all modalities**:

- text responses  
- images  
- audio streams  
- file/document outputs  
- JSON-mode structured results  
- tool/function-call outputs  

Egress policies often differ from ingress policies, focusing on leakage,
compliance, and safe delivery.

## Step 1 — Output Normalization

Depending on content type:

- **Text:** normalization, metadata tagging  
- **Images:** format validation, metadata stripping, safety signal extraction  
- **Audio:** transcription-based checks if enabled  
- **Files:** MIME checks, extraction, structure validation  
- **Structured outputs:** schema validation and field inspection  

## Step 2 — Egress Policy Evaluation

Egress policies evaluate:

- content safety  
- leakage risk  
- regulatory restrictions  
- prohibited categories  
- ambiguity requiring clarification  
- redaction or transformation rules (if allowed by policy)  

Modality-specific governance (image safety, file restrictions, etc.) is applied here.

## Step 3 — Enforcement Decision

Possible outcomes:

- Return model output unchanged  
- Return a redacted or policy-transformed version (if permitted)  
- Block and return a structured policy decision  
- Trigger clarify-first and return the request to the submitter  

Ambiguous or high-risk responses may follow the same clarification workflow as ingress.

## Step 4 — Return to Client

Approved responses are delivered to the caller.  
All outcomes are logged to audit streams with modality metadata.

---

# 🧩 4. Verifier Integration

The Verifier is a separate, non-execution microservice used when intent is
ambiguous.

It classifies:

- purpose of a request  
- potential harmful categories  
- unclear or dual-use patterns  

If the Verifier cannot classify confidently:

- The runtime returns the request to the submitter for clarification  

Guardrail does **not** execute user content during verification.

---

# 📦 5. Policy Packs

Policy Packs define governance rules for both ingress and egress.

They are:

- Versioned  
- Signed with checksums  
- Immutable after release  
- Audited on activation and rollback  
- Tenant-scoped  

Each pack contains:

- Category definitions  
- Modality rules  
- Regulatory profiles  
- Safety boundaries  
- Checksum metadata  

Policy Packs determine the behavior of both runtime arms.

---

# 🏛 6. Enterprise Runtime Extensions

Enterprise builds on Core by adding:

- Tenant isolation  
- RBAC and operator roles  
- Admin Console  
- Retention and evidence bundling  
- Audit dashboards  
- Signed SBOM artifacts  
- Advanced rate limiting and DLQ controls  

The evaluation engine remains identical to Core.

---

# 🔐 7. Audit Logging

Guardrail emits structured audit logs for:

- Sanitization signals  
- Policy decisions  
- Clarification events  
- Verifier usage  
- Blocked or redacted responses  
- Administrative actions (Enterprise)  
- Modality metadata  

Audit logs support security investigations and governance programs.

---

# 🌐 8. Configuration

Guardrail supports environment-based configuration for:

- LLM provider settings  
- Redis integration  
- Policy Pack sources  
- Verifier endpoints  
- Tenant configuration  
- Observability settings  

Enterprise adds:

- Retention  
- Admin UI config  
- Object store backends  
- RBAC and IAM settings  

---

# 🧪 9. Runtime Positioning

Guardrail does not guarantee safety or compliance.  
It provides a configurable evaluation and governance layer that helps
organizations reduce risk, maintain visibility, and support policy-aligned AI use.

---

# 🆘 10. Support

General inquiries: **enterprise@guardrailapi.com**  
Security disclosures: **security@guardrailapi.com**

---
