# Admin UI

The Guardrail Enterprise Console (v1.5.0) gives operators a centralized console for managing
tenants, policy packs, runtime endpoints, and billing data. The UI runs as a standalone web
application that communicates with the Guardrail API using service account credentials.

## Logging in

1. Navigate to the Admin UI URL provided by your deployment.
2. Authenticate with SSO or local credentials depending on your configuration.
3. Select the organization and workspace you want to administer.

After logging in you land on the workspace dashboard with summaries of active policy packs,
recent verifier runs, and outstanding approval requests.

## Key capabilities

- **Tenant overview and selection** – Browse organizations and workspaces and switch contexts
  without re-authenticating.
- **Traffic and clarifications views** – Inspect recent decision traffic and verifier results when
  prompts were flagged for review.
- **Usage and billing summaries** – Review aggregated usage and period summaries provided by Core
  1.6.0.
- **Tenant lifecycle actions** – Create workspaces, manage API keys, and rotate credentials
  available in Enterprise v1.5.0.

## Approval workflows

Administrative actions that affect production—such as promoting a new policy pack or rotating an
API key—can require dual approval. Configure approvers per workspace or organization. The UI tracks
who requested and approved the change and exposes the audit record to the Verifier.

## Notifications

Integrate the Admin UI with email, Slack, or Microsoft Teams to deliver approval requests and
incident alerts. Notifications include deep links that direct reviewers back into the appropriate
screen.

## Extensibility

The UI consumes the same public API documented in the [API Reference](api-reference.md). You can
replicate any action programmatically if you need to integrate with existing ITSM tools or custom
portals.
