# Quickstart

Follow this guide to stand up a Guardrail API environment in minutes. The steps focus on the
`guardrailctl` CLI that ships from this umbrella repository and can be adapted for Core or
Enterprise deployments.

## Prerequisites

* Python 3.11 or newer.
* Access to the Guardrail container registry (Enterprise customers) or the public images
  published for the Core edition.
* A workstation with Docker installed if you plan to use the provided Compose bundle.
* Optional: kubectl and Helm if targeting Kubernetes.

## Install the CLI

```bash
python -m pip install --upgrade pip
pip install guardrailctl
```

To track the latest changes from the main branch you can install directly from GitHub:

```bash
pipx install git+https://github.com/WesMilam/llm-guardrail-api.git
```

Confirm the CLI is available:

```bash
guardrailctl --version
```

## Discover available releases

Guardrail distributes both Core and Enterprise channels. View the available builds with:

```bash
guardrailctl channels list
```

Use the edition and tag columns when selecting a release for deployment or verification.

## Verify an artifact before deployment

Every Enterprise artifact is signed. Validate a candidate release prior to rolling it out:

```bash
guardrailctl verify --edition enterprise --tag v1.0.0-GA
```

Verification writes a signed SBOM and attestation bundle to the current directory. Store the
outputs with your change request for traceability.

## Install to a target directory

Create a working directory for the runtime and unpack the selected channel:

```bash
mkdir -p /opt/guardrail
cd /opt/guardrail
guardrailctl install --edition enterprise --tag v1.0.0-GA --dest .
```

The CLI lays down the runtime binaries, configuration stubs, and policy-pack manifest needed
by Compose, Helm, or custom automation.

## Generate deployment assets

Choose the deployment model that fits your environment. The CLI can render both Docker
Compose and Helm manifests.

```bash
# Docker Compose assets
guardrailctl compose init --dest ./compose

# Kubernetes manifests
mkdir -p manifests
guardrailctl helm render --out ./manifests
```

Review the generated files and commit them to your infrastructure repository. After you roll
out the services, continue to the [Policy Packs](policy-packs.md) page to populate the
runtime with guardrails tailored to your use cases.
