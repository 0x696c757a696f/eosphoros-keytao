#!/usr/bin/env python3
"""Report direct xmjd6-rere commits added since the last manual review."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "tools" / "legacy_upstream.lock.json"


def remote_commit(repository: str, ref: str) -> str:
    result = subprocess.run(
        ["git", "ls-remote", repository, ref],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    rows = [line.split() for line in result.stdout.splitlines() if line.strip()]
    if len(rows) != 1:
        raise RuntimeError(f"cannot resolve {ref} from {repository}")
    return rows[0][0]


def build_report() -> dict[str, object]:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    current = remote_commit(lock["repository"], lock["ref"])
    reviewed = lock["reviewed_commit"]
    return {
        "repository": lock["repository"],
        "ref": lock["ref"],
        "reviewed_commit": reviewed,
        "current_commit": current,
        "update_available": current != reviewed,
        "compare_url": (
            "https://github.com/hugh7007/xmjd6-rere/compare/"
            f"{reviewed}...{current}"
        ),
        "policy": lock["review"]["dictionary_policy"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-update", action="store_true")
    args = parser.parse_args()
    try:
        report = build_report()
    except (OSError, subprocess.CalledProcessError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print(f"xmjd6-rere check failed: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif report["update_available"]:
        print(
            "xmjd6-rere has changed: "
            f"{report['reviewed_commit']} -> {report['current_commit']}"
        )
        print(report["compare_url"])
        print("Review selectively; do not replace local dictionaries or renamed paths.")
    else:
        print(f"xmjd6-rere is reviewed through {report['reviewed_commit']}")
    return 10 if args.fail_on_update and report["update_available"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
