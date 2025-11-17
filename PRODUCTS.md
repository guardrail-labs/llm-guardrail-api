# Guardrail API — Product Overview

> Guardrail Labs, LLC — Patent Pending  
> This document describes the four primary components of the Guardrail API platform.

The Guardrail API platform is composed of modular, interoperable components that work
together to evaluate LLM traffic, enforce governance rules, support regulatory alignment,
and provide visibility into AI interactions.

Each component can be adopted independently or deployed together for full-stack coverage.

---

# 🧠 1. Guardrail Core Runtime

**Repository:** https://github.com/guardrail-labs/llm-guardrail-api-next  
**Edition:** Open Source  
**Current Version:** 1.5.0

The Core Runtime provides the foundational enforcement engine for Guardrail, including:

### Features
- **Dual-arm traffic evaluation** (ingress + egress)  
- **Clarify-first intent assessment workflow**  
- **Return-to-requestor loop** when intent cannot be determined  
- **Unicode / confusables detection**  
- **Policy pack evaluation**  
- **HMAC-signed audit logging**  
- **Tenant header handling**  
- **Local development + testing support**  

### Use Cases
- Developer prototyping  
- Local enforcement gateways  
- Lightweight production deployments  
- Sandbox runtimes  

### Sub-components
- FastAPI application  
- Request/response mediators  
- Policy evaluation layer  
- Basic telemetry endpoints  

The Core Runtime is a dependency of every Guardrail edition.

---

# 🛡 2. Guardrail Enterprise Runtime

**Repository:** Private (licensed customers only)  
**Edition:** Commercial  
**Current Version:** 1.4.0

The Enterprise edition adds governance, compliance, and operational tooling required for
high-risk or regulated deployments.

### Features
- **Dual-arm isolation model** with separate ingress/egress paths  
- **Admin Console** (incidents, clarifications, appeals, tenants, policy packs)  
- **Tenant isolation and per-tenant policy namespaces**  
- **Signed SBOM + cosign release artifacts**  
- **Evidence bundles for SOC 2 and GDPR/AI-Act alignment**  
- **Extended retention + data lifecycle support**  
- **Clarification queue viewer and admin review workflows**  
- **Role-based access controls (RBAC)**  

### Use Cases
- Regulated environments (healthcare, government, finance)  
- Enterprise model gateways  
- Multi-tenant SaaS offerings  
- Audit-heavy deployments  

### Integrations
- Redis (quotas, rate limiting, DLQ)  
- Postgres (retention and audit stores)  
- Object storage (long-term evidence)  
- Kubernetes + Helm charts  

Enterprise builds directly on the Core Runtime to provide a complete AI governance platform.

---

# 🔍 3. Guardrail Verifier Service

**Repository:** https://github.com/guardrail-labs/guardrail-verifier  
**Edition:** Proprietary (public source access)  
**Current Version:** 0.2.0

The Verifier is an optional microservice used when **intent is ambiguous**.

It evaluates the request **without executing it** and provides a classification to the Core or Enterprise runtime.

### Responsibilities
- Analyze ambiguous inputs  
- Detect dual-intent patterns  
- Determine whether a request should proceed or be clarified  
- Provide structured, non-execution-based safety signals  
- Integrate with policy packs that define verifier categories  

### Clarify-First Workflow
If a request’s intent remains unclear after verification:

**→ It is returned to the user for clarification.**  
The system does not guess, bypass rules, or execute untrusted content.

### Deployment
- As a sidecar  
- As a Kubernetes microservice  
- As a horizontally scaled pool  

The Verifier improves accuracy for complex queries while maintaining safety boundaries.

---

# 📦 4. Guardrail Policy Packs

**Repository:** https://github.com/guardrail-labs/llm-guardrail-policy-packs  
**Edition:** Proprietary (public source access)   
**Current Version:** 1.0.0

Policy Packs define the rules that govern how Guardrail evaluates prompts and responses.

### Contents
- Safety rules  
- Regulatory profiles (GDPR, HIPAA, AI-Act)  
- Industry-specific templates (healthcare, finance, government)  
- Version metadata  
- Checksums + signatures  
- Optional verifier integration settings  

### Properties
- Signed and versioned  
- Immutable once published  
- Diffable in the Enterprise UI  
- Tenant-isolated  
- Activation and rollback are fully audited  

### Examples
- Privacy-handling rules  
- Safety categories for LLM interactions  
- Sensitive data protections  
- Content boundary controls  

Policy Packs make governance **configurable**, not hard-coded.

---

# 🔗 5. How the Products Fit Together

Client → Ingress Guard (Core/Enterprise)
→ Verifier (optional)
→ LLM Provider
→ Egress Guard (Core/Enterprise)
→ Client


### Core
Performs evaluation and mediation.

### Enterprise
Adds governance, compliance, multi-tenancy, and operational controls.

### Verifier
Provides intent clarification for risky or ambiguous prompts.

### Policy Packs
Define the rules each component uses during evaluation.

---

# 🧭 6. Choosing an Edition

| Need | Recommended Component |
|------|------------------------|
| Local development or POC | Core Runtime |
| Full enterprise governance | Enterprise Runtime |
| Complex ambiguous prompts | Verifier |
| Safety/compliance rules | Policy Packs |

---

© Guardrail Labs LLC 2025. All rights reserved.
