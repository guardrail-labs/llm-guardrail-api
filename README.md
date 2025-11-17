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

## 🏗 Platform Components

The Guardrail platform is delivered through four coordinated repositories:

### **1. Umbrella & CLI (`llm-guardrail-api`)**
This repo.  
Provides:

- MkDocs documentation portal  
- `guardrailctl` CLI (installation, validation, rendering)  
- Deployment templates and examples  
- Architecture and integration docs  

### **2. Core Runtime (`llm-guardrail-api-next`)**
Open-source enforcement engine providing:

- Ingress/egress mediation  
- Policy evaluation  
- Unicode/confusable detection  
- Clarify-first verification workflow  
- HMAC-signed audit logging  

Ideal for local development, POCs, and lightweight deployments.

### **3. Enterprise Runtime (`llm-guardrail-api-enterprise`)**
Private, commercially licensed edition with:

- Dual-arm circuit isolation  
- Signed SBOM bundles & cosign artifacts  
- Tenant-isolated policy namespaces  
- Admin UI (incidents, appeals, packs, quotas)  
- Compliance and retention tooling  
- SOC 2 aligned controls  

Not publicly accessible; integrated through the CLI.

### **4. Policy Packs (`llm-guardrail-policy-packs`)**
Curated, signed bundles of:

- Safety rules  
- Regulatory profiles (GDPR, HIPAA, AI-Act)  
- Industry presets  
- Internal governance templates  

Policy Packs can be promoted and versioned independently.

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
