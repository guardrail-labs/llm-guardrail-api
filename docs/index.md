# Guardrail API — Home

**Guardrail API** is a firewall for LLMs: it sanitizes prompts, verifies intent, rate-limits, and audits model output.

## Quickstart
```bash
pipx install .
guardrailctl channels list
guardrailctl verify --edition enterprise --tag v1.0.0-GA
guardrailctl install --edition enterprise --tag v1.0.0-GA --dest /opt/guardrail
```

See:

- [INSTALL_ENTERPRISE](INSTALL_ENTERPRISE.md)
- [OPERATIONS_QUICKSTART](OPERATIONS_QUICKSTART.md)
- [admin guide](admin_guide.md)
- [Release verification](RELEASE_VERIFY.md)
- [GA release notes](GA_RELEASE_NOTES.md)
