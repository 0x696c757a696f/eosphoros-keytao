#!/usr/bin/env python3
"""Fingerprint tracked inputs that can affect native CI packages."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PREFIXES = (".github/ISSUE_TEMPLATE/", "docs/", "tests/")
EXCLUDED_NAMES = {"README.md"}


def affects_native_packages(path: str) -> bool:
    normalized = PurePosixPath(path).as_posix()
    return normalized not in EXCLUDED_NAMES and not normalized.startswith(
        EXCLUDED_PREFIXES
    )


def tracked_paths(root: Path = ROOT) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return sorted(
        path
        for path in result.stdout.decode("utf-8").split("\0")
        if path and affects_native_packages(path)
    )


def fingerprint(root: Path = ROOT) -> str:
    digest = hashlib.sha256()
    for relative in tracked_paths(root):
        path = root / relative
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


if __name__ == "__main__":
    print(fingerprint())
