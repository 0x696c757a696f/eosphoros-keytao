#!/usr/bin/env python3
"""Refresh the pinned Mira runtime checksums.

Mira only publishes a rolling ``latest`` release. This script downloads every
binary listed in ``tools/mira_runtime.lock.json``, keeps it under ``.tmp/mira``
so the caller can test it, and with ``--write`` records the new SHA-256 values.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "tools" / "mira_runtime.lock.json"
DOWNLOAD_DIR = ROOT / ".tmp" / "mira"
USER_AGENT = "eosphoros-sync/1"


def load_lock(path: Path = LOCK_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render_lock(lock: dict[str, Any]) -> str:
    return json.dumps(lock, ensure_ascii=False, indent=2) + "\n"


def download(release: str, binary: str) -> str:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(release + binary, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    target = DOWNLOAD_DIR / binary
    target.write_bytes(data)
    target.chmod(0o755)
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="record new checksums in the lock")
    args = parser.parse_args()

    lock = load_lock()
    pinned: dict[str, str] = lock["binaries"]
    current = {binary: download(lock["release"], binary) for binary in pinned}
    for binary in sorted(pinned):
        state = "unchanged" if pinned[binary] == current[binary] else "changed"
        print(f"{binary}: {state} {current[binary]}")

    if args.write and current != pinned:
        lock["binaries"] = current
        LOCK_PATH.write_text(render_lock(lock), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
