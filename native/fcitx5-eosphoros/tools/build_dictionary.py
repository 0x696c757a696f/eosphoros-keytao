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


MAGIC = b"EOSDICT3"
VERSION = 3


@dataclass(frozen=True)
class Entry:
    text: str
    code: str
    weight: int
    namespace: str = ""


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
    sort_mode = "original"
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        for line_number, raw in enumerate(source, 1):
            line = raw.rstrip("\r\n")
            if not in_body:
                if line.strip().startswith("sort:"):
                    sort_mode = line.split(":", 1)[1].strip().split("#", 1)[0].strip()
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
    if sort_mode == "by_weight":
        # Python's sort is stable, so equal weights retain source order.
        entries.sort(key=lambda entry: entry.weight, reverse=True)
    return entries


def read_manifest(path: Path, root: Path) -> list[tuple[str, Path]]:
    """Read PREFIX<TAB>REPOSITORY_RELATIVE_PATH rows in declared order."""
    result: list[tuple[str, Path]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) == 1:
            prefix, relative = "", fields[0]
        elif len(fields) == 2:
            prefix, relative = fields
        else:
            raise ValueError(f"{path}:{line_number}: expected [prefix TAB] path")
        if prefix and (len(prefix) != 1 or prefix not in "iuvo"):
            raise ValueError(f"{path}:{line_number}: unsupported namespace prefix")
        source = root / relative
        if not source.is_file():
            raise ValueError(f"{path}:{line_number}: missing dictionary {source}")
        result.append((prefix, source))
    return result


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
            namespace = ord(entry.namespace) if entry.namespace else 0
            target.write(struct.pack("<IIiB", len(code), len(text), entry.weight, namespace))
            target.write(code)
            target.write(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--input", action="append", type=Path, default=[])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sources = [("", path) for path in args.input]
    if args.manifest:
        sources.extend(read_manifest(args.manifest, args.root))
    if not sources:
        parser.error("at least one --input or --manifest is required")

    entries: list[Entry] = []
    for prefix, input_path in sources:
        source_entries = read_rime_dictionary(input_path)
        entries.extend(
            Entry(
                entry.text,
                entry.code if prefix and entry.code.startswith(prefix) else prefix + entry.code,
                entry.weight,
                prefix,
            )
            for entry in source_entries
        )
    write_dictionary(args.output, read_native_config(args.schema), entries)
    print(f"built {args.output}: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
