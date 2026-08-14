#!/usr/bin/env python3
"""Update VERSION and all top-level Rime version fields together."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_RE = re.compile(
    r"^(\s*(?:(?:config_)?version|generated):\s*)([\"']?)\d{4}-\d{2}-\d{2}[\"']?",
    re.MULTILINE,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("date", nargs="?", default=dt.date.today().isoformat())
    args = parser.parse_args()
    try:
        dt.date.fromisoformat(args.date)
    except ValueError as exc:
        parser.error(str(exc))

    lock_path = ROOT / "tools" / "upstream_dictionaries.lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    for relative, metadata in lock.get("generated", {}).items():
        path = ROOT / relative
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != metadata["sha256"]:
            raise RuntimeError(
                f"refusing to refresh upstream lock for modified file: {relative}"
            )

    (ROOT / "VERSION").write_text(args.date + "\n", encoding="utf-8", newline="\n")
    changed = 0
    yaml_paths = list(ROOT.glob("*.yaml"))
    yaml_paths.extend((ROOT / "dicts" / "eosphoros").glob("*.yaml"))
    yaml_paths.extend(
        (
            ROOT / "mobile_themes" / "palettes.yaml",
            ROOT / "fcitx5" / "themes.yaml",
        )
    )
    for path in sorted(yaml_paths):
        original = path.read_text(encoding="utf-8-sig")
        def replace_version(match: re.Match[str]) -> str:
            quote = match.group(2) or '"'
            return f"{match.group(1)}{quote}{args.date}{quote}"

        updated, count = VERSION_RE.subn(replace_version, original)
        if count and updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed += 1
    lock["generated_on"] = args.date
    for relative, metadata in lock.get("generated", {}).items():
        metadata["sha256"] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    lock_path.write_text(
        json.dumps(lock, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Updated VERSION and {changed} YAML file(s) to {args.date}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
