🚀 DEPLOYMENT_OVERVIEW.md — Final Formatted Version
# Guardrail API — Deployment Overview

> Guardrail Labs, LLC — Patent Pending  
> This document summarizes deployment patterns for the Guardrail API platform
> and explains how the components fit into a production environment.

Guardrail API can be deployed in several modes depending on use case:  
local development, single-node evaluation, containerized services, or full
Kubernetes-based environments.

This document provides a high-level operational overview; see the docs portal
and component-specific INSTALL guides for detailed steps.

---

# 🧱 1. Architecture Model (High-Level)

Guardrail sits between clients and one or more LLM providers:



Client Apps
↓
Guardrail Ingress Arm (prompts)
↓ ↘ (if ambiguous)
Verifier Service ↘ clarify-first → back to requestor
↓
LLM Provider / Model API
↓
Guardrail Egress Arm (responses)
↓
Client Apps


Each runtime (Core or Enterprise) evaluates traffic independently on both arms.

### Components involved:
- **Runtime (Core or Enterprise)** — enforcement engine  
- **Verifier (optional)** — non-execution intent classification  
- **Policy Packs** — safety/governance rule bundles  
- **Redis** — quotas, DLQ, idempotency, rate limiting  
- **Optional Postgres / Object Storage** — retention & audit for Enterprise  
- **Admin UI** — Enterprise only  

---

# 🧭 2. Deployment Modes

Guardrail supports three main deployment approaches:

---

## **2.1 Local / Developer Mode**

Suitable for:
- Testing integrations  
- Running examples  
- Experimenting with policy packs  

Run via Python or Uvicorn:

```bash
pip install guardrail-core
uvicorn app.main:create_app --factory --reload


Local mode is not hardened and not intended for production.

2.2 Single-Node Docker Deployment

A common option for:

Internal platform teams

Prototyping production gateways

Staging environments

Typical layout:

guardrail/
  Dockerfile
  .env
  redis/


Run the service:

docker build -t guardrailapi .
docker run -d --env-file .env -p 8080:8080 guardrailapi


Redis should be deployed as a separate container or managed instance.

2.3 Kubernetes Deployment (Recommended for Production)

Production deployments typically rely on:

Guardrail Helm chart (Core or Enterprise)

Kubernetes Ingress / Gateway API for TLS termination

Redis (managed service or statefulset)

Optional Postgres + object store (Enterprise)

External secrets manager (AWS/GCP/Azure/Vault)

A common cluster layout:

namespace: guardrail
    deployments:
      - guardrail-core or guardrail-enterprise
      - guardrail-verifier (optional)
    services:
      - guardrail-api
      - verifier-api
    config:
      - policy-packs (mounted or fetched via guardrailctl)
      - env vars / secrets
    storage:
      - redis
      - (optional) postgres
      - (optional) s3/minio


This mode enables:

Autoscaling

Robust tenancy isolation

Integration with enterprise IAM

Secure audit storage

Separation of ingress and egress SLAs

🔧 3. Required Infrastructure

Regardless of deployment mode, Guardrail expects the following:

3.1 Runtime Environment

Linux x86_64

Python 3.11+ or Docker

Outbound HTTPS to LLM providers

3.2 Redis

Used for:

Quotas

Idempotency

Dead-letter queue

Rate limiting

Certain scheduling tasks

3.3 Network / Security Requirements

TLS termination on ingress gateway

Ability to forward:

X-Tenant-ID

Authentication headers

Any custom claims you use

3.4 (Enterprise Only) Additional Services

Optional Postgres for retention + audit indexing

Optional object storage for long-term evidence bundles

Admin UI endpoints behind internal auth

🪪 4. Multi-Tenant Operation

Guardrail supports multiple tenants per runtime. Each tenant has:

Unique policy namespace

Separate audit logs

Separate quotas and limits

Separate clarification / incident queues

Enterprise deployments may add:

RBAC for tenant admins

Read-only auditor roles

Region-based retention segregation

The Admin UI operates within the current tenant context.

📦 5. Policy Pack Delivery & Activation

Policy Packs can be loaded via:

Mounted directories

Pulled through guardrailctl

Internal artifact store

(Not recommended) Embedded in images

Activation is:

Versioned

Signed (checksums)

Logged in audit stream

Reversible (rollback audited)

This ensures traceable governance for all policy updates.

🔍 6. Verifier Deployment

The Verifier service is optional but recommended for:

Ambiguous high-risk prompts

Clarify-first workflows

Research vs. misuse differentiation

Deployment options:

Single-node container

Kubernetes deployment

Horizontal autoscaling for high-throughput workloads

Integration flow:

Ingress detects unclear intent

Verifier evaluates intent (non-execution)

If still unclear → returned to requestor

If classified → enforcement proceeds

🔐 7. Security & Hardening Guidelines
Network

TLS everywhere

Admin endpoints restricted to internal networks

Private networking for Postgres/Redis

Secrets

Inject via env vars or secret manager

Never bake secrets in images

Scaling

Ingress/Egress arms scale independently

Verifier pool scales horizontally

Logging

Treat logs as sensitive

Rotate and protect audit logs

Firewalls

Restrict outbound egress to known LLM domains

Restrict inbound traffic except via your gateway

🛡 8. High Availability / Redundancy

Production deployments typically use:

Multi-replica runtimes

Redis HA (sentinel or managed)

Multi-AZ architecture

Load balancers or service mesh

Autoscaling for surges

Both arms (ingress & egress) operate independently during temporary degradation.

📊 9. Observability & Metrics

Guardrail exposes:

/metrics — Prometheus metrics

/health — readiness/liveness checks

Structured JSON audit logs

Tenant-level counters

Arm-level SLA indicators

Enterprise includes additional visibility in the Admin Console.

🧪 10. Deployment Testing

Recommended phases:

1. Static Validation

Linting

Policy pack validation

Container builds

2. Staging Tests

Ingress/egress classification

Unicode / obfuscation tests

Clarify-first behavior

3. End-to-End Tests
client → guardrail → LLM → guardrail → client

🆘 11. Support

For deployment assistance or production onboarding:

enterprise@guardrailapi.com

security@guardrailapi.com

See component-specific INSTALL guides for detailed steps.
