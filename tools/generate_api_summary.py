"""Fetch and summarize Guardrail service OpenAPI specs."""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path
from typing import Any

SERVICES: dict[str, str] = {
    "Core": "http://127.0.0.1:8080/openapi.json",
    "Enterprise": "http://127.0.0.1:8081/openapi.json",
    "Verifier": "http://127.0.0.1:8082/openapi.json",
}


def _fetch(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=5) as resp:  # noqa: S310
        return json.load(resp)


def main() -> int:
    lines: list[str] = ["# API Summary", ""]
    for name, url in SERVICES.items():
        try:
            spec = _fetch(url)
            info = spec.get("info", {})
            title = info.get("title", name)
            version = info.get("version", "?")
            paths = spec.get("paths", {})
            lines.append(f"## {title} ({name})")
            lines.append(f"- Version: `{version}`")
            lines.append(f"- Endpoints: {len(paths)}")
            lines.append(f"- Source: [{url}]({url})")
            lines.append("")
        except Exception as exc:  # noqa: BLE001
            lines.append(f"## {name}")
            lines.append(f"- ❌ Error fetching: {exc}")
            lines.append("")

    Path("docs/api/summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("API summary written to docs/api/summary.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
