from __future__ import annotations

import hashlib
import os
import tarfile
from pathlib import Path
from typing import Iterable, Tuple


class ChecksumMismatchError(Exception):
    """Raised when a checksum validation fails."""


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_checksum_file(path: Path) -> Tuple[str, str]:
    lines = path.read_text("utf-8").splitlines()
    if not lines:
        raise ValueError(f"checksum file {path} is empty")
    parts = lines[0].split()
    if len(parts) < 2:
        raise ValueError(f"checksum file {path} has invalid format")
    return parts[0], parts[-1]


def verify_checksum(artifact: Path, checksum_file: Path) -> str:
    expected, _ = read_checksum_file(checksum_file)
    actual = sha256sum(artifact)
    if actual != expected:
        raise ChecksumMismatchError(
            f"checksum mismatch for {artifact}: {actual} != {expected}"
        )
    return actual


def extract_tarball(archive: Path, dest: Path) -> Iterable[str]:
    dest.mkdir(parents=True, exist_ok=True)
    names: list[str] = []
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar.getmembers():
            names.append(member.name)
        tar.extractall(dest)
    return names


def atomic_symlink(target: Path, link: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    tmp_link = link.parent / f".{link.name}.tmp"
    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()
    os.symlink(target, tmp_link)
    os.replace(tmp_link, link)
