#!/usr/bin/env python3
"""Keep Weasel and Squirrel theme display names tidy and deterministic."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "desktop_theme_names.yaml"
TARGETS = (ROOT / "weasel.yaml", ROOT / "squirrel.yaml")
THEME_HEADER = re.compile(r"^  (\S[^:]*):(?:\s+#.*)?\s*$")


def rules() -> tuple[dict[str, str], set[str]]:
    document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    names = document["names"]
    removed = set(document["removed"])
    if set(names) & removed:
        raise ValueError("theme IDs cannot be both named and removed")
    return names, removed


def normalized_text(path: Path, names: dict[str, str], removed: set[str]) -> str:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    output: list[str] = []
    in_schemes = False
    current_theme: str | None = None
    skip_theme = False
    seen: set[str] = set()

    for line in lines:
        if line == "preset_color_schemes:":
            in_schemes = True
            output.append(line)
            continue

        if in_schemes and line and not line.startswith(" "):
            in_schemes = False
            current_theme = None
            skip_theme = False

        match = THEME_HEADER.match(line) if in_schemes else None
        if match:
            current_theme = match.group(1).strip("'\"")
            seen.add(current_theme)
            skip_theme = current_theme in removed
            if skip_theme:
                continue
            if current_theme not in names:
                raise ValueError(f"{path.name}: missing canonical name for {current_theme}")
            output.append(line)
            output.append(f'    name: "{names[current_theme]}"')
            continue

        if skip_theme:
            continue
        if current_theme and re.match(r"^    (?:name|creat_time):", line):
            continue
        output.append(line)

    unknown = seen - set(names) - removed
    if unknown:
        raise ValueError(f"{path.name}: unknown themes: {', '.join(sorted(unknown))}")
    return "\n".join(output).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    names, removed = rules()
    stale: list[str] = []

    for path in TARGETS:
        expected = normalized_text(path, names, removed)
        current = path.read_text(encoding="utf-8-sig")
        if current != expected:
            if args.check:
                stale.append(path.name)
            else:
                path.write_text(expected, encoding="utf-8", newline="\n")

    if stale:
        print("Desktop theme names are stale: " + ", ".join(stale))
        return 1
    if args.check:
        print("Desktop theme names are canonical")
    else:
        print("Normalized desktop theme names")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
