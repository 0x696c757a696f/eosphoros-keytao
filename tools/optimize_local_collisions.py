#!/usr/bin/env python3
"""Move low-priority local rows to free, longer JianDao codes.

The optimizer is intentionally conservative: it only edits the broad cizu and
fjcy dictionaries, keeps the highest-priority row on every shared code, and
uses a longer code from the row's existing pronunciation family. User data,
specialty dictionaries, short unique codes, and pronunciation choices are not
changed.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.clean_dictionary_quality import valid_word_codes
from tools.eosphoros_codes import iter_dictionary_rows, load_character_code_options
from tools.sync_upstream_dictionaries import (
    LOCAL_WORD_DICTIONARIES,
    collision_row_count,
)


ROOT = Path(__file__).resolve().parents[1]
DICT_DIR = ROOT / "dicts" / "eosphoros"
TARGET_NAMES = {
    "eosphoros.cizu.dict.yaml",
    "eosphoros.fjcy.dict.yaml",
}


@dataclass(frozen=True)
class Row:
    filename: str
    position: int
    word: str
    code: str


@dataclass(frozen=True)
class Move:
    row: Row
    new_code: str


def load_rows(root: Path = ROOT) -> tuple[list[Row], dict[str, list[Row]]]:
    rows: list[Row] = []
    owners: dict[str, list[Row]] = defaultdict(list)
    dictionary_dir = root / "dicts" / "eosphoros"
    for filename in LOCAL_WORD_DICTIONARIES:
        path = dictionary_dir / filename
        if not path.is_file():
            continue
        for position, (word, code) in enumerate(iter_dictionary_rows(path)):
            row = Row(filename, position, word, code)
            rows.append(row)
            owners[code].append(row)
    return rows, dict(owners)


def plan_moves(root: Path = ROOT) -> tuple[list[Row], tuple[Move, ...]]:
    rows, owners = load_rows(root)
    dictionary_dir = root / "dicts" / "eosphoros"
    options = load_character_code_options(
        dictionary_dir / "eosphoros.danzi.dict.yaml"
    )
    priority = {name: index for index, name in enumerate(LOCAL_WORD_DICTIONARIES)}
    occupied = set(owners)
    moves: list[Move] = []

    # Larger collision groups are handled first. The order is otherwise stable
    # so two platforms produce byte-identical rewrites.
    for code, shared_rows in sorted(
        owners.items(), key=lambda item: (-len(item[1]), item[0])
    ):
        if len(shared_rows) < 2:
            continue
        ordered = sorted(
            shared_rows,
            key=lambda row: (priority[row.filename], row.position),
        )
        # Keep the highest-priority row on the original short code. Consider
        # lower-priority rows from lowest priority upward for free suffixes.
        for row in reversed(ordered[1:]):
            if row.filename not in TARGET_NAMES:
                continue
            base_length = 3 if len(row.word) == 3 else 4
            if len(row.code) < base_length:
                continue
            candidates = sorted(
                (
                    candidate
                    for candidate in valid_word_codes(row.word, options)
                    if candidate.startswith(row.code[:base_length])
                    and len(candidate) > len(row.code)
                ),
                key=lambda candidate: (len(candidate), candidate),
            )
            new_code = next(
                (candidate for candidate in candidates if candidate not in occupied),
                None,
            )
            if new_code is None:
                continue
            occupied.add(new_code)
            moves.append(Move(row, new_code))
    return rows, tuple(moves)


def collision_metrics(rows: list[Row], moves: tuple[Move, ...]) -> tuple[int, int]:
    counts = Counter(row.code for row in rows)
    before = collision_row_count(dict(counts))
    for move in moves:
        counts[move.row.code] -= 1
        counts[move.new_code] += 1
    return before, collision_row_count(dict(counts))


def rewrite_target(path: Path, moves: dict[int, Move]) -> None:
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
                move = moves.get(position)
                if move is not None:
                    if (fields[0], fields[1]) != (move.row.word, move.row.code):
                        raise ValueError(
                            f"{path}:{position}: row changed while planning moves"
                        )
                    fields[1] = move.new_code
                    line = "\t".join(fields)
                position += 1
        output.append(line)
    path.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rows, moves = plan_moves(ROOT)
    before, after = collision_metrics(rows, moves)
    by_file = Counter(move.row.filename for move in moves)
    details = ", ".join(f"{name}={count}" for name, count in sorted(by_file.items()))
    print(
        f"Local collisions: {before}/{len(rows)} ({before / len(rows):.6%}); "
        f"planned: {after}/{len(rows)} ({after / len(rows):.6%}); "
        f"moves={len(moves)}" + (f" ({details})" if details else "")
    )

    if args.check:
        return 1 if moves else 0

    grouped: dict[str, dict[int, Move]] = defaultdict(dict)
    for move in moves:
        grouped[move.row.filename][move.row.position] = move
    for filename, file_moves in grouped.items():
        rewrite_target(DICT_DIR / filename, file_moves)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
