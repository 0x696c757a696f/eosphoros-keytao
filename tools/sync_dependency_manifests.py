#!/usr/bin/env python3
"""Keep Pixi's direct Python dependency pins aligned with requirements files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIXI_TOML = ROOT / "pixi.toml"
SOURCES = {
    "pip": (ROOT / "requirements-ci.txt", "pip", "conda"),
    "pyyaml": (ROOT / "requirements-dev.txt", "PyYAML", "conda"),
    "pillow": (ROOT / "requirements-dev.txt", "Pillow", "conda"),
    "pyinstaller": (ROOT / "requirements-build.txt", "PyInstaller", "pypi"),
}


def pinned_version(path: Path, package: str) -> str:
    pattern = re.compile(rf"^{re.escape(package)}==([^\s#]+)", re.IGNORECASE)
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if match:
            return match.group(1)
    raise ValueError(f"missing exact {package} pin in {path.name}")


def conda_constraint(version: str) -> str:
    parts = version.split(".")
    if len(parts) < 2 or not all(part.isdigit() for part in parts):
        raise ValueError(f"unsupported version: {version}")
    return version + ".*"


def render_pixi() -> str:
    text = PIXI_TOML.read_text(encoding="utf-8")
    for key, (path, package, ecosystem) in SOURCES.items():
        version = pinned_version(path, package)
        constraint = conda_constraint(version) if ecosystem == "conda" else f"=={version}"
        pattern = re.compile(rf"(?m)^{re.escape(key)}\s*=\s*\"[^\"]+\"$")
        text, count = pattern.subn(f'{key} = "{constraint}"', text)
        if count != 1:
            raise ValueError(f"expected one {key} dependency in pixi.toml, found {count}")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="update pixi.toml")
    mode.add_argument("--check", action="store_true", help="fail if pixi.toml is stale")
    args = parser.parse_args()

    current = PIXI_TOML.read_text(encoding="utf-8")
    expected = render_pixi()
    if current == expected:
        print("Dependency manifests are aligned")
        return 0
    if args.write:
        PIXI_TOML.write_text(expected, encoding="utf-8", newline="\n")
        print("Updated pixi.toml from requirements files")
        return 0
    print("pixi.toml is stale; run tools/sync_dependency_manifests.py --write")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
