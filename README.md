# Guardrail API — Patent Pending  
**Real-Time AI Firewall for Large Language Models**  
Built and maintained by **Guardrail Labs, LLC**

Guardrail API is an open-source, real-time enforcement engine that protects your LLM applications by evaluating both **ingress (prompts)** and **egress (model responses)** for safety, misuse, and policy alignment.

It is lightweight, deterministic, and provider-agnostic — compatible with OpenAI, Anthropic, Google, and all major model APIs.

---

## 🔒 Why Guardrail API?

Modern LLM applications face risks:

- Unsafe or high-risk prompts  
- Jailbreak attempts and adversarial input  
- Leaking sensitive or disallowed information  
- Inconsistent or unpredictable safety filters  
- Lack of auditability for compliance and governance  

Guardrail API solves this by acting as an **AI Firewall** that performs:

- **Ingress evaluation** (before prompts reach the model)  
- **Egress evaluation** (before responses hit the user)  
- **Structured allow/deny decisions**  
- **Explainable reasons and categories**  
- **Strong audit evidence for SOC 2, GDPR, HIPAA, and AI-risk frameworks**

Guardrail API is the foundation layer of the Guardrail ecosystem — security, safety, and governance built in from day one.

---

## 🚀 Quickstart

Install:

```bash
pip install llm-guardrail-api
```
Run the API:

```bash
guardrail serve
```
Send a decision request:

```bash
Copy code
curl -X POST http://localhost:8000/decision \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-4",
        "ingress": { "text": "Write malware" }
      }'
```
Example response:
```
json
Copy code
{
  "allowed": false,
  "category": "unsafe_intent",
  "reason": "The request appears designed to produce harmful or malicious output."
}
```
---

## 🧩 Core Features
Dual-arm policy enforcement (prompts + responses)

Configurable rules and evaluation profiles

Deterministic, explainable safety decisions

Provider-agnostic design

Streaming-safe enforcement

FastAPI + Python runtime

Structured incident reporting

Lightweight and production-ready

---

## 📚 Documentation
Complete documentation for Guardrail API is available at:

👉 https://guardrailapi.com/docs

You’ll find:

Core concepts

API reference

Prompt/response evaluation examples

Deployment guidance

Integration patterns

Decision model details

This is the authoritative source of truth for the Guardrail API.

---
🛠 Developer Setup
Clone and install:

```bash
Copy code
git clone https://github.com/guardrail-labs/llm-guardrail-api.git
cd llm-guardrail-api
pip install -e .
```
Run the test suite:

```bash
pytest
```
---

## 📄 License
Guardrail API (Core Runtime) is licensed under the Apache 2.0 License.

This applies only to the open-source core.
Other Guardrail Labs components and policy packs may carry different license terms.

---
## 🏢 About Guardrail Labs, LLC
Guardrail Labs, LLC builds security, safety, and risk-governance infrastructure for AI systems in enterprise environments.
Our mission is to help organizations deploy AI responsibly — with transparency, auditability, and real-time protection.

🌐 Website: https://guardrailapi.com

📧 info@guardrailapi.com

🛡 Guardrail API — Patent Pending

© Guardrail Labs, LLC. All rights reserved.
