# Troubleshooting

## Cannot reach Core API
Verify the container is running and listening on the expected port (`/healthz` should return 200).
If you are routing through a proxy, ensure `X-Guardrail-Tenant` headers are preserved.

## No usage data appearing in Enterprise Console
Core 1.6.0 exports aggregated metrics via `/v1/admin/usage/summary`. Confirm the Enterprise Console
is pointed at the correct Core URL and that recent traffic exists for the selected tenant.

## Tenant appears misconfigured
List tenants through the Admin UI or `GET /v1/tenants` and confirm the workspace identifier in your
headers matches an existing tenant. Regenerate API keys if they were rotated.

## Ports already in use
Change the `-p HOST:CONTAINER` mappings (for example, `-p 18080:8080`) and update the curl commands
to match.

## OpenAPI returns 404
Ensure the service is healthy by checking `/healthz` and verify you are sending requests to the
correct port.

## Metrics empty
Wait a few seconds after startup; some counters publish on first use. Trigger a trivial request to
populate the feed.

## Enterprise CSRF routes
Admin `POST` or `DELETE` endpoints require CSRF tokens. Use `GET` endpoints for smoke checks or
supply the expected headers.

## Verifier timeouts
The Verifier fails closed. If a provider is down the breaker opens and requests fall back. Inspect
`verifier_*` metrics for `breaker_open` counters.
---

**Guardrail Labs, LLC — Patent Pending**
