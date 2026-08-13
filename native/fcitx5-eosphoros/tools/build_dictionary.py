#!/usr/bin/env python3
"""Build the deterministic native Eosphoros dictionary.

Input is one or more Rime dictionary YAML files. Only the tab-separated body is
read; the runtime never parses YAML and has no dependency on librime.
"""

from __future__ import annotations

import argparse
import re
import struct
from dataclasses import dataclass
from pathlib import Path


MAGIC = b"EOSDICT2"
VERSION = 2


@dataclass(frozen=True)
class Entry:
    text: str
    code: str
    weight: int


@dataclass(frozen=True)
class NativeConfig:
    topup_this: str
    topup_with: str
    min_length: int
    max_length: int
    auto_clear: bool
    topup_command: bool
    page_size: int


def read_schema_section(path: Path, section: str) -> dict[str, str]:
    values: dict[str, str] = {}
    active = False
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        if not raw.startswith((" ", "\t")):
            active = raw.strip() == f"{section}:"
            continue
        if not active:
            continue
        match = re.match(r"^\s{2}([A-Za-z0-9_]+):\s*(.*?)\s*$", raw)
        if not match:
            continue
        value = match.group(2).split("#", 1)[0].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[match.group(1)] = value
    return values


def read_native_config(path: Path) -> NativeConfig:
    topup = read_schema_section(path, "topup")
    menu = read_schema_section(path, "menu")
    required = {
        "topup_this",
        "topup_with",
        "min_length",
        "max_length",
        "auto_clear",
        "topup_command",
    }
    missing = sorted(required.difference(topup))
    if missing:
        raise ValueError(f"{path}: missing native topup settings: {', '.join(missing)}")

    def boolean(name: str) -> bool:
        value = topup[name].lower()
        if value in {"true", "1", "yes", "on"}:
            return True
        if value in {"false", "0", "no", "off"}:
            return False
        raise ValueError(f"{path}: invalid boolean for topup/{name}: {topup[name]}")

    return NativeConfig(
        topup_this=topup["topup_this"],
        topup_with=topup["topup_with"],
        min_length=int(topup["min_length"]),
        max_length=int(topup["max_length"]),
        auto_clear=boolean("auto_clear"),
        topup_command=boolean("topup_command"),
        page_size=int(menu.get("page_size", "5")),
    )


def parse_weight(value: str) -> int:
    value = value.strip().rstrip("%")
    if not value:
        return 0
    try:
        return int(float(value))
    except ValueError:
        return 0


def read_rime_dictionary(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    in_body = False
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        for line_number, raw in enumerate(source, 1):
            line = raw.rstrip("\r\n")
            if not in_body:
                if line.strip() == "...":
                    in_body = True
                continue
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) < 2:
                continue
            text, code = fields[0].strip(), fields[1].strip()
            if not text or not code or len(code.encode("ascii", "ignore")) != len(code):
                raise ValueError(f"{path}:{line_number}: invalid text/code row")
            weight = parse_weight(fields[2]) if len(fields) > 2 else 0
            entries.append(Entry(text, code, weight))
    if not in_body:
        raise ValueError(f"{path}: missing Rime dictionary body marker (...)")
    return entries


def write_string(target: object, value: str) -> None:
    encoded = value.encode("ascii")
    target.write(struct.pack("<I", len(encoded)))
    target.write(encoded)


def write_dictionary(path: Path, config: NativeConfig, entries: list[Entry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as target:
        target.write(MAGIC)
        target.write(struct.pack("<I", VERSION))
        write_string(target, config.topup_this)
        write_string(target, config.topup_with)
        target.write(
            struct.pack(
                "<IIIIII",
                config.min_length,
                config.max_length,
                int(config.auto_clear),
                int(config.topup_command),
                config.page_size,
                len(entries),
            )
        )
        for entry in entries:
            code = entry.code.encode("ascii")
            text = entry.text.encode("utf-8")
            target.write(struct.pack("<IIi", len(code), len(text), entry.weight))
            target.write(code)
            target.write(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    entries: list[Entry] = []
    for input_path in args.input:
        entries.extend(read_rime_dictionary(input_path))
    write_dictionary(args.output, read_native_config(args.schema), entries)
    print(f"built {args.output}: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
