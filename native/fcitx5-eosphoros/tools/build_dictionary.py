#!/usr/bin/env python3
"""Build the deterministic native Eosphoros dictionary.

Input is one or more Rime dictionary YAML files. Only the tab-separated body is
read; the runtime never parses YAML and has no dependency on librime.
"""

from __future__ import annotations

import argparse
import struct
from dataclasses import dataclass
from pathlib import Path


MAGIC = b"EOSDICT1"
VERSION = 1


@dataclass(frozen=True)
class Entry:
    text: str
    code: str
    weight: int


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


def write_dictionary(path: Path, entries: list[Entry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as target:
        target.write(MAGIC)
        target.write(struct.pack("<II", VERSION, len(entries)))
        for entry in entries:
            code = entry.code.encode("ascii")
            text = entry.text.encode("utf-8")
            target.write(struct.pack("<IIi", len(code), len(text), entry.weight))
            target.write(code)
            target.write(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    entries: list[Entry] = []
    for input_path in args.input:
        entries.extend(read_rime_dictionary(input_path))
    write_dictionary(args.output, entries)
    print(f"built {args.output}: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
