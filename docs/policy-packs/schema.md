# Policy Pack Schema

The manifest for each pack is a YAML document that declares identity, compatibility, and lifecycle
status. Core expects the following fields for packs targeting Policy Packs 1.0.0:

- **name** *(string)* – Human-readable pack name.
- **id** *(string)* – Stable identifier used when loading the pack into Core.
- **version** *(semver)* – Pack version such as `1.0.0`.
- **schema** *(semver)* – Schema version supported by the runtime (`1.0.0`).
- **status** *(enum)* – `stable`, `beta`, or `deprecated`.
- **compat.core** *(semver range)* – Minimum Core runtime version required (e.g., `>=1.6.0`).
- **compat.enterprise** *(semver range)* – Minimum Enterprise Console version required (e.g.,
  `>=1.5.0`).
- **summary** *(string)* – Short description of the ruleset and coverage.
- **artifacts** *(list, when used)* – Additional files or models the pack depends on.

The validator enforces manifest presence, semantic version formatting, and required compatibility
fields before a pack can be promoted.
