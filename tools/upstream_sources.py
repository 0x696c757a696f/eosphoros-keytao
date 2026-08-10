#!/usr/bin/env python3
"""Read pinned upstream source files from GitHub or a local checkout."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any


USER_AGENT = "eosphoros-sync/1"


def raw_url(source: dict[str, Any], relative_path: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{source['repository']}/"
        f"{source['commit']}/{relative_path}"
    )


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read().decode("utf-8-sig")


def resolve_ref(repository: str, branch: str) -> str:
    url = f"https://api.github.com/repos/{repository}/commits/{branch}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = json.load(response)
    return str(payload["sha"])


def read_source(
    source: dict[str, Any], relative_path: str, local_root: Path | None
) -> str:
    if local_root is not None:
        return (local_root / relative_path).read_text(encoding="utf-8-sig")
    return fetch_text(raw_url(source, relative_path))
