from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from guardrailctl import io


def _write_checksum(path: Path, digest: str) -> None:
    path.write_text(f"{digest}  artifact.tgz\n", "utf-8")


def test_verify_checksum_success(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.tgz"
    artifact.write_bytes(b"payload")
    digest = hashlib.sha256(b"payload").hexdigest()
    checksum = tmp_path / "artifact.tgz.sha256"
    _write_checksum(checksum, digest)
    assert io.verify_checksum(artifact, checksum) == digest


def test_verify_checksum_failure(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.tgz"
    artifact.write_bytes(b"payload")
    checksum = tmp_path / "artifact.tgz.sha256"
    wrong_digest = hashlib.sha256(b"other").hexdigest()
    _write_checksum(checksum, wrong_digest)
    with pytest.raises(io.ChecksumMismatchError):
        io.verify_checksum(artifact, checksum)


def test_atomic_symlink_updates_target(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    link = tmp_path / "current"
    os.symlink(first, link)

    io.atomic_symlink(second, link)

    assert link.is_symlink()
    assert link.resolve() == second.resolve()
