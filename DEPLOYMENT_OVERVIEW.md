# Guardrail API — Deployment Overview

> Guardrail Labs, LLC — Patent Pending  
> This document provides a high-level overview of how to deploy Guardrail API
> components in development, staging, and production environments.

The Guardrail platform is composed of modular services that evaluate AI
traffic, enforce governance policies, and support clarify-first workflows.
Deployments range from lightweight local setups to full multi-tenant
Kubernetes installations.

This overview describes the major patterns and infrastructure needed to deploy
Core, Enterprise, the Verifier, and Policy Packs.

---

# 🧱 1. High-Level Architecture

Guardrail sits between client applications and model providers:

Client  
↓  
**Ingress Arm (Core or Enterprise)**  
↓ ↘ (if ambiguous)  
**Verifier** → returned to user if unclear  
↓  
**LLM Provider**  
↓  
**Egress Arm (Core or Enterprise)**  
↓  
Client

Both arms evaluate **all supported modalities**:  
text, images, audio, files, and structured results.

The arms operate independently, so egress protections continue even if ingress
experiences temporary degradation.

---

# 🧭 2. Deployment Modes

Guardrail supports three primary deployment patterns.

---

## 2.1 Local / Developer Mode

Best for:
- Training and experimentation  
- CLI usage  
- Policy pack iteration  
- Integration prototyping  

Example:

```bash
pip install guardrail-core
uvicorn app.main:create_app --factory --reload
```
Local mode is not hardened and is not recommended for production use.

2.2 Single-Node Docker Deployment
Common for:

Internal prototypes

Staging environments

Small-scale deployments

Typical layout:
```
bash
Copy code
guardrail/
  .env
  Dockerfile
  redis/
```
Run Core or Enterprise:
```
bash
Copy code
docker build -t guardrailapi .
docker run -d --env-file .env -p 8080:8080 guardrailapi
```
Redis should run as a separate container or managed service.

2.3 Kubernetes Deployment (Recommended for Production)
Production environments typically use:

Guardrail Helm charts (Core or Enterprise)

Kubernetes Ingress or Gateway API for TLS termination

Managed Redis (quota, DLQ, idempotency, rate limiting)

Optional Postgres / object storage (Enterprise retention)

External secrets manager (AWS, Azure, GCP, or Vault)

A typical cluster layout:
```
markdown
Copy code
namespace: guardrail
  deployments:
    - guardrail-core or guardrail-enterprise
    - guardrail-verifier (optional)
  services:
    - guardrail-api
    - verifier-api
  storage:
    - redis
    - (optional) postgres
    - (optional) s3/minio
  config:
    - tenant configs
    - policy packs
    - secrets
```
Kubernetes provides:

autoscaling

high availability

rolled updates

network policy enforcement

multi-tenant isolation

🔧 3. Required Infrastructure
Regardless of deployment mode, Guardrail requires:

3.1 Runtime Requirements
Linux x86_64

Python 3.11+ or Docker

HTTPS egress to LLM providers

3.2 Redis
Used for:

idempotency

quotas

rate limiting

dead-letter queue

certain async tasks

3.3 Network / Security
TLS termination at ingress gateway

Ability to forward:

X-Tenant-ID

authentication context

relevant claims

3.4 (Enterprise Only)
Optional Postgres (retention + audit indexing)

Optional object storage (evidence bundles)

Internal RBAC roles for admin console

🏛 4. Multi-Tenant Operation
Both Core and Enterprise support multi-tenant deployments.

Each tenant has:

independent policy namespace

isolated audit logs

separate quotas and rate limits

independent clarification queues

Enterprise adds:

RBAC

regional retention stores

policy pack diffing and rollback

visibility controls for tenant admins

The Admin Console operates within a tenant-scoped context.

📦 5. Policy Pack Delivery
Policy Packs may be loaded via:

mounted directories

guardrailctl fetch

internal artifact repositories

CI/CD pipelines (recommended)

Activations are:

versioned

checksum-verified

logged in audit streams

reversible (rollback also audited)

Policy Packs determine the runtime’s evaluation behavior.

🧩 6. Verifier Deployment
The Verifier is optional but recommended for ambiguous or high-risk prompts.

Deployment modes:

single Docker container

Kubernetes deployment

horizontally scaled pool

If the Verifier cannot classify intent confidently:
the request is returned to the submitter for clarification.

The Verifier never executes user input.

🔐 7. Security & Hardening
Recommended practices:

Network
TLS termination in Ingress/Gateway API

Restrict internal admin endpoints

Use private networking for Redis/Postgres

Secrets
store in secret managers

never build secrets into images

Scaling
ingress and egress arms may scale independently

verifier pools scale horizontally

Logging
treat prompt/response logs as sensitive

rotate and secure audit logs

🛡 8. High Availability & Fault Tolerance
Production deployments benefit from:

multi-replica deployments

Redis HA (sentinel or managed)

cross-zone redundancy

autoscaling policies

health and readiness probes

Ingress and egress circuits operate independently to maintain continuity even
when one arm experiences load or upstream issues.

📊 9. Observability
Guardrail exposes:

/metrics for Prometheus

/health for readiness/liveness

structured audit logs

tenant-level counters and SLA indicators

Enterprise adds:

Admin Console observability

retention evidence export

operator dashboards

🧪 10. Deployment Testing
Recommended phases:

Static validation
container builds

policy pack validation

CLI configuration checks

Staging tests
ingress/egress rules

clarify-first behavior

obfuscation and confusables handling

Full E2E tests
Client → Guardrail → LLM → Guardrail → Client

📬 11. Support
General inquiries: info@guardrailapi.com

Enterprise support: enterprise@guardrailapi.com

Security disclosures: security@guardrailapi.com
