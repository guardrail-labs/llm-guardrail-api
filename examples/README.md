# Examples — One-Command Demo

```bash
make demo     # boots core/enterprise/verifier and runs smoke checks
make down     # stop & remove
```

Ports: Core 8080, Enterprise 8081, Verifier 8082.

### Acceptance Criteria
- `make demo` boots all three containers and passes smoke locally.
- CI workflow `examples-smoke` runs on PRs and passes.
- No ruff/mypy changes needed (docs/scripts only).
- Keep versions: Core **1.5.0**, Enterprise **1.4.0**, Verifier **0.2.0**.

Want the Helm overlays next (single-tenant, multi-tenant+verifier, egress-only) as **PR-E2**?
