# Guardrail API — Umbrella Project

[![Docs](https://img.shields.io/badge/docs-live-blue)](https://guardrail-labs.github.io/llm-guardrail-api/)
![Core](https://img.shields.io/badge/Core-1.5.0-green)
![Enterprise](https://img.shields.io/badge/Enterprise-1.4.0-green)
![Verifier](https://img.shields.io/badge/Verifier-0.2.0-green)
![Policy Packs](https://img.shields.io/badge/Policy_Packs-1.0.0-green)

> **Guardrail Labs, LLC — Patent Pending**  
> A unified platform for AI security, governance, and compliance.

---

## 🧠 What is the Guardrail API?

Guardrail API is a **dual-arm AI security firewall** that sits between your applications
and large language models (LLMs). It inspects and governs:

- **Ingress** — prompts *entering* a model  
- **Egress** — responses *leaving* a model  

The system enforces policy packs, detects unsafe or ambiguous intent,
and produces signed audit trails that support SOC 2, GDPR, HIPAA, and EU AI-Act alignment.

This umbrella repository provides:

- The **documentation portal**  
- The **`guardrailctl` CLI**  
- Deployment templates  
- Integration guides  
- Platform architecture documentation  

All other Guardrail components plug into this umbrella.

---

## 🧱 Platform Components

Guardrail is delivered through four coordinated repositories maintained by
Guardrail Labs:

### **1. Core Runtime — `llm-guardrail-api-next` (Open Source)**  
Dual-arm enforcement engine supporting:
- multimodal ingress/egress evaluation  
- policy pack execution  
- clarify-first logic  
- optional verifier integration  

This is the foundation for all Guardrail deployments.

---

### **2. Enterprise Runtime — `llm-guardrail-api-enterprise` (Proprietary)**  
Adds governance, compliance, and operational controls, including:
- multi-tenant administration  
- RBAC  
- retention and evidence bundles  
- audit dashboards  
- signed artifacts and SBOMs  
- enhanced rate limiting / DLQ / quotas  

The evaluation engine matches Core; Enterprise extends operations and governance.

---

### **3. Verifier Service — `guardrail-verifier` (Source-Available)**  
A non-execution intent-classification microservice used when requests are
ambiguous.  
Supports:
- modality-aware intent analysis  
- clarify-first workflows  
- policy-driven ambiguity handling  

The Verifier never executes user-submitted content.

---

### **4. Guardrail Policy Packs — `llm-guardrail-policy-packs` (Source-Available)**  
Versioned, signed, auditable rule bundles containing:
- safety categories  
- modality rules (text/image/audio/file)  
- regulatory profiles (GDPR, HIPAA, AI Act templates)  
- organization-specific governance logic  

Policy Packs define the rule surface the runtime enforces.


---

## 📚 Documentation Portal

The complete product documentation is available at:

### **https://guardrail-labs.github.io/llm-guardrail-api/**

It includes:

- Installation guides for Core & Enterprise  
- Architecture diagrams  
- Clarifications + appeals workflow  
- Admin UI tour  
- Tenancy & RBAC  
- Policy pack management  
- Verifier integration  
- SOC 2 evidence collection  
- CLI reference  

This portal is the recommended starting point for all users.

---

## 🚀 Install the CLI

Use `pipx` for an isolated installation:

```bash
pipx install git+https://github.com/guardrail-labs/llm-guardrail-api.git
```

Install locally while developing:
```
python -m pip install -U pip
pip install -e .

```

## 🔧 Common guardrailctl Commands

List channels and verify releases (Core example)
```
guardrailctl channels list
guardrailctl verify --edition core --tag v1.5.0
```

Install a component to a target directory
```
guardrailctl install --edition core --tag v1.5.0 --dest /opt/guardrail
```

Generate deployment assets
```
guardrailctl compose init --dest /opt/guardrail
mkdir -p manifests
guardrailctl helm render --out ./manifests
```
---

🏛 Licensing Model

Core Runtime — open source (Apache 2.0)

Verifier Service — source-available (non-commercial license)

Policy Packs — source-available (non-commercial license)

Enterprise Runtime — proprietary commercial license

This repository (Umbrella) is licensed under Apache 2.0 and contains no
proprietary logic from the Enterprise edition.
---

## 🛡 About Guardrail Labs
Guardrail Labs builds AI security, safety, and governance infrastructure.
Our mission is to help teams deploy AI responsibly — with transparency,
accountability, and compliance built in.

To learn more or contact us:
enterprise@guardrailapi.com
security@guardrailapi.com

© Guardrail Labs LLC 2025. All rights reserved.
