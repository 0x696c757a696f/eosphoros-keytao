#!/usr/bin/env python3
"""Compile native pronunciation and Emoji lookup data without Lua at runtime."""

from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path


MAGIC = b"EOSAUX03"
LUA_ROW = re.compile(r'^  \[("(?:[^"\\]|\\.)*")\] = ("(?:[^"\\]|\\.)*"),?$')


def pronunciations(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    body = False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not body:
            body = line.strip() == "..."
            continue
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) >= 2 and fields[0] not in result:
            value = fields[1].strip()
            if value.startswith("(") and value.endswith(")"):
                result[fields[0]] = value[1:-1].replace("_", "、")
    return result


def emoji_rows(root: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for path in sorted(root.glob("eosphoros_emoji*_*.lua")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.startswith("  ["):
                continue
            match = LUA_ROW.match(line)
            if not match:
                raise ValueError(f"{path}:{line_number}: unsupported generated Lua row")
            key, value = json.loads(match.group(1)), json.loads(match.group(2))
            bucket = result.setdefault(key, [])
            for item in value.split(" "):
                if item and item not in bucket:
                    bucket.append(item)
    return result


def conversion_rows(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.glob("eosphoros_s2g_*.lua")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.startswith("  ["):
                continue
            match = LUA_ROW.match(line)
            if not match:
                raise ValueError(f"{path}:{line_number}: unsupported generated Lua row")
            result.setdefault(json.loads(match.group(1)), json.loads(match.group(2)))
    return result


def character_parts(path: Path) -> dict[str, tuple[str, str, str]]:
    result: dict[str, tuple[str, str, str]] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 4:
            raise ValueError(f"{path}:{line_number}: invalid character-parts row")
        result.setdefault(fields[0], (fields[1], fields[2], fields[3]))
    return result


def text(target: object, value: str) -> None:
    data = value.encode("utf-8")
    target.write(struct.pack("<I", len(data)))
    target.write(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pronunciation", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pron = pronunciations(args.pronunciation)
    emoji = emoji_rows(args.root / "opencc" / "eosphoros")
    parts = character_parts(args.root / "zzc_state" / "char_parts.tsv")
    conversion = conversion_rows(args.root / "opencc" / "eosphoros")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as target:
        target.write(MAGIC)
        target.write(struct.pack("<IIII", len(pron), len(emoji), len(parts), len(conversion)))
        for key, value in pron.items():
            text(target, key); text(target, value)
        for key, values in emoji.items():
            text(target, key)
            target.write(struct.pack("<I", len(values)))
            for value in values:
                text(target, value)
        for key, values in parts.items():
            text(target, key)
            for value in values:
                text(target, value)
        for key, value in conversion.items():
            text(target, key); text(target, value)
    print(f"built {args.output}: {len(pron)} pronunciations, {len(emoji)} emoji keys, {len(parts)} character parts, {len(conversion)} conversion rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
