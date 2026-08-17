#!/usr/bin/env python3
"""Refresh the immutable OpenCC release asset lock."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCK = ROOT / "tools" / "opencc.lock.json"
DIGEST_PATTERN = re.compile(r"^sha256:([0-9a-f]{64})$", re.IGNORECASE)


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "eosphoros-opencc-updater",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def refreshed_lock(current: dict[str, Any]) -> dict[str, Any]:
    repository = str(current["repository"])
    tag = str(current["tag"])
    asset_name = str(current["asset"])
    release = fetch_json(
        f"https://api.github.com/repos/{repository}/releases/tags/{tag}"
    )
    asset = next(
        (candidate for candidate in release["assets"] if candidate["name"] == asset_name),
        None,
    )
    if asset is None:
        raise ValueError(f"release {tag} has no asset named {asset_name}")
    match = DIGEST_PATTERN.fullmatch(str(asset.get("digest") or ""))
    if match is None:
        raise ValueError(f"release asset {asset_name} has no valid SHA-256 digest")
    return {
        "repository": repository,
        "tag": tag,
        "release_id": int(release["id"]),
        "asset": asset_name,
        "asset_id": int(asset["id"]),
        "url": str(asset["url"]),
        "sha256": match.group(1).lower(),
    }


def render_lock(lock: dict[str, Any]) -> str:
    return json.dumps(lock, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    args = parser.parse_args()

    current = json.loads(args.lock.read_text(encoding="utf-8"))
    expected = render_lock(refreshed_lock(current))
    actual = args.lock.read_text(encoding="utf-8")
    if actual == expected:
        print("OpenCC release asset lock is current")
        return 0
    if args.write:
        args.lock.write_text(expected, encoding="utf-8", newline="\n")
        print("Updated OpenCC release asset lock")
        return 0
    if args.check:
        print("OpenCC release asset lock is stale")
        return 1
    print(expected, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
