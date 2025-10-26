from __future__ import annotations

import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, TypedDict, TypeVar, cast

import requests
import typer
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

from . import config
from .io import ChecksumMismatchError, atomic_symlink, extract_tarball, verify_checksum

app = typer.Typer(add_completion=False)
compose_app = typer.Typer(help="Docker Compose helpers")
tenant_app = typer.Typer(help="Tenant bootstrap operations")
channels_app = typer.Typer(help="Release channel management")
helm_app = typer.Typer(help="Helm rendering utilities")
app.add_typer(compose_app, name="compose")
app.add_typer(tenant_app, name="tenant")
app.add_typer(channels_app, name="channels")
app.add_typer(helm_app, name="helm")

env = Environment(
    loader=PackageLoader("guardrailctl", "templates"),
    autoescape=select_autoescape(),
)

F = TypeVar("F", bound=Callable[..., Any])


def _command_factory(typer_app: typer.Typer) -> Callable[..., Callable[[F], F]]:
    def factory(*args: Any, **kwargs: Any) -> Callable[[F], F]:
        def decorator(func: F) -> F:
            typer_app.command(*args, **kwargs)(func)
            return func

        return decorator

    return factory


def _callback_factory(typer_app: typer.Typer) -> Callable[..., Callable[[F], F]]:
    def factory(*args: Any, **kwargs: Any) -> Callable[[F], F]:
        def decorator(func: F) -> F:
            typer_app.callback(*args, **kwargs)(func)
            return func

        return decorator

    return factory


app_command = _command_factory(app)
compose_command = _command_factory(compose_app)
tenant_command = _command_factory(tenant_app)
channels_command = _command_factory(channels_app)
helm_command = _command_factory(helm_app)
app_callback = _callback_factory(app)


class AppState(TypedDict):
    quiet: bool


@app_callback()
def main(ctx: typer.Context, quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress informational output")) -> None:
    ctx.obj = AppState(quiet=quiet)


def _get_state(ctx: typer.Context) -> AppState:
    return cast(AppState, ctx.obj)


def _echo(ctx: typer.Context, message: str) -> None:
    if not _get_state(ctx)["quiet"]:
        typer.echo(message)


def _echo_error(message: str) -> None:
    typer.echo(message, err=True)


def _gh_release_assets(owner: str, repo: str, tag: str) -> List[Dict[str, Any]]:
    headers: Dict[str, str] = {}
    token = os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}",
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    release = response.json()
    assets = release.get("assets", [])
    if not isinstance(assets, list):
        raise RuntimeError("Unexpected response payload from GitHub API")
    return cast(List[Dict[str, Any]], assets)


def _download_asset(url: str, destination: Path) -> None:
    with requests.get(url, stream=True, timeout=60) as stream:
        stream.raise_for_status()
        with destination.open("wb") as file:
            for chunk in stream.iter_content(chunk_size=1 << 16):
                if chunk:
                    file.write(chunk)


def _fetch_assets(
    owner: str,
    repo: str,
    tag: str,
    names: Iterable[str],
    dest: Path,
) -> Dict[str, Path]:
    dest.mkdir(parents=True, exist_ok=True)
    assets = _gh_release_assets(owner, repo, tag)
    result: Dict[str, Path] = {}
    required = {name: False for name in names}
    for asset in assets:
        name = asset.get("name")
        if name in required:
            _download_asset(asset["browser_download_url"], dest / name)
            result[name] = dest / name
            required[name] = True
    missing = [name for name, present in required.items() if not present]
    if missing:
        raise RuntimeError(f"Missing assets: {', '.join(missing)}")
    return result


def _preview_tarball(path: Path, limit: int = 10) -> List[str]:
    entries: List[str] = []
    with tarfile.open(path, "r:gz") as archive:
        for member in archive.getmembers():
            entries.append(member.name)
            if len(entries) >= limit:
                break
    return entries


