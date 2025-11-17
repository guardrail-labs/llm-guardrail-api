# Contributing to Guardrail Labs — Umbrella Repository

Thank you for your interest in contributing to the Guardrail API umbrella
project. This repository (`llm-guardrail-api`) contains public documentation,
the `guardrailctl` CLI, and shared assets used across the Guardrail platform.

Because this repository is licensed under MIT, contributions are welcome.
However, contributions must respect the boundaries of the Guardrail Labs
licensing model and should not attempt to modify proprietary components.

Please read the following guidelines before opening an issue or submitting a
pull request.

---

# 🧭 1. What This Repository Contains

This repository includes:

- Documentation for the Guardrail platform  
- The `guardrailctl` command-line tool  
- Public deployment templates  
- Architecture, runtime, and governance documentation  
- Product overview and glossary  
- MIT-licensed assets only  

This repository **does not** contain proprietary runtime code.

---

# 🚫 2. What You May *Not* Contribute

The following components are **proprietary** and must not be copied, reverse
engineered, reimplemented, or referenced through PRs in this repository:

- `llm-guardrail-api-enterprise`  
- Guardrail Labs proprietary licensing text  
- Internal retention, evidence, RBAC, or governance logic  
- Proprietary configuration schemas  
- Embedded policy evaluation logic  
- Guardrail Labs’ commercial artifacts or SBOM bundles  

Pull requests touching or recreating these components will be closed.

---

# ✔️ 3. What You *May* Contribute

Contributions are welcome in the following areas:

### Documentation
- Fixes to formatting, clarity, or consistency  
- Additions to the glossary  
- Improvements to readability or structure  
- Better examples or explanations  

### CLI (`guardrailctl`)
- Bug reports and straightforward fixes  
- New commands that operate only on open-source components  
- Enhancements that do not touch proprietary logic  

### Deployment Templates
- Improvements to Kubernetes, Docker, or Helm templates  
- Cross-platform compatibility enhancements  
- Corrections or clarifications to examples  

### Issue Reports
- Documentation defects  
- Installation or environment problems  
- Unexpected CLI behavior  
- Suggestions for clarity-first workflow examples  

---

# 🧪 4. Development Requirements

Before submitting a PR:

1. Ensure all Python tooling passes:

   ```bash
   ruff check .
   mypy .


Ensure documentation builds cleanly:
 ```
mkdocs build
 ```

Provide tests for CLI changes where appropriate.
Follow standard Python formatting and type-checking conventions.

## 🔃 5. Pull Request Process
 ```
Fork the repository on GitHub.

Create a feature branch:

git checkout -b feat/<short-description>


Commit changes with a clear message.

Ensure the CI pipeline passes.

Open a pull request with:

clear problem description

summary of changes

confirmation that proprietary components were not modified

A maintainer will review and provide feedback or merge.
 ```
## 🛡 6. Security Concerns

Do not report security issues through GitHub issues or pull requests.

Instead, follow the disclosure process in SECURITY.md:

security@guardrailapi.com

## 📬 7. Contact

For questions or clarifications:

info@guardrailapi.com

Thank you for helping improve Guardrail Labs' public documentation and tooling.

