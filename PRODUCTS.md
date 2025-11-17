# Guardrail API — Product Overview

> Guardrail Labs, LLC — Patent Pending  
> This document describes the primary components of the Guardrail API platform and
> clarifies their licensing and roles in the system.

The Guardrail API platform is composed of modular components that evaluate AI
traffic, enforce governance policies, support regulatory alignment, and provide
visibility into model behavior. Each component operates independently but can be
combined for full-stack governance.

---

# 🧠 1. Guardrail Core Runtime

**Repository:**  
https://github.com/guardrail-labs/llm-guardrail-api-next

**Edition:**  
**Open Source (Apache 2.0 Licensed)**

**Current Version:**  
**1.5.0**

The Core Runtime is the foundational enforcement engine responsible for
evaluating both **ingress** (requests) and **egress** (responses). It provides
the essential mediation logic used across all Guardrail editions.

### Key Features
- Dual-arm (ingress + egress) traffic evaluation  
- Clarify-first workflow  
- Return-to-requestor handling when intent remains ambiguous  
- Unicode + confusables normalization  
- Policy pack evaluation  
- HMAC-signed audit logging  
- REST API with FastAPI  
- Ideal for local development and self-hosted deployments  

### Common Use Cases
- Developer environments  
- Proof-of-concept integrations  
- Lightweight production enforcement  
- Model gateway experimentation  


---

# 🛡 2. Guardrail Enterprise Runtime

**Repository:**  
Private (licensed customers only)

**Edition:**  
**Proprietary / Commercial License**

**Current Version:**  
**1.4.0**

The Enterprise Runtime extends the Core with governance, compliance, and
multi-tenancy features required for regulated, high-risk, or large-scale AI
deployments.

### Key Features
- Admin Console (incidents, clarifications, policy packs, tenants)  
- Tenant-isolated policy namespaces  
- Clarification queue + appeals workflow  
- Role-based access controls (RBAC)  
- Data retention + evidence bundles  
- Signed SBOM + cosign release artifacts  
- Extended rate limiting, quotas, and DLQ support  
- Kubernetes/Helm production templates  

### Common Use Cases
- Healthcare, finance, government deployments  
- AI gateways requiring compliance controls  
- Multi-tenant SaaS or platform integrations  
- Enterprise-scale governance programs  

Enterprise builds directly on the Core Runtime and is distributed as a
commercially licensed product.

---

# 🔍 3. Guardrail Verifier Service

**Repository:**  
https://github.com/guardrail-labs/guardrail-verifier

**Edition:**  
**Proprietary / Source-Available (public code, not open source)**

**Current Version:**  
**0.2.0**

The Verifier is an optional microservice used when user intent is ambiguous. It
performs **non-execution-based** analysis to help determine whether a request
should proceed or be clarified.

### Responsibilities
- Evaluate request intent without executing user code  
- Detect disguised or dual-stage patterns  
- Provide safety classifications to Core/Enterprise  
- Support policy packs that include verifier rules  

### Clarify-First Behavior
If intent remains unclear after verification:

**→ The request is returned to the user for clarification.**  
The system does not proceed or guess.

### Deployment Modes
- As a standalone microservice  
- As a Kubernetes deployment  
- As a horizontally scalable pool  

The Verifier strengthens ambiguous-request handling while preserving safety.

---

# 📦 4. Guardrail Policy Packs

**Repository:**  
https://github.com/guardrail-labs/llm-guardrail-policy-packs

**Edition:**  
**Proprietary / Source-Available (public code, not open source)**

**Current Version:**  
**1.0.0**

Policy Packs define governance rules used by Core and Enterprise. They are
publicly accessible for transparency, but remain proprietary under Guardrail
Labs’ license.

### What Policy Packs Contain
- Safety and governance rules  
- Regulatory templates (GDPR, HIPAA, AI-Act profiles)  
- Industry-specific rule sets  
- Metadata: signatures, checksums, version  
- Optional verifier integration hints  
- Tenant-namespace support  

### Characteristics
- Signed and versioned  
- Immutable once published  
- Diffable in the Enterprise UI  
- Activation and rollback fully audited  
- Tenant-isolated  

### Example Uses
- Sensitive data handling controls  
- Safety categories for LLM prompts  
- Governance boundaries for agent systems  
- Compliance-aligned enforcement templates  

---

# 🔗 5. How Products Work Together

Client
↓
Ingress Guard (Core or Enterprise)
↓ ↘ (if ambiguous)
Verifier ↘ return to user if unclear
↓
LLM Provider
↓
Egress Guard (Core or Enterprise)
↓
Client


### Core Runtime  
Provides the evaluation engine.

### Enterprise Runtime  
Adds governance + multi-tenancy + admin controls.

### Verifier  
Handles ambiguous-intent classification.

### Policy Packs  
Define the rules each runtime enforces.

Together, they form a configurable, dual-arm AI mediation platform.

---

# 🧭 6. Selecting the Right Components

| Requirement | Component |
|------------|-----------|
| Local development | Core Runtime |
| Production governance | Enterprise Runtime |
| Ambiguous intent handling | Verifier |
| Safety + compliance rules | Policy Packs |
| Deployment automation | Umbrella CLI |

---

© Guardrail Labs LLC 2025. All rights reserved.
