# Guardrail Labs — Glossary of Terms

> Guardrail Labs, LLC — Patent Pending  
> Guardrail Labs supports effective communication through the normalization
> of terminology across AI, security, and software engineering fields.  
> This glossary is provided to help maintain shared understanding across
> technical and non-technical stakeholders.

This glossary defines terms used throughout the Guardrail API platform,
documentation portal, and governance framework.

---

# 🧩 Core Concepts

### **Guardrail Runtime**
The enforcement engine that evaluates inbound prompts (ingress) and outbound
model responses (egress). Handles policy execution, clarification logic, and
modality-aware governance.

### **Dual-Arm Architecture**
A design where ingress and egress evaluation paths operate independently, each
maintaining its own policies, circuit breakers, metrics, and decision logs.

### **Ingress**
All user-submitted inputs before they reach an LLM.  
Includes text, images, audio, files, structured JSON payloads, and tool-call
envelopes.

### **Egress**
All model-generated outputs before they are returned to the user.  
Includes text, images, audio, files, and structured outputs.

### **Clarify-First Workflow**
A safety-aligned approach in which ambiguous intent results in a clarification
request rather than an immediate block or allowed decision.  
The runtime does not guess user intent.

### **Verifier Service**
A non-execution microservice used to classify unclear or ambiguous requests.
Provides intent categories without running or simulating untrusted content.

### **Policy Packs**
Versioned, signed rule bundles that determine how the runtime evaluates and
governs requests. Rules may include safety categories, modality constraints,
regulatory profiles, and pattern-based logic.

---

# 🔐 Security & Compliance Terms

### **Sanitization**
Modality-appropriate preprocessing steps such as Unicode normalization,
confusables detection, MIME/type checks, metadata stripping, or structural
validation.

### **Confusables / Homoglyphs**
Unicode characters designed to visually mimic other characters, often used in
obfuscation or red-teaming scenarios. Guardrail detects and surfaces these
signals to policy.

### **Audit Log**
Structured, append-only records describing policy decisions, clarifications,
sanitization signals, and administrative actions. Enterprise deployments may
export evidence bundles for regulators or auditors.

### **Retention**
Enterprise-level configuration controlling how long logs, clarifications, or
evidence bundles are stored.

### **Regulatory Profiles**
Groups of rules associated with governance frameworks (e.g., GDPR, HIPAA,
AI Act templates). Profiles may be tenant-specific or region-specific.

---

# 🏛 Operational Terms

### **Tenant**
A logically isolated configuration and governance boundary.  
Each tenant has separate policies, quotas, logs, and clarification queues.

### **RBAC (Role-Based Access Control)**
Enterprise feature controlling access to administrative capabilities.  
Typical roles include tenant admin, platform operator, or read-only auditor.

### **DLQ (Dead-Letter Queue)**
A Redis-based holding area for failed or malformed requests that could not be
processed by the runtime.

### **Idempotency**
Guarantees that repeated identical requests are processed only once.  
The runtime uses Redis to track idempotent keys for safety and consistency.

### **Circuit Breaker**
A control that temporarily limits or isolates an arm (ingress or egress) in the
event of degradation, overload, or upstream model failures.

---

# 🌐 Modalities

### **Text Modality**
Human-readable strings supplied by a user or produced by a model.

### **Image Modality**
Uploaded or generated images; subject to metadata checks, format validation, and
policy rules (e.g., safety categories).

### **Audio Modality**
Audio inputs or outputs; may include optional transcription signals.

### **File Modality**
Documents, structured files, or binary content; subject to MIME/type checking,
content extraction, and size limits.

### **Structured / JSON Modality**
Model-generated JSON, tool-call envelopes, or schema-dependent results subject
to structure validation and key-level rules.

---

# 📬 Contact & Attribution

For glossary additions, corrections, or terminology requests, contact:  
**info@guardrailapi.com**

© Guardrail Labs LLC 2025. All rights reserved.
