# Guardrail Labs — Security Policy

> Guardrail Labs, LLC — Patent Pending  
> This document describes how to report vulnerabilities and how security
> communications should be handled for Guardrail API components.

Guardrail Labs is committed to responsible communication practices and
collaboration with the security community.  
While the Guardrail platform does not guarantee prevention of security risks,
we aim to provide transparent channels for reporting and addressing issues.

---

# 🧭 1. Scope

This policy applies to the following repositories:

### ✔ Open Source (MIT / Apache 2.0)
- `llm-guardrail-api` (Umbrella Docs & CLI)
- `llm-guardrail-api-next` (Core Runtime)

### ✔ Proprietary / Source-Available
- `guardrail-verifier`
- `llm-guardrail-policy-packs`

### ✔ Proprietary / Commercial
- `llm-guardrail-api-enterprise`

Vulnerabilities, suspected weaknesses, or unexpected runtime behavior may be
reported for any of the above components.

---

# 🧱 2. Reporting a Vulnerability

To report a security issue, contact us at:

### **security@guardrailapi.com**  
Subject line:  
`SECURITY DISCLOSURE – <Short Description>`

Please include (to the extent possible):
- Component and version  
- Steps to reproduce  
- Relevant logs or audit events (with sensitive data removed)  
- Any clarifying details about your environment  

Do **not** submit vulnerabilities through GitHub Issues or pull requests.

Guardrail Labs will acknowledge receipt and follow up for additional details
if needed.

---

# ⚖️ 3. Responsible Disclosure

Guardrail Labs follows industry-standard responsible disclosure practices:

- No punitive action for **good-faith** security research  
- We request researchers give us reasonable time to investigate  
- If appropriate, fixes will be published in a documented release  
- Credit may be provided (optional)  
- Premature public disclosure may limit our ability to respond  
- Proprietary systems will be patched through licensed distribution channels  

If a reported issue affects multiple Guardrail components, we may coordinate
a cross-repository advisory.

---

# ⛔ 4. Out-of-Scope Findings

The following do **not** fall under this security policy:

- Social engineering attacks  
- Physical security issues  
- Vulnerabilities in third-party LLM providers  
- Issues requiring administrative or root access  
- Findings in modified or self-patched versions of Guardrail  
- Policy misconfiguration by the user or tenant operator  

We may still provide guidance on remediation where possible.

---

# 🛡 5. Coordination for Enterprise Customers

Licensed Enterprise customers may request:

- private coordination channels  
- assistance validating security behaviors  
- deployment hardening recommendations  
- tenant-isolation or RBAC reviews  
- retention and audit configuration checks  

Enterprise inquiries should be directed to:

### **enterprise@guardrailapi.com**

---

# 📬 Contact Summary

- **Security disclosures:**  
  `security@guardrailapi.com`

- **Enterprise support:**  
  `enterprise@guardrailapi.com`

- **General inquiries:**  
  `info@guardrailapi.com`

---

© Guardrail Labs LLC 2025. All rights reserved.
