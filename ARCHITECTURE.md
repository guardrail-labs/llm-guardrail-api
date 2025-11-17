# Guardrail API — System Architecture

> Guardrail Labs, LLC — Patent Pending  
> This document provides a high-level, public-safe overview of the Guardrail API platform.

Guardrail API is a **dual-arm AI security firewall** that mediates traffic between end-users and large language models (LLMs). It enforces policy packs, detects ambiguous or malicious intent, verifies questionable requests, and records tamper-evident audit logs for compliance.

The architecture is composed of four major layers:

1. **Ingress Arm** — validates and governs inputs  
2. **Egress Arm** — validates and governs model outputs  
3. **Verifier Service** — resolves unclear intent without executing user content  
4. **Governance Layer** — policy packs, tenants, retention, and audit integrity  

This document explains how these layers operate in a unified runtime.

---

## 🧩 1. High-Level Architecture Diagram

       ┌──────────────────────────────┐
       │        Client / App          │
       └──────────────┬───────────────┘
                      │
                      ▼
            ┌───────────────────────┐
            │     Ingress Guard     │
            │  (policies + checks)  │
            └────────────┬──────────┘
                         │
      Clarify / Verify?  │
        (if needed)      │
                         ▼
                  ┌───────────────┐
                  │   Verifier    │
                  │ (LLM or rules)│
                  └───────┬───────┘
                          │
            ┌─────────────┴─────────────┐
            │        LLM Provider        │
            └─────────────┬─────────────┘
                          │
                          ▼
            ┌───────────────────────────┐
            │        Egress Guard       │
            │   (response governance)   │
            └─────────────┬─────────────┘
                          │
                          ▼
       ┌──────────────────────────────┐
       │      Client / Application    │
       └──────────────────────────────┘

**Key idea:**  
Even if the ingestion path experiences degradation or rate-limiting, the egress arm is designed to operate independently and continue applying output-side governance.

This reflects Guardrail’s dual-arm isolation model, where each arm evaluates traffic separately rather than depending on the other.


---

## 🧱 2. Ingress Guard (Request Mediation)

The ingress arm protects the model from:

- Unsafe or harmful prompts  
- Hidden text attacks (Unicode, confusables)  
- Jailbreak patterns  
- Misleading multi-stage requests  
- Data leakage attempts  
- Ambiguous intent from unknown users  

### Responsibilities

- Normalize and sanitize user input  
- Detect suspicious directives  
- Enforce policy pack rules  
- Trigger verification when intent is unclear  
- Rate-limit or circuit-break based on tenant quotas  

### Outcomes

A request can be:

- **Clean** → forwarded to the LLM  
- **Clarified** → sent to verifier  
- **Blocked** → user receives a safe denial message  
- **Escalated** → logged as an incident for admin review  

All decisions are added to the HMAC-signed audit log.

---

## 🔁 3. Verifier Layer (Intent Evaluation)

The Verifier performs **non-execution-based** analysis of a request when the ingress arm identifies unclear or suspicious intent.

### What it does

- Determines whether executing the request could harm the model, user, or system  
- Confirms whether hidden instructions or dual-intent patterns exist  
- Provides the Guardrail decision engine with a safe recommendation  

### What it *does not* do

- Never executes untrusted user code  
- Never forwards content to external tools  
- Never evaluates harmful instructions  
- Never bypasses Guardrail policy packs  

### When used

- Unclear intent (e.g., “explain malware vs write malware”)  
- Potential data exfiltration patterns  
- Dual-stage payloads or agentic prompts  
- Suspiciously encoded content  

If the verifier is unavailable, Guardrail applies **conservative blocking**.

---

## 📤 4. Egress Guard (Response Mediation)

The egress arm protects the **user** and **organization** from unsafe or prohibited model output.

Egress enforcement runs even if ingress is unavailable, providing:

- Independent circuit breakers  
- Independent policy evaluation  
- Guaranteed output governance  

### Responsibilities

- Enforce output-side policy packs  
- Detect hallucinations, unsafe content, or accidental leakage  
- Govern regulated data behaviors (PHI/PII indicators, GDPR signals)  
- Capture evidence for audits  
- Trigger clarifications or admin review on risky responses  

Egress is the last line of defense before content reaches the user.

---

## 📦 5. Policy Packs

Policy Packs define the governance rules for both arms.

Each pack contains:

- Safety rules  
- Compliance profiles (GDPR, HIPAA, AI-Act)  
- Industry-specific policies  
- Metadata, version, signatures, and checksums  
- Tenant-isolated namespaces  

Policy packs are:

- **Signed**
- **Versioned**
- **Diffable**
- **Rollback-safe**
- **Tenant-isolated**

Admin Console allows pack inspection, diffing, and activation.

---

## 🧑‍🤝‍🧑 6. Tenancy & Isolation

Each tenant receives a fully isolated policy and data environment:

- Policy namespaces  
- Audit logs  
- Quotas and rate limits  
- Clarification and appeals queues  
- Circuit breaker states  
- Optional verifier settings  

No cross-tenant visibility is permitted, even for admins.

Tenant separation is enforced at:

1. Ingress guard  
2. Egress guard  
3. Policy packs  
4. Audit retention  
5. Admin UI access  

---

## 🧾 7. Audit, Retention & Evidence

Every decision recorded by Guardrail generates an **HMAC-signed audit event.**

Events include:

- Request/response metadata  
- Policy results  
- Sanitization decisions  
- Verification details  
- Admin actions  
- Rollbacks and pack loads  

Optional modules support:

- Retention policies  
- GDPR/AI-Act data deletion requests  
- SOC 2 evidence bundles  
- Long-term log archival  

Audit integrity is cryptographically guaranteed.

---

## 🏗 8. Deployment Architecture

Guardrail can be deployed in:

### ✔ Local / Docker Mode  
Ideal for development and testing.

### ✔ Kubernetes / Helm  
Recommended for production.  
Supports:

- Horizontal scaling  
- Multi-tenant environments  
- Verifier autoscaling  
- Redis, Postgres, S3 backends  

### ✔ Sidecar or Gateway Mode  
Guardrail can act as:

- A standalone gateway service  
- An API-level firewall  
- A sidecar to application pods  
- A reverse proxy filter layer  

### ✔ Multi-Model Architecture  
Supports routing to:

- OpenAI  
- Anthropic  
- Azure OpenAI  
- Vertex  
- Local models  

Routing rules are defined per tenant and per policy.

---

## 🔐 9. Security Model (High-Level)

- **Clarify-first** → ambiguity results in verification  
- **Two-tier blocking** → safe denial + escalation paths  
- **No execution of user code** at any stage  
- **Unicode/confusables detection** on ingress  
- **Independent ingress/egress enforcement**  
- **Tamper-evident audit log** via HMAC  
- **Verifier fallback safety**  
- **Strict tenant isolation**  
- **SOC 2–aligned controls** in Enterprise edition  

For a detailed overview, see `SECURITY_OVERVIEW.md`.

---

## 🧭 10. Component Map

| Component | Purpose |
|----------|---------|
| **Core Runtime** | Open-source policy evaluation and dual-arm mediation |
| **Enterprise Runtime** | Hardened edition with admin UI, retention, SOC 2 controls |
| **Verifier** | Intent clarification and risk assessment |
| **Policy Packs** | Signed governance bundles |
| **Umbrella CLI (`guardrailctl`)** | Installation, verification, artifact management |

---

© Guardrail Labs LLC 2025. All rights reserved.
