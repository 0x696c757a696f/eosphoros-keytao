#!/usr/bin/env python3
"""Build the Yong table and grouped dazhu table from production sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from tools.build_fcitx5_table import MAX_CODE_LENGTH, ROOT, collect_entries
except ModuleNotFoundError:  # Direct execution: python tools/build_yong_table.py
    from build_fcitx5_table import MAX_CODE_LENGTH, ROOT, collect_entries


HEADER = f"""name=晨星键道
key=`abcedfghijklmnopqrstuvwxyz;\\
len={MAX_CODE_LENGTH}
wildcard=~
bihua=viuoa
nsort=1
code_e2=p11+p12+p21+p22+p13+p23
code_e3=p11+p21+p31+p13+p23+p33
code_a4=p11+p21+p31+n11+p13+p23+p33
[DATA]
"""


def build(root: Path, table_path: Path, dazhu_path: Path) -> int:
    entries = collect_entries(root)
    table_path.parent.mkdir(parents=True, exist_ok=True)
    dazhu_path.parent.mkdir(parents=True, exist_ok=True)

    with table_path.open("w", encoding="gb18030", newline="\n") as table:
        table.write(HEADER)
        for entry in entries:
            table.write(f"{entry.code} {entry.text}\n")

    # Yong's auxiliary dazhu table groups candidates with the same code. The
    # stable source order is the same priority used by Fcitx5 and Rime.
    entries.sort(key=lambda entry: (entry.code, entry.source_order))
    with dazhu_path.open("w", encoding="utf-8", newline="\n") as dazhu:
        previous = ""
        words: list[str] = []
        for entry in entries:
            if entry.code != previous and previous:
                dazhu.write(previous + "\t" + "\t".join(words) + "\n")
                words = []
            previous = entry.code
            words.append(entry.text)
        if previous:
            dazhu.write(previous + "\t" + "\t".join(words) + "\n")
    return len(entries)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", type=Path, required=True)
    parser.add_argument("--dazhu", type=Path, required=True)
    args = parser.parse_args()
    count = build(ROOT, args.table.resolve(), args.dazhu.resolve())
    print(f"Yong table: {count} unique rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
