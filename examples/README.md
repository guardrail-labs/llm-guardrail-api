# Examples — One-Command Demo

```bash
make demo     # boots core/enterprise/verifier and runs smoke checks
make down     # stop & remove
```

Ports: Core 8080, Enterprise 8081, Verifier 8082.

## CI Notes (Private GHCR)

The CI workflow logs into GHCR using repo secrets:

- `GHCR_READ_USER` — the username that owns the PAT
- `GHCR_READ_PAT` — a read-only PAT with `read:packages`

Forked PRs skip this job (no secrets exposure). Use an internal mirror branch if you need CI smoke on external contributions.

## Acceptance Criteria

- `make demo` boots all three containers and passes smoke locally.
- CI workflow `examples-smoke` passes on internal PRs and `workflow_dispatch`.
- No changes to ruff/mypy (docs/scripts only).
- Versions pinned: Core 1.5.0, Enterprise 1.4.0, Verifier 0.2.0.

---

## Repo Settings (one-time)
Add repository secrets:
- **GHCR_READ_USER** = `<username that created the PAT>`
- **GHCR_READ_PAT**  = `<PAT with read:packages>`
> These correspond to the account that has access to `ghcr.io/guardrail-labs/*` images.

---

## Validation

**Local:**
```bash
docker login ghcr.io -u "$GHCR_READ_USER" -p "$GHCR_READ_PAT"
docker pull ghcr.io/guardrail-labs/guardrail-enterprise:1.4.0
make demo
make down
```

**CI:**

Open PR from an internal branch named `feat/examples-smoke` (or similar).

Confirm job runs (not skipped), images pre-pull, stack boots, smoke passes.

Re-run via “Run workflow” if needed.
