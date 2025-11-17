# Guardrail API — Frequently Asked Questions (FAQ)

> Guardrail Labs, LLC — Patent Pending  
> This FAQ provides a high-level overview of the Guardrail platform and answers
> common questions about behavior, architecture, and deployment.

---

## 1. What is the Guardrail API?

Guardrail API is a real-time governance and safety layer that sits between
clients and large language models (LLMs). It evaluates both prompts (ingress)
and model responses (egress) to help organizations reduce risk, improve
oversight, and enforce policy.

Guardrail does not replace an LLM. It governs how models are used.

---

## 2. How does Guardrail evaluate prompts and responses?

Guardrail uses two independent evaluation paths:

- **Ingress Arm** — evaluates requests, clarifies intent, checks policy.  
- **Egress Arm** — evaluates model responses for safety and leakage.  

The arms operate independently so that egress protections continue even if
ingress is degraded or rate-limited.

---

## 3. What happens when Guardrail cannot tell what the user intends?

Guardrail follows a **clarify-first** workflow:

1. The ingress arm marks the request as ambiguous.  
2. The Verifier evaluates intent without executing user content.  
3. If intent cannot be clearly classified,  
   the request is returned to the submitter for clarification.  

The system does not guess or proceed with unclear intent.

---

## 4. Does Guardrail execute user-supplied code or commands?

No.  
The Guardrail runtime and Verifier perform **non-execution analysis only**.
Execution of untrusted commands is never performed as part of evaluation.

---

## 5. What are Policy Packs?

Policy Packs are versioned rule bundles that define:

- safety boundaries  
- governance rules  
- content categories  
- regulatory templates (HIPAA, GDPR, AI Act profiles)  

They are signed, auditable, and tenant-isolated.  
Enterprise deployments can diff, activate, and roll back policy packs.

---

## 6. How is the Verifier different from the runtime?

The Verifier is a separate microservice used only when intent is unclear.  
It provides additional context for ambiguous requests.

Runtime = always on.  
Verifier = only used when needed.

If the Verifier still cannot classify the request, Guardrail returns it to the
submitter for clarification.

---

## 7. Is Guardrail a guarantee of AI safety or compliance?

No.  
Guardrail is a governance and policy enforcement layer. It provides signals,
controls, and oversight designed to help reduce risk, but it cannot guarantee
outcomes or replace an organization’s internal policies.

---

## 8. Does Guardrail store prompts or responses?

Storage depends on configuration:

- Core Runtime: minimal audit metadata  
- Enterprise Runtime: optional retention stores, audit bundles, and evidence exports  

Organizations define their own retention strategy based on policy,
regulations, and risk.

---

## 9. How does multi-tenancy work?

Each tenant maintains:

- its own policy namespace  
- its own audit stream  
- its own quotas and rate limits  
- its own clarification and incident queues  

Tenant isolation is enforced at the API, policy, storage, and admin layers.

---

## 10. Is Guardrail open source?

The Guardrail platform contains multiple components with different licenses:

- **Core Runtime** — Open Source (MIT)  
- **Enterprise Runtime** — Proprietary  
- **Verifier Service** — Proprietary, source-available  
- **Policy Packs** — Proprietary, source-available  

The core is open source; the governance and rule components are not.

---

## 11. What does “source-available” mean?

Source-available means the repository is publicly visible for evaluation,
auditing, and transparency, but:

- it is **not** open source  
- it may not be copied, forked, or redistributed  
- commercial usage requires a license  

The code is visible, but rights are restricted.

---

## 12. Can Guardrail run in air-gapped or offline environments?

Yes, with certain constraints:

- Policy Packs can be bundled locally  
- Enterprise Runtime can operate fully offline  
- Verifier can run locally if LLM verifiers are also local  
- Model providers must be reachable unless using self-hosted models  

Deployment guides describe the required environment variables and artifacts.

---

## 13. What are common deployment patterns?

Organizations often deploy Guardrail as:

- a sidecar next to a model gateway  
- a cluster service in Kubernetes  
- a reverse-proxy style gateway in front of LLM APIs  
- a centralized enterprise safety layer  

Enterprise deployments often combine Redis, Postgres, and object storage.

---

## 14. How does Guardrail integrate with models?

Guardrail can be placed in front of:

- OpenAI  
- Anthropic  
- Google Gemini  
- Azure OpenAI  
- Local models (vLLM, Ollama, etc.)  
- Any HTTP-based model provider  

Integration is done at the API gateway level.

---

## 15. How are audit logs generated?

Guardrail records:

- safety evaluation results  
- verifier outcomes  
- clarifications  
- blocks and overrides  
- policy activation/rollback events  

Enterprise can export structured, evidence-ready bundles for audit teams.

---

## 16. Who maintains Guardrail?

Guardrail Labs, LLC is responsible for:

- the open-source core  
- proprietary enterprise runtime  
- verifier microservice  
- curated policy packs  
- documentation, support, and commercial onboarding  

---

## 17. How do I get support?

General inquiries:  
**enterprise@guardrailapi.com**

Security disclosures:  
**security@guardrailapi.com**

Deployment assistance and onboarding are included with enterprise licensing.

---

*This FAQ is informational and does not modify or extend any license agreement,
service-level obligation, or legal commitment from Guardrail Labs LLC.*
