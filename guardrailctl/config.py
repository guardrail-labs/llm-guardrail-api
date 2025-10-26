from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping

import yaml


CONFIG_ENV_PREFIX = "GUARDRAIL_CHANNEL_"
DEFAULT_OVERRIDE_ENV = "GUARDRAIL_CHANNELS_OVERRIDE"
CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "guardrailctl"
OVERRIDE_FILENAME = "channels.override.yaml"


@dataclass(frozen=True)
class Channel:
    owner: str
    repo: str
    artifact: str
    checksum: str
    soc2_artifact: str | None = None
    soc2_checksum: str | None = None

    def asset(self, template: str, tag: str) -> str:
        return template.replace("${tag}", tag)

    def build_assets(self, tag: str) -> Dict[str, str]:
        data = {
            "artifact": self.asset(self.artifact, tag),
            "checksum": self.asset(self.checksum, tag),
        }
        if self.soc2_artifact and self.soc2_checksum:
            data["soc2_artifact"] = self.asset(self.soc2_artifact, tag)
            data["soc2_checksum"] = self.asset(self.soc2_checksum, tag)
        return data


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    content = path.read_text("utf-8")
    data = yaml.safe_load(content) or {}
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping in {path}")
    return data


def _merge_dict(base: Dict[str, Any], override: Mapping[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, Mapping)
        ):
            result[key] = _merge_dict(result[key], value)
        else:
            result[key] = value
    return result


def _apply_env_overrides(channels: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for edition, data in channels.items():
        merged = dict(data)
        upper = edition.upper()
        for field in ("OWNER", "REPO", "ARTIFACT", "CHECKSUM", "SOC2_ARTIFACT", "SOC2_CHECKSUM"):
            value = os.getenv(f"{CONFIG_ENV_PREFIX}{upper}_{field}")
            if value:
                merged[field.lower()] = value
        result[edition] = merged
    return result


def _override_path() -> Path:
    override_env = os.getenv(DEFAULT_OVERRIDE_ENV)
    if override_env:
        return Path(override_env).expanduser()
    return CONFIG_DIR / OVERRIDE_FILENAME


def load_channels() -> Dict[str, Channel]:
    package_path = Path(__file__).parent / "channels.yaml"
    base = _load_yaml(package_path).get("channels", {})
    if not isinstance(base, dict):
        raise ValueError("channels.yaml must contain a mapping under 'channels'")
    override_data = _load_yaml(_override_path())
    override_channels = override_data.get("channels", {})
    if override_channels and not isinstance(override_channels, Mapping):
        raise ValueError("override file must contain mapping under 'channels'")
    merged_channels: Dict[str, Dict[str, Any]] = {}
    for edition, data in base.items():
        edition_data = dict(data) if isinstance(data, Mapping) else {}
        overrides = (
            override_channels.get(edition, {})
            if isinstance(override_channels, Mapping)
            else {}
        )
        if overrides and not isinstance(overrides, Mapping):
            raise ValueError(f"override for {edition} must be a mapping")
        merged = _merge_dict(edition_data, overrides if isinstance(overrides, Mapping) else {})
        merged_channels[edition] = merged
    merged_channels = _apply_env_overrides(merged_channels)
    channels: Dict[str, Channel] = {}
    for edition, data in merged_channels.items():
        channels[edition] = Channel(
            owner=str(data.get("owner", "")),
            repo=str(data.get("repo", "")),
            artifact=str(data.get("artifact", "")),
            checksum=str(data.get("checksum", "")),
            soc2_artifact=(
                str(data["soc2_artifact"]) if data.get("soc2_artifact") else None
            ),
            soc2_checksum=(
                str(data["soc2_checksum"]) if data.get("soc2_checksum") else None
            ),
        )
    return channels


def get_channel(edition: str) -> Channel:
    channels = load_channels()
    if edition not in channels:
        raise KeyError(f"unknown edition '{edition}'")
    channel = channels[edition]
    missing = [
        field
        for field in ("owner", "repo", "artifact", "checksum")
        if not getattr(channel, field)
    ]
    if missing:
        raise ValueError(f"channel '{edition}' missing fields: {', '.join(missing)}")
    return channel


def channels_override_location() -> Path:
    return _override_path()


def resolve_admin_url(url: str | None) -> str:
    return url or os.getenv("GUARDRAIL_URL") or "http://localhost:8080"


def resolve_admin_token(token: str | None) -> str | None:
    return token or os.getenv("GUARDRAIL_TOKEN")
