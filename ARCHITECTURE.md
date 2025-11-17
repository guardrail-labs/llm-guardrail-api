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


**Dual-arm model:**  
Ingress and egress operate through **separate evaluation paths**.  
If the ingress path is degraded, the egress arm is designed to continue applying output-side governance whenever possible.

---

## 🧱 2. Ingress Guard (Request Mediation)

The ingress arm evaluates prompts before they reach the model.

### Responsibilities
- Normalize text and detect hidden characters  
- Evaluate rules defined in policy packs  
- Identify ambiguous or high-risk intent  
- Determine whether verification is needed  
- Apply tenant-specific quotas, rate limits, and restrictions  

### Possible Outcomes
- **Clean →** forwarded to model  
- **Requires clarification →** verifier assesses intent  
- **Still unclear →** request returned to the user for clarification  
- **Blocked →** user receives a safe, policy-aligned denial  
- **Escalated →** recorded as an incident for admin review  

All decisions are written to the HMAC-signed audit log.

---

## 🔁 3. Verifier Layer (Intent Evaluation)

The verifier analyzes content **without executing it** and is used when intent is ambiguous.

### What the Verifier Does
- Classifies whether intent is safe or harmful  
- Determines if executing the prompt would pose risk  
- Detects disguised or dual-intent patterns  
- Provides a safe evaluation result to the ingress guard  

### If Verifier Cannot Determine Intent
If the verifier cannot determine intent with sufficient confidence:

**→ The request is returned to the submitter for clarification.**

The system does *not* proceed or guess.

### What the Verifier Never Does
- Never executes user instructions  
- Never forwards content to tools or external systems  
- Never bypasses Guardrail policy enforcement  

---

## 📤 4. Egress Guard (Response Mediation)

The egress arm evaluates LLM output before it reaches the user.

### Responsibilities
- Apply policy rules to model responses  
- Detect harmful or disallowed model behaviors  
- Identify accidental data leakage  
- Evaluate hallucination-prone or unsafe categories  
- Support compliance indicators (PHI/PII, GDPR-relevant text)  

### Behavior
The egress arm operates independently from ingress and continues to apply output-side evaluation even in scenarios where ingress may be degraded.

---

## 📦 5. Policy Packs

Policy Packs are signed, versioned bundles of governance rules.

Policy Packs include:
- Safety and risk rules  
- Regulatory profiles (GDPR, HIPAA, AI-Act)  
- Industry presets  
- Metadata: signature, checksum, version, tenant namespace  

Characteristics:
- Immutable once signed  
- Versioned and diffable  
- Independently deployable  
- Tenant-isolated  
- Fully audited on activation or rollback  

---

## 🧑‍🤝‍🧑 6. Tenancy & Isolation

Each tenant operates in a **fully isolated governance environment**:

- Dedicated policy namespace  
- Independent audit log stream  
- Separate clarification and incident queues  
- Independent circuit breaker and quota settings  
- Optional tenant-specific verifiers  

No tenant can access another tenant’s data or policies.

---

## 🧾 7. Audit, Retention & Evidence

Guardrail produces structured, tamper-evident audit logs containing:

- Request/response metadata  
- Policy evaluation results  
- Sanitization outcomes  
- Verification results  
- Admin actions  
- Activation/rollback of policy packs  

Optional modules support:

- Retention windows  
- GDPR/AI-Act deletion workflows  
- Long-term log archival to S3/MinIO/GCS  
- SOC 2 evidence generation  

---

## 🏗 8. Deployment Architecture

Guardrail can be deployed in multiple modes:

### Local / Docker
Simple evaluation environments.

### Kubernetes / Helm (Recommended)
Supports:
- Horizontal scaling  
- Multi-tenant deployments  
- Redis, Postgres, and object storage backends  
- Verifier autoscaling  

### Sidecar / Gateway
Can operate as:
- API-level firewall  
- Reverse proxy filter  
- Model gateway  
- Edge mediation layer  

### Multi-Model Routing
Supports:
- OpenAI  
- Anthropic  
- Azure OpenAI  
- Vertex  
- Local models  

Routing is tenant-specific.

---

## 🔐 9. Security Model (High-Level)

Guardrail uses the following high-level security principles:

- **Clarify-first** → ambiguous requests require intent clarification  
- **Return-to-requestor loop** for unresolved ambiguity  
- **Non-execution verification**  
- **Independent ingress/egress mediation paths**  
- **Unicode/confusables normalization**  
- **Tamper-evident audit logging (HMAC)**  
- **Tenant isolation across all layers**  
- **Optional SOC 2–aligned controls in Enterprise edition**  

For a broader overview, see `SECURITY_OVERVIEW.md`.

---

## 🧭 10. Component Map

| Component | Purpose |
|----------|---------|
| **Core Runtime** | Open-source ingress + egress mediation engine |
| **Enterprise Runtime** | Hardened edition with admin UI, retention, compliance tooling |
| **Verifier** | Intent evaluation when requests are unclear |
| **Policy Packs** | Signed governance bundles |
| **Umbrella CLI (`guardrailctl`)** | Installation, validation, artifact coordination |

---

© Guardrail Labs LLC 2025. All rights reserved.

