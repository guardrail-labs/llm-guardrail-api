# Troubleshooting

## Ports already in use
Change the `-p HOST:CONTAINER` mappings (for example, `-p 18080:8080`) and update the curl
commands to match.

## OpenAPI returns 404
Ensure the service is healthy by checking `/healthz` and verify you are sending requests to the
correct port.

## Metrics empty
Wait a few seconds after startup; some counters publish on first use. Trigger a trivial request
to populate the feed.

## Enterprise CSRF routes
Admin `POST` or `DELETE` endpoints require CSRF tokens. Use `GET` endpoints for smoke checks or
supply the expected headers.

## Verifier timeouts
The Verifier fails closed. If a provider is down the breaker opens and requests fall back.
Inspect `verifier_*` metrics for `breaker_open` counters.
