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

When a user sends a prompt through Guardrail:

### Step 1 — Normalization & Sanitization
The runtime performs:
- Unicode normalization  
- Confusables / homoglyph checks  
- Simple pattern checks for obfuscation  

Signals are attached to the evaluation context.

### Step 2 — Policy Pack Evaluation
Policies determine:
- Allowed categories  
- Disallowed patterns  
- Required clarifications  
- Regulatory boundaries  

If a rule triggers clarification → move to Step 3.  
If a rule triggers immediate denial → block and log.  
If allowed → proceed normally.

### Step 3 — Clarify-First Workflow
If intent is ambiguous:
- The Verifier may be consulted for non-execution analysis  
- If still unclear → the request is returned to the submitter  
- The system does not guess user intent  

Only when intent is clear does the request proceed.

### Step 4 — Forward to LLM
The sanitized, policy-checked prompt is sent to the configured LLM provider.

---

# 🔄 3. Response Lifecycle (Egress)

After the LLM generates a response:

### Step 1 — Content Normalization
Light normalization and metadata tagging may apply.

### Step 2 — Egress Policy Evaluation
Policies evaluate:
- Safety categories  
- Leakage indicators  
- Disallowed content  
- Regulatory restrictions  

The egress arm may block, modify, or clarify, depending on policy.

### Step 3 — Return to Client
If approved, the response returns to the user.  
If not, the runtime returns a policy decision instead.

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
