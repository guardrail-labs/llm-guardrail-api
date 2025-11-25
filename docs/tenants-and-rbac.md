# Tenants and RBAC

Guardrail API supports multi-tenant deployments so you can host multiple business units or
customers in the same runtime. RBAC ensures each user, service account, and automation job only has
access to the resources it needs.

## Tenant hierarchy

1. **Organization** – Top-level boundary for billing, policy isolation, and governance.
2. **Workspace** – Sub-division within an organization aligned to a product team or application.
   Workspaces inherit shared policy packs but can override runtime settings.

Each layer exposes quota controls, audit logs, and alert destinations. Enterprise customers can map
the hierarchy to their SSO groups and ticketing queues.

## Credentials and usage segmentation

API keys and service account tokens are issued per workspace so usage can be segmented by tenant.
Include the `X-Guardrail-Tenant` header on runtime requests to ensure decision events and aggregated
usage metrics are attributed correctly.

## Roles

The default roles ship with the Admin UI and CLI.

| Role | Scope | Capabilities |
| --- | --- | --- |
| **Org Owner** | Organization | Invite members, manage billing, approve policy pack promotions, configure SSO. |
| **Workspace Admin** | Workspace | Assign workspace roles, configure runtime endpoints, manage API keys. |
| **Auditor** | Organization | Read-only access to verifier attestations, decision logs, and SOC 2 evidence packages. |
| **Service Account** | Workspace | Token-based automation for CI/CD integrations and inference workloads. |

## RBAC enforcement

* The API Gateway checks every request for a valid tenant token or service account credential.
* Policy evaluations include the caller's role and workspace context to determine the allowed
  guardrail actions.
* Administrative operations (creating tenants, promoting policy packs, rotating keys) require
  elevated roles. The Admin UI enforces least privilege by only showing actions permitted for the
  current user.

## Integrating with identity providers

External identity provider integration (e.g., SAML or OIDC) is planned but not part of this release.

## Auditing access

Guardrail records decision, clarification, and usage events.
RBAC changes are not currently logged as audit events in this release.
---

**Guardrail Labs, LLC — Patent Pending**
