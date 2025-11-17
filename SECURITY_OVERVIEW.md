# Guardrail API — Security Overview

> Guardrail Labs, LLC — Patent Pending  
> This document provides a high-level overview of the Guardrail API security model.
> It is intended for architects, security teams, compliance officers, and engineers.

Guardrail API is designed as a **dual-arm AI firewall** that evaluates and governs
LLM traffic in real time. It focuses on:

- Reducing the risk of unsafe or non-compliant prompts and responses  
- Supporting clarify-first handling of ambiguous intent  
- Providing structured, tamper-evident logs for audits and investigations  
- Enforcing tenant isolation and configurable policy packs  

This document does not describe internal implementation details, but instead
summarizes the philosophy and major security mechanisms.

---

## 🧭 1. Security Philosophy

Guardrail is built around a few core principles:

- **Clarify-first** — Ambiguous intent should be clarified, not guessed.  
- **Dual-arm evaluation** — Requests and responses are evaluated independently.  
- **Non-execution verification** — Risk is assessed without running untrusted content.  
- **Tenant isolation** — Each tenant has its own policies, logs, and limits.  
- **Transparent governance** — Policy packs and decisions are logged and auditable.  
- **Defense-in-depth** — Multiple checks (sanitization, policy, verification, audit) work together.

Guardrail is not a guarantee of safety or compliance, but is intended to help
organizations reduce risk and improve oversight of LLM usage.

---

## 🔀 2. Clarify-First & Return-to-Requestor

When a request’s intent is not clearly safe or clearly unsafe, Guardrail follows
a **clarify-first** pattern:

1. The ingress arm flags the request as **ambiguous**.  
2. The Verifier evaluates intent without executing the prompt.  
3. If the Verifier still cannot classify the request with sufficient confidence,  
   the system returns the request to the submitter with a clarification request.  

The system does **not**:

- Blindly pass ambiguous content to the model  
- Execute untrusted instructions  
- Attempt to “guess” user intent when signals are weak  

This pattern is designed to reduce the risk of silently allowing borderline or
misleading prompts through.

---

## 🧱 3. Dual-Arm Evaluation (Ingress & Egress)

Guardrail uses two independent evaluation paths:

- **Ingress Arm** — Checks prompts before they reach the LLM.  
- **Egress Arm** — Checks model outputs before they reach the user.

These arms are intended to operate independently:

- Ingress focuses on **intent, attack patterns, and prompt safety**.  
- Egress focuses on **content, leakage, and policy alignment**.  

If ingress experiences degradation or rate limiting, egress is still designed
to apply output-side policies where possible. This dual-arm model helps detect
issues that might emerge only on the response side (e.g., hallucinated PHI/PII,
unexpected model behavior).

---

## 🧬 4. Unicode, Confusables & Obfuscation

Adversarial prompts often rely on:

- Hidden characters  
- Mixed scripts (Latin, Cyrillic, Greek, etc.)  
- Zero-width spaces  
- Look-alike homoglyphs  

Guardrail incorporates **normalization and confusables detection** to help:

- Normalize certain inputs into a consistent representation  
- Flag suspicious mixes of character classes  
- Provide signals to policy packs and verifiers  

Organizations can adjust how strict these checks are via configuration.
The goal is to surface suspicious encodings, not to block all unusual text.

---

## 🔍 5. Verifier — Non-Execution Intent Evaluation

The Verifier is an optional microservice used when the ingress arm detects that
a request is unclear or potentially risky.

Key properties:

- Evaluates **intent**, not execution results  
- Does **not** run user-supplied code or commands  
- Returns a classification or risk signal to the Guardrail runtime  
- Integrates with policy-defined categories (e.g., “research vs. weaponization”)  

If the Verifier cannot confidently classify the request:

- The runtime returns the request to the submitter for clarification  
- The original ambiguous request is not executed against the model  

The Verifier is intended as an additional safety lens, not a standalone decision-maker.

---

## 📦 6. Policy Packs & Governance

Policy Packs define the rules that govern:

- Which categories of content are allowed or disallowed  
- How regulated data must be treated (e.g., privacy hints, retention hints)  
- How clarification, escalation, or blocking should behave for certain patterns  
- What to log and when to raise incidents  

Policy Packs are:

- **Versioned**  
- **Signed and checksum-validated**  
- **Tenant-specific**  
- **Audited on activation and rollback**  

This enables organizations to:

- Align Guardrail behavior with internal policies  
- Maintain an auditable trail of policy changes  
- Implement different rulesets for different tenants, regions, or applications  

---

## 🧑‍🤝‍🧑 7. Tenancy & Access Control

Guardrail supports **multi-tenant operation**, where each tenant has:

- Separate policy namespaces  
- Separate audit streams  
- Separate quotas and rate limits  
- Separate clarification and incident queues  

Enterprise deployments can additionally use:

- Admin roles with scoped access to specific tenants  
- Read-only roles for auditors or compliance reviewers  
- Admin console views that reflect only the current tenant’s data  

Tenant isolation is a central aspect of the architecture and is reinforced at:

- API surface  
- Policy evaluation  
- Storage and retention  
- Admin UI layers  

---

## 🧾 8. Audit Logging & Retention

Guardrail records **structured, tamper-evident audit logs** for key events:

- Policy evaluation results  
- Sanitization and normalization steps  
- Verifier classifications (where applicable)  
- Clarifications, blocks, and appeals  
- Admin actions (policy changes, rollbacks, tenant updates)  

Enterprise deployments may combine audit logging with:

- Retention windows and data lifecycle policies  
- Exportable evidence bundles for audits  
- Long-term archival in object storage  

Audit logs are designed to support **post-incident investigations**, regulatory
reviews, and internal accountability processes.

---

## 🔐 9. Data Handling Considerations

Guardrail is typically deployed as a gateway in front of one or more LLMs.

Depending on configuration, deployments may:

- See raw user prompts  
- See model responses  
- Store subsets of metadata and content for auditing  
- Store only structured decision records with minimal content fields  

Organizations are responsible for:

- Configuring retention and minimization settings  
- Aligning deployment with internal privacy and security policies  
- Ensuring that logs and exports are handled as sensitive data where applicable  

Enterprise features can assist with these tasks, but final responsibility
remains with the deploying organization.

---

## 🏗 10. Deployment & Hardening (High Level)

Guardrail can be deployed via Docker or Kubernetes with typical hardening steps:

- Restricting admin endpoints behind secure networks or VPNs  
- Enforcing TLS for all external-facing traffic  
- Securing Redis/Postgres/object storage with authentication and network controls  
- Limiting access to logs and evidence bundles  
- Restricting who can modify policy packs or admin settings  

The documentation portal includes more detailed deployment guidance.

---

## 🛡 11. Vulnerabilities & Responsible Disclosure

Guardrail Labs maintains a separate **security policy** document in the
source repositories (`SECURITY.md`) that describes:

- How to report security issues  
- Expected response timelines  
- Disclosure expectations  

In general:

- Vulnerabilities should be reported confidentially  
- Good-faith security research is welcomed within reasonable boundaries  
- Public disclosure should follow a coordinated process  

For high-level questions about this overview, or deployment guidance,
organizations can reach out via:

- **enterprise@guardrailapi.com**  
- **security@guardrailapi.com**

---

*This document is informational and does not modify or extend any license,
service-level agreement, or legal commitments made by Guardrail Labs LLC.*
