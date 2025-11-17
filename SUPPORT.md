# Guardrail Labs — Support Guide

> Guardrail Labs, LLC — Patent Pending  
> This document describes how to request help, report issues, and obtain
> support for the Guardrail API platform.

Guardrail Labs provides different support paths depending on the component used
(open-source, source-available, or proprietary).  
This guide outlines where to report issues and how to contact our team.

---

# 🧭 1. Support for Open Source Components

The following repositories are open source:

- **llm-guardrail-api-next** (Core Runtime)
- **llm-guardrail-api** (Umbrella Docs & CLI)

For these, the recommended support path is:

### ✔ GitHub Issues (preferred)
Use GitHub Issues for:
- bug reports  
- documentation corrections  
- reproducible runtime problems  
- feature suggestions  

Provide:
- version used  
- steps to reproduce  
- expected vs. actual behavior  
- environment details (Docker, Uvicorn, OS)  

### ✔ Discussions (community use)
Some repositories provide GitHub Discussions for general questions.

Open-source support is provided on a best-effort basis and does not include
SLA guarantees.

---

# 🔒 2. Support for Source-Available Components

The following repositories are source-available under a proprietary license:

- **guardrail-verifier**
- **llm-guardrail-policy-packs**

For these components:

### ✔ Support Channel
Email: **info@guardrailapi.com**

Guardrail Labs provides guidance for:
- integrating the Verifier  
- understanding policy pack behavior  
- questions about usage under the Guardrail Labs license  

Source-available components do **not** include commercial SLAs unless paired
with an Enterprise agreement.

---

# 🏛 3. Support for Enterprise Components

The following components are proprietary and covered under commercial licensing:

- **llm-guardrail-api-enterprise**  
- Enterprise retention systems  
- Admin Console  
- Governance, evidence, and RBAC features  

Enterprise customers receive prioritized support.

### ✔ Primary Support Channel
Email: **enterprise@guardrailapi.com**

Use this channel for:
- onboarding  
- deployment questions  
- operational support  
- retention & evidence configuration  
- RBAC and tenant administration  
- Helm/Kubernetes deployments  

### ✔ Security Disclosures
Email: **security@guardrailapi.com**

Use this channel for:
- vulnerability reports  
- security concerns  
- observed anomalies in production  
- coordinated disclosure  

Guardrail Labs follows responsible disclosure practices.

---

# 🛠 4. Diagnostic Information to Include

To help us assist you efficiently, please include (when applicable):

- component version(s)  
- deployment mode (Docker, Kubernetes, Uvicorn)  
- logs or audit entries (redacted)  
- policy pack versions used  
- tenant configuration (redacted)  
- steps to reproduce or time of occurrence  
- details on any verifier involvement  
- details on failed ingress or egress decisions  

For sensitive environments (regulated workloads), contact us before sharing
logs or artifacts so we can provide a secure upload channel.

---

# 📦 5. Production Support Expectations

Enterprise customers receive:

- prioritized response  
- deployment guidance  
- best practices for policy packs  
- capacity and scaling recommendations  
- retention and evidence bundle guidance  
- clarification on tenant and RBAC design  
- assistance interpreting audit events  

Open-source and source-available components receive best-effort support
through GitHub issues or the general contact address.

---

# 📬 Contact Summary

- **General / Source-Available Support:**  
  **info@guardrailapi.com**

- **Enterprise Support:**  
  **enterprise@guardrailapi.com**

- **Security Disclosures:**  
  **security@guardrailapi.com**

---

© Guardrail Labs LLC 2025. All rights reserved.
