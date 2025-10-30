# Admin UI

The Guardrail Admin UI gives operators a centralized console for managing tenants, policy
packs, runtime endpoints, and compliance workflows. The UI runs as a standalone web
application that communicates with the Guardrail API using service account credentials.

## Logging in

1. Navigate to the Admin UI URL provided by your deployment.
2. Authenticate with SSO or local credentials depending on your configuration.
3. Select the organization and workspace you want to administer.

After logging in you land on the workspace dashboard with summaries of active policy packs,
recent verifier runs, and outstanding approval requests.

## Key areas

* **Tenants** – Create organizations and workspaces, invite members, and assign RBAC roles.
* **Policy Packs** – Browse available packs, review pending promotions, and trigger rollbacks.
* **Runtime** – View endpoint health, configure upstream model connections, and manage API
  tokens for applications.
* **Compliance** – Download SOC 2 evidence bundles and verify that attestations are attached
  to the latest releases.

## Approval workflows

Administrative actions that affect production—such as promoting a new policy pack or rotating
an API key—can require dual approval. Configure approvers per workspace or organization. The
UI tracks who requested and approved the change and exposes the audit record to the Verifier.

## Notifications

Integrate the Admin UI with email, Slack, or Microsoft Teams to deliver approval requests and
incident alerts. Notifications include deep links that direct reviewers back into the
appropriate screen.

## Extensibility

The UI consumes the same public API documented in the [API Reference](api-reference.md). You
can replicate any action programmatically if you need to integrate with existing ITSM tools or
custom portals.
