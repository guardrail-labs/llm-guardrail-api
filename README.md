# Guardrail Umbrella Docs

[![Docs](https://img.shields.io/badge/docs-live-blue)](#)
![Core](https://img.shields.io/badge/Core-1.5.0-green)
![Enterprise](https://img.shields.io/badge/Enterprise-1.4.0-green)
![Verifier](https://img.shields.io/badge/Verifier-0.2.0-green)
![Policy Packs](https://img.shields.io/badge/Policy_Packs-1.0.0-green)

> Guardrail Labs, LLC — Patent Pending

See the [documentation portal](https://guardrail-labs.github.io/llm-guardrail-api/) for the full version matrix.


This repository contains the Guardrail API umbrella project. It publishes the MkDocs-based
documentation portal, the `guardrailctl` CLI, and deployment templates used to bootstrap new
environments.

## Repository layout

The Guardrail platform is delivered through four coordinated repositories:

1. **Umbrella & CLI (`llm-guardrail-api`)** – hosts the documentation portal, deployment
   templates, and the `guardrailctl` installer used to interact with every other component.
2. **Core Runtime (`llm-guardrail-api-next`)** – open-source runtime that powers policy
   evaluation, inference mediation, and local development environments.
3. **Enterprise Runtime (`llm-guardrail-api-enterprise`)** – hardened build with signed
   artifacts, extended integrations, and SOC 2 controls for production deployments.
4. **Policy Packs (`llm-guardrail-policy-packs`)** – curated rule bundles that encode Guardrail
   best practices and can be promoted across tenants.

> **Note:** The Enterprise Runtime (`llm-guardrail-api-enterprise`) and its artifacts are private and available only under commercial license. The public docs and CLI can interact with these editions, but their source repositories and container images are not publicly accessible.


Each repository publishes releases independently so teams can version runtimes, policy packs,
and documentation on their own cadence. The umbrella CLI links them together by fetching
channels, verifying artifacts, and rendering deployment assets.

## Documentation portal

The complete product documentation lives at
(https://guardrail-labs.github.io/llm-guardrail-api/).
It covers installation, architecture, tenants and RBAC, policy pack workflows, the Admin UI,
verifier usage, and SOC 2 evidence collection.

## Install the CLI

Use `pipx` for an isolated installation:

```bash
pipx install git+https://github.com/guardrail-labs/llm-guardrail-api.git
```

Or install locally while developing:

```bash
python -m pip install -U pip
pip install -e .
```

## Common commands

List channels and verify releases (Core edition):

```bash
guardrailctl channels list
guardrailctl verify --edition core --tag v1.5.0
```
Install to a target directory:

```bash
guardrailctl install --edition core --tag v1.5.0 --dest /opt/guardrail
```

Generate deployment assets:

```bash
guardrailctl compose init --dest /opt/guardrail
mkdir -p manifests
guardrailctl helm render --out ./manifests
```

Refer to the [documentation portal](https://guardrail-labs.github.io/llm-guardrail-api/) for
end-to-end guides covering enterprise installation, operations, and release verification.
