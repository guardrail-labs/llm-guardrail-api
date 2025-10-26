# Guardrail API Umbrella Repository

This repository is the home of Guardrail API. It provides:

- `guardrailctl`: a Typer-based installer and deployment helper for Guardrail API Enterprise and Core.
- Deployment templates for Docker Compose and Helm.
- Public documentation published via GitHub Pages.

The runtime releases live in dedicated repositories:

- Enterprise: <https://github.com/WesMilam/llm-guardrail-api-enterprise>
- Core: <https://github.com/WesMilam/llm-guardrail-api-next>

## Install the CLI

Use `pipx` for an isolated installation:

```bash
pipx install git+https://github.com/WesMilam/llm-guardrail-api.git
```

Or install locally while developing:

```bash
python -m pip install -U pip
pip install -e .
```

## Usage

List channels and verify releases:

```bash
guardrailctl channels list
guardrailctl verify --edition enterprise --tag v1.0.0-GA
```

Install to a target directory:

```bash
guardrailctl install --edition enterprise --tag v1.0.0-GA --dest /opt/guardrail
```

Generate deployment assets:

```bash
guardrailctl compose init --dest /opt/guardrail
guardrailctl helm render --out ./manifests
```

Refer to the [documentation site](https://wesmilam.github.io/llm-guardrail-api/) for enterprise installation, operations, and release verification guides.