def _merge_dict(base: Mapping[str, Any], override: Mapping[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(result.get(key), Mapping):
            result[key] = _merge_dict(cast(Mapping[str, Any], result[key]), value)
        else:
            result[key] = value
    return result


@app_command()
def verify(
    ctx: typer.Context,
    tag: str = typer.Option(..., "--tag", help="Release tag to verify"),
    edition: str = typer.Option("enterprise", "--edition", help="Release edition"),
    json_output: bool = typer.Option(False, "--json", help="Emit machine readable JSON"),
    soc2: bool = typer.Option(False, "--soc2", help="Validate the SOC2 bundle"),
) -> None:
    try:
        channel = config.get_channel(edition)
    except (KeyError, ValueError) as exc:
        _echo_error(str(exc))
        raise typer.Exit(code=2) from exc

    assets = channel.build_assets(tag)
    required = [assets["artifact"], assets["checksum"]]
    if soc2:
        if not channel.soc2_artifact or not channel.soc2_checksum:
            _echo_error(f"edition '{edition}' does not publish SOC2 artifacts")
            raise typer.Exit(code=2)
        required.extend([assets["soc2_artifact"], assets["soc2_checksum"]])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        try:
            downloaded = _fetch_assets(
                channel.owner,
                channel.repo,
                tag,
                required,
                tmp_path,
            )
        except requests.HTTPError as exc:
            _echo_error(f"GitHub API error: {exc}")
            raise typer.Exit(code=1) from exc
        except Exception as exc:  # noqa: BLE001 - surface fetch failure
            _echo_error(str(exc))
            raise typer.Exit(code=1) from exc

        artifact_path = downloaded[assets["artifact"]]
        checksum_path = downloaded[assets["checksum"]]
        try:
            digest = verify_checksum(artifact_path, checksum_path)
        except (ChecksumMismatchError, ValueError) as exc:
            _echo_error(str(exc))
            raise typer.Exit(code=1) from exc

        preview = _preview_tarball(artifact_path)
        result: Dict[str, Any] = {
            "edition": edition,
            "tag": tag,
            "artifact": {
                "name": assets["artifact"],
                "checksum": digest,
                "preview": preview,
            },
        }

        if soc2:
            soc2_artifact = downloaded[assets["soc2_artifact"]]
            soc2_checksum = downloaded[assets["soc2_checksum"]]
            try:
                soc2_digest = verify_checksum(soc2_artifact, soc2_checksum)
            except (ChecksumMismatchError, ValueError) as exc:
                _echo_error(str(exc))
                raise typer.Exit(code=1) from exc
            soc2_preview = _preview_tarball(soc2_artifact)
            result["soc2"] = {
                "name": assets["soc2_artifact"],
                "checksum": soc2_digest,
                "preview": soc2_preview,
            }

        if json_output:
            typer.echo(json.dumps(result, indent=2))
            return

        _echo(ctx, f"Checksum OK: {digest}")
        if preview:
            _echo(ctx, "Archive preview:")
            for name in preview:
                _echo(ctx, f"  {name}")
        if soc2:
            soc2_data = cast(Dict[str, Any], result.get("soc2", {}))
            _echo(ctx, f"SOC2 checksum OK: {soc2_data.get('checksum')}")
            if soc2_data.get("preview"):
                _echo(ctx, "SOC2 archive preview:")
                for name in cast(List[str], soc2_data["preview"]):
                    _echo(ctx, f"  {name}")


@app_command()
def current(
    ctx: typer.Context,
    root: Path = typer.Option(Path("/opt/guardrail"), "--root", help="Guardrail installation root"),
    json_output: bool = typer.Option(False, "--json", help="Emit machine readable JSON"),
) -> None:
    link = root / "current"
    if not link.exists():
        if json_output:
            typer.echo(json.dumps({"path": None, "tag": None}))
        else:
            _echo_error(f"no current release found at {link}")
        raise typer.Exit(code=1)
    try:
        target = link.resolve(strict=True)
    except FileNotFoundError as exc:
        _echo_error(f"current symlink is broken: {exc}")
        raise typer.Exit(code=1) from exc
    result = {"path": str(target), "tag": target.name}
    if json_output:
        typer.echo(json.dumps(result, indent=2))
        return
    _echo(ctx, f"Current release: {target} ({target.name})")


@app_command()
def upgrade(
    ctx: typer.Context,
    tag: str = typer.Option(..., "--tag", help="Release tag to install"),
    edition: str = typer.Option("enterprise", "--edition", help="Release edition"),
    from_path: Path = typer.Option(Path("/opt/guardrail"), "--from", help="Guardrail root directory"),
    to: Optional[Path] = typer.Option(None, "--to", help="Destination release directory"),
) -> None:
    try:
        channel = config.get_channel(edition)
    except (KeyError, ValueError) as exc:
        _echo_error(str(exc))
        raise typer.Exit(code=2) from exc

    root = from_path
    releases_root = root / "releases"
    release_dir = to or releases_root / tag
    releases_root.mkdir(parents=True, exist_ok=True)

    if release_dir.exists():
        _echo_error(f"destination {release_dir} already exists")
        raise typer.Exit(code=1)

    assets = channel.build_assets(tag)
    required = [assets["artifact"], assets["checksum"]]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        try:
            downloaded = _fetch_assets(
                channel.owner,
                channel.repo,
                tag,
                required,
                tmp_path,
            )
        except requests.HTTPError as exc:
            _echo_error(f"GitHub API error: {exc}")
            raise typer.Exit(code=1) from exc
        except Exception as exc:  # noqa: BLE001
            _echo_error(str(exc))
            raise typer.Exit(code=1) from exc

        artifact_path = downloaded[assets["artifact"]]
        checksum_path = downloaded[assets["checksum"]]
        try:
            verify_checksum(artifact_path, checksum_path)
        except (ChecksumMismatchError, ValueError) as exc:
            _echo_error(str(exc))
            raise typer.Exit(code=1) from exc

        extract_dir = tmp_path / "extract"
        extract_tarball(artifact_path, extract_dir)
        try:
            shutil.copytree(extract_dir, release_dir)
        except Exception as exc:  # noqa: BLE001 - ensure cleanup
            if release_dir.exists():
                shutil.rmtree(release_dir, ignore_errors=True)
            _echo_error(f"failed to stage release: {exc}")
            raise typer.Exit(code=1) from exc

    current_link = root / "current"
    try:
        atomic_symlink(release_dir, current_link)
    except OSError as exc:
        _echo_error(f"failed to update current symlink: {exc}")
        raise typer.Exit(code=1) from exc

    _echo(ctx, f"Activated {edition} {tag} at {release_dir}")


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, "utf-8")


@compose_command("init")
def compose_init(
    ctx: typer.Context,
    profile: str = typer.Option("minimal", "--profile", help="Compose profile: minimal or full"),
    dest: Path = typer.Option(Path("/opt/guardrail"), "--dest", help="Project directory"),
) -> None:
    profile = profile.lower()
    if profile not in {"minimal", "full"}:
        _echo_error("profile must be 'minimal' or 'full'")
        raise typer.Exit(code=2)

    dest.mkdir(parents=True, exist_ok=True)
    template_name = "docker-compose.yaml.j2" if profile == "minimal" else "docker-compose.full.yaml.j2"
    docker_compose = env.get_template(template_name).render()
    env_example = env.get_template("env.example.j2").render()
    _write_file(dest / "docker-compose.yaml", docker_compose)
    _write_file(dest / ".env.example", env_example)

    if profile == "full":
        monitoring_dir = dest / "monitoring"
        prometheus_config = """
        global:
          scrape_interval: 15s
        scrape_configs:
          - job_name: 'guardrail'
            static_configs:
              - targets: ['guardrail:8080']
        """.strip()
        _write_file(monitoring_dir / "prometheus.yml", prometheus_config + "\n")

    _echo(ctx, f"Wrote docker-compose.yaml to {dest}")


def _load_env_questions() -> List[Dict[str, Any]]:
    template = env.get_template("env.prompt.yaml")
    data = yaml.safe_load(template.render()) or {}
    questions = data.get("questions", [])
    if not isinstance(questions, list):
        raise ValueError("env.prompt.yaml must define a list of questions")
    result: List[Dict[str, Any]] = []
    for item in questions:
        if not isinstance(item, Mapping):
            raise ValueError("questions must be mappings")
        name = item.get("name")
        if not name:
            raise ValueError("each question requires a name")
        result.append(dict(item))
    return result


@compose_command("env")
def compose_env(
    ctx: typer.Context,
    dest: Path = typer.Option(Path("."), "--dest", help="Project directory"),
    write: bool = typer.Option(False, "--write", help="Write to .env"),
    out: Optional[Path] = typer.Option(None, "--out", help="Override .env output path"),
    set_values: List[str] = typer.Option([], "--set", help="Provide KEY=VALUE pairs"),
    no_prompt: bool = typer.Option(False, "--no-prompt", help="Skip interactive prompts"),
) -> None:
    try:
        questions = _load_env_questions()
    except ValueError as exc:
        _echo_error(str(exc))
        raise typer.Exit(code=1) from exc

    values: Dict[str, str] = {}
    order: List[str] = []
    for question in questions:
        name = str(question["name"])
        order.append(name)
        default = question.get("default")
        values[name] = "" if default is None else str(default)

    provided: Dict[str, str] = {}
    for item in set_values:
        if "=" not in item:
            _echo_error("--set must be provided as KEY=VALUE")
            raise typer.Exit(code=2)
        key, value = item.split("=", 1)
        provided[key] = value
        values[key] = value

    if not no_prompt:
        for question in questions:
            name = str(question["name"])
            if name in provided:
                continue
            message = str(question.get("message", name))
            default = values.get(name, "")
            response = typer.prompt(message, default=default)
            values[name] = response

    lines = [f"{key}={values[key]}" for key in order if key in values]
    for key, value in values.items():
        if key not in order:
            lines.append(f"{key}={value}")
    output = "\n".join(lines) + "\n"

    if write:
        target = out or (dest / ".env")
        _write_file(target, output)
        _echo(ctx, f"Wrote {target}")
        return

    typer.echo(output)


def _run_compose(dest: Path, action: str) -> None:
    command = ["docker", "compose", "-f", str(dest / "docker-compose.yaml"), action]
    subprocess.check_call(command)


@compose_command("up")
def compose_up(dest: Path = typer.Option(Path("/opt/guardrail"), "--dest")) -> None:
    _run_compose(dest, "up")


@compose_command("down")
def compose_down(dest: Path = typer.Option(Path("/opt/guardrail"), "--dest")) -> None:
    _run_compose(dest, "down")


def _tenant_headers(token: Optional[str]) -> Dict[str, str]:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _handle_admin_error(response: requests.Response) -> None:
    detail = response.text.strip()
    if detail:
        _echo_error(f"admin API error: {response.status_code} {detail}")
    else:
        _echo_error(f"admin API error: {response.status_code}")


@tenant_command("create")
def tenant_create(
    ctx: typer.Context,
    tenant_id: str = typer.Option(..., "--id", help="Tenant identifier"),
    admin_user: str = typer.Option(..., "--admin-user", help="Admin user email"),
    url: Optional[str] = typer.Option(None, "--url", help="Admin API base URL"),
    token: Optional[str] = typer.Option(None, "--token", help="Admin API token"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
) -> None:
    base_url = config.resolve_admin_url(url).rstrip("/")
    resolved_token = config.resolve_admin_token(token)
    payload = {"id": tenant_id, "admin_user": admin_user}
    try:
        response = requests.post(
            f"{base_url}/admin/api/tenants",
            json=payload,
            headers=_tenant_headers(resolved_token),
            timeout=30,
        )
    except requests.RequestException as exc:
        _echo_error(f"failed to reach admin API: {exc}")
        raise typer.Exit(code=1) from exc
    if response.status_code >= 400:
        _handle_admin_error(response)
        raise typer.Exit(code=1)
    data: Any
    try:
        data = response.json()
    except ValueError:
        data = {"id": tenant_id, "admin_user": admin_user}
    if json_output:
        typer.echo(json.dumps(data, indent=2))
        return
    _echo(ctx, f"Created tenant {tenant_id} for admin {admin_user}")


@tenant_command("list")
def tenant_list(
    ctx: typer.Context,
    url: Optional[str] = typer.Option(None, "--url", help="Admin API base URL"),
    token: Optional[str] = typer.Option(None, "--token", help="Admin API token"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
) -> None:
    base_url = config.resolve_admin_url(url).rstrip("/")
    resolved_token = config.resolve_admin_token(token)
    try:
        response = requests.get(
            f"{base_url}/admin/api/tenants",
            headers=_tenant_headers(resolved_token),
            timeout=30,
        )
    except requests.RequestException as exc:
        _echo_error(f"failed to reach admin API: {exc}")
        raise typer.Exit(code=1) from exc
    if response.status_code >= 400:
        _handle_admin_error(response)
        raise typer.Exit(code=1)
    try:
        tenants = response.json()
    except ValueError:
        tenants = []
    if json_output:
        typer.echo(json.dumps({"tenants": tenants}, indent=2))
        return
    if not tenants:
        _echo(ctx, "No tenants found")
        return
    for tenant in tenants:
        if isinstance(tenant, Mapping):
            tenant_id = tenant.get("id", "<unknown>")
            admin = tenant.get("admin_user", "<unknown>")
            _echo(ctx, f"{tenant_id}: {admin}")
        else:
            _echo(ctx, str(tenant))


@channels_command("list")
def channels_list(
    ctx: typer.Context,
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
) -> None:
    try:
        channels = config.load_channels()
    except ValueError as exc:
        _echo_error(str(exc))
        raise typer.Exit(code=1) from exc
    data = {edition: asdict(channel) for edition, channel in channels.items()}
    if json_output:
        typer.echo(json.dumps(data, indent=2))
        return
    for edition, channel in data.items():
        _echo(ctx, f"{edition}: owner={channel['owner']} repo={channel['repo']}")


@channels_command("set")
def channels_set(
    ctx: typer.Context,
    edition: str = typer.Option(..., "--edition", help="Edition to override"),
    owner: str = typer.Option(..., "--owner", help="Repository owner"),
    repo: str = typer.Option(..., "--repo", help="Repository name"),
) -> None:
    override_path = config.channels_override_location()
    data: Dict[str, Any] = {}
    if override_path.exists():
        try:
            data = yaml.safe_load(override_path.read_text("utf-8")) or {}
        except yaml.YAMLError as exc:
            _echo_error(f"failed to read override file: {exc}")
            raise typer.Exit(code=1) from exc
    channels_section = data.get("channels", {})
    if channels_section and not isinstance(channels_section, dict):
        _echo_error("override file must contain a mapping under 'channels'")
        raise typer.Exit(code=1)
    edition_data = dict(channels_section.get(edition, {})) if isinstance(channels_section, dict) else {}
    edition_data["owner"] = owner
    edition_data["repo"] = repo
    channels_section = channels_section if isinstance(channels_section, dict) else {}
    channels_section[edition] = edition_data
    data["channels"] = channels_section
    override_path.parent.mkdir(parents=True, exist_ok=True)
    override_path.write_text(yaml.safe_dump(data, sort_keys=False), "utf-8")
    _echo(ctx, f"Wrote overrides to {override_path}")


@helm_command("render")
def helm_render(
    ctx: typer.Context,
    values_files: List[Path] = typer.Option([], "--values", help="Values files to merge"),
    out: Path = typer.Option(Path("./manifests"), "--out", help="Output directory"),
) -> None:
    defaults = yaml.safe_load(env.get_template("helm/values.yaml").render()) or {}
    if not isinstance(defaults, Mapping):
        _echo_error("helm values template must render to a mapping")
        raise typer.Exit(code=1)
    merged: Mapping[str, Any] = cast(Mapping[str, Any], defaults)
    for path in values_files:
        if not path.exists():
            _echo_error(f"values file {path} not found")
            raise typer.Exit(code=1)
        try:
            override = yaml.safe_load(path.read_text("utf-8")) or {}
        except yaml.YAMLError as exc:
            _echo_error(f"failed to parse {path}: {exc}")
            raise typer.Exit(code=1) from exc
        if not isinstance(override, Mapping):
            _echo_error(f"values file {path} must contain a mapping")
            raise typer.Exit(code=1)
        merged = _merge_dict(merged, override)

    out.mkdir(parents=True, exist_ok=True)
    merged_values = yaml.safe_dump(merged, sort_keys=False)
    _write_file(out / "values.merged.yaml", merged_values)

    template_names = [
        name
        for name in env.list_templates()
        if name.startswith("helm/templates/")
    ]
    for template_name in template_names:
        template = env.get_template(template_name)
        rendered = template.render(Values=merged)
        target = out / Path(template_name).name
        _write_file(target, rendered)

    notes_template = env.get_template("helm/NOTES.txt")
    notes = notes_template.render(output=str(out))
    _write_file(out / "NOTES.txt", notes)

    _echo(ctx, f"Rendered Helm manifests to {out}")
