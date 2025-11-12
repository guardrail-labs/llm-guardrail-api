# Policy Pack Schema

- **version** and **schema** must be SemVer (`MAJOR.MINOR.PATCH`).
- **compat.core / compat.enterprise**: required, semver ranges.
- **status**: `stable | beta | deprecated`.

The validator enforces manifest presence and schema conformance.
