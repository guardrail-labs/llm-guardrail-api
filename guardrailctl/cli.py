from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple, TypeVar, cast
from typing import Callable

import requests
import typer
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

R = TypeVar("R")

app = typer.Typer(add_completion=False)


def _typed_command(*args: Any, **kwargs: Any) -> Callable[[Callable[..., R]], Callable[..., R]]:
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        command = app.command(*args, **kwargs)(func)
        return cast(Callable[..., R], command)

    return decorator


env = Environment(
    loader=PackageLoader("guardrailctl", "templates"),
    autoescape=select_autoescape(),
)


def _load_channels() -> Dict[str, Any]:
    config_path = Path(__file__).parent / "channels.yaml"
    data = yaml.safe_load(config_path.read_text("utf-8"))
    channels = data.get("channels", {})
    if not channels:
        raise RuntimeError("channels.yaml missing channel definitions")
    return cast(Dict[str, Any], channels)


def _gh_release_assets(owner: str, repo: str, tag: str) -> list[dict[str, Any]]:
    headers: dict[str, str] = {}
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
    return assets


def _download_asset(url: str, out: Path) -> None:
    with requests.get(url, stream=True, timeout=60) as stream:
        stream.raise_for_status()
        with out.open("wb") as file:
            for chunk in stream.iter_content(chunk_size=1 << 16):
                if chunk:
                    file.write(chunk)


def _fetch(owner: str, repo: str, tag: str, names: Iterable[str], dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    assets = _gh_release_assets(owner, repo, tag)
    required = {name: False for name in names}
    for asset in assets:
        name = asset.get("name")
        if name in required:
            _download_asset(asset["browser_download_url"], dest / name)
            required[name] = True
    missing = [name for name, present in required.items() if not present]
    if missing:
        raise RuntimeError(f"Missing assets: {', '.join(missing)}")


def _read_checksum(file: Path) -> Tuple[str, str]:
    line = file.read_text("utf-8").strip().splitlines()[0]
    parts = line.split()
    if len(parts) < 2:
        raise RuntimeError(f"Invalid checksum format in {file}")
    return parts[0], parts[-1]


def _sha256(file: Path) -> str:
    digest = hashlib.sha256()
    with file.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


@_typed_command()
def channels(cmd: str = typer.Argument("list")) -> None:
    channel_map = _load_channels()
    if cmd == "list":
        typer.echo(json.dumps(channel_map, indent=2))
        return
    typer.echo("Supported: list", err=True)
    raise typer.Exit(code=2)


def _prepare_build_tree(source: Path, artifact: str) -> Path:
    build_dir = source / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = source / artifact
    target = build_dir / artifact
    artifact_path.replace(target)
    return target


@_typed_command()
def verify(
    tag: str = typer.Option(..., "--tag"),
    edition: str = typer.Option("enterprise", "--edition"),
) -> None:
    channels_map = _load_channels()
    if edition not in channels_map:
        typer.echo(f"Unknown edition: {edition}", err=True)
        raise typer.Exit(code=2)
    channel = channels_map[edition]
    owner = channel["owner"]
    repo = channel["repo"]
    artifact = channel["artifact"].replace("${tag}", tag)
    checksum = channel["checksum"].replace("${tag}", tag)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        _fetch(owner, repo, tag, (artifact, checksum), tmp_path)
        checksum_path = tmp_path / checksum
        artifact_path = _prepare_build_tree(tmp_path, artifact)
        expected, _ = _read_checksum(checksum_path)
        calculated = _sha256(artifact_path)
        if calculated != expected:
            typer.echo(f"Checksum mismatch: {calculated} != {expected}", err=True)
            raise typer.Exit(code=1)
        typer.echo("SHA256 OK")
        with tarfile.open(artifact_path, "r:gz") as archive:
            for index, member in enumerate(archive.getmembers()):
                typer.echo(member.name)
                if index >= 9:
                    break


@_typed_command()
def install(
    tag: str = typer.Option(..., "--tag"),
    edition: str = typer.Option("enterprise", "--edition"),
    dest: Path = typer.Option(Path("/opt/guardrail"), "--dest"),
) -> None:
    channels_map = _load_channels()
    if edition not in channels_map:
        typer.echo(f"Unknown edition: {edition}", err=True)
        raise typer.Exit(code=2)
    channel = channels_map[edition]
    owner = channel["owner"]
    repo = channel["repo"]
    artifact = channel["artifact"].replace("${tag}", tag)
    checksum = channel["checksum"].replace("${tag}", tag)
    dest.mkdir(parents=True, exist_ok=True)
    _fetch(owner, repo, tag, (artifact, checksum), dest)
    checksum_path = dest / checksum
    artifact_path = _prepare_build_tree(dest, artifact)
    expected, _ = _read_checksum(checksum_path)
    calculated = _sha256(artifact_path)
    if calculated != expected:
        typer.echo("Checksum mismatch on install", err=True)
        raise typer.Exit(code=1)
    with tarfile.open(artifact_path, "r:gz") as archive:
        archive.extractall(dest)
    typer.echo(f"Installed {edition} {tag} to {dest}")


@_typed_command("compose")
def compose_cmd(
    action: str = typer.Argument("init"),
    dest: Path = typer.Option(Path("/opt/guardrail"), "--dest"),
) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    if action == "init":
        docker_compose = env.get_template("docker-compose.yaml.j2").render()
        env_example = env.get_template("env.example.j2").render()
        (dest / "docker-compose.yaml").write_text(docker_compose, "utf-8")
        (dest / ".env.example").write_text(env_example, "utf-8")
        typer.echo("Wrote docker-compose.yaml and .env.example")
        return
    if action in {"up", "down"}:
        command = ["docker", "compose", "-f", str(dest / "docker-compose.yaml"), action]
        subprocess.check_call(command)
        return
    typer.echo("compose actions: init|up|down", err=True)
    raise typer.Exit(code=2)


@_typed_command("helm")
def helm_render(
    out: Path = typer.Option(Path("./manifests"), "--out"),
) -> None:
    out.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).parent / "templates" / "helm"
    for path in src.rglob("*"):
        if path.is_file():
            target = out / path.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(path.read_text("utf-8"), "utf-8")
    typer.echo(f"Rendered Helm starter chart to {out}")
