#!/usr/bin/env python3
"""Remove invalid-code rows when the same word already has a legal row."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.clean_dictionary_quality import valid_word_codes
from tools.eosphoros_codes import iter_dictionary_rows, load_character_code_options


ROOT = Path(__file__).resolve().parents[1]
DICT_DIR = ROOT / "dicts" / "eosphoros"
TARGET_NAMES = {
    "eosphoros.cizu.dict.yaml",
    "eosphoros.fjcy.dict.yaml",
}


@dataclass(frozen=True)
class Removal:
    filename: str
    position: int
    word: str
    code: str


def plan_removals(root: Path = ROOT) -> tuple[Removal, ...]:
    dictionary_dir = root / "dicts" / "eosphoros"
    options = load_character_code_options(
        dictionary_dir / "eosphoros.danzi.dict.yaml"
    )
    rows_by_word: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    target_words: set[str] = set()
    for filename in sorted(TARGET_NAMES):
        path = dictionary_dir / filename
        for position, (word, code) in enumerate(iter_dictionary_rows(path)):
            rows_by_word[word].append((path.name, position, code))
            target_words.add(word)

    # Only non-target rows whose text can validate a target duplicate matter.
    # Avoid computing legal codes for the million-plus unrelated upstream rows.
    for path in sorted(dictionary_dir.glob("*.dict.yaml")):
        if path.name == "eosphoros.danzi.dict.yaml" or path.name in TARGET_NAMES:
            continue
        for position, (word, code) in enumerate(iter_dictionary_rows(path)):
            if word in target_words:
                rows_by_word[word].append((path.name, position, code))

    removals: list[Removal] = []
    for word, rows in rows_by_word.items():
        if len(rows) < 2:
            continue
        valid = valid_word_codes(word, options)
        if not valid or not any(code in valid for _, _, code in rows):
            continue
        for filename, position, code in rows:
            if filename in TARGET_NAMES and code not in valid:
                removals.append(Removal(filename, position, word, code))
    return tuple(
        sorted(removals, key=lambda row: (row.filename, row.position))
    )


def rewrite_target(path: Path, removals: dict[int, Removal]) -> None:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    in_data = False
    position = 0
    output: list[str] = []
    for line in lines:
        if line.strip() == "...":
            in_data = True
            output.append(line)
            continue
        if in_data and line.strip() and not line.lstrip().startswith("#"):
            fields = line.split("\t")
            if len(fields) >= 2 and fields[0] and fields[1]:
                removal = removals.get(position)
                if removal is not None:
                    if (fields[0], fields[1]) != (removal.word, removal.code):
                        raise ValueError(
                            f"{path}:{position}: row changed while planning removals"
                        )
                    position += 1
                    continue
                position += 1
        output.append(line)
    path.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()

    removals = plan_removals(ROOT)
    by_file: dict[str, dict[int, Removal]] = defaultdict(dict)
    for removal in removals:
        by_file[removal.filename][removal.position] = removal
    print(
        "Invalid duplicate codes: "
        + str(len(removals))
        + " pending"
        + (
            " ("
            + ", ".join(
                f"{filename}={len(rows)}" for filename, rows in sorted(by_file.items())
            )
            + ")"
            if by_file
            else ""
        )
    )
    if args.check:
        return 1 if removals else 0
    for filename, file_removals in by_file.items():
        rewrite_target(DICT_DIR / filename, file_removals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
