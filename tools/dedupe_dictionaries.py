#!/usr/bin/env python3
"""Remove exact duplicate rows from Rime dictionaries."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def dedupe(path: Path, seen: set[bytes] | None = None) -> int:
    output: list[bytes] = []
    seen = seen if seen is not None else set()
    in_data = False
    removed = 0
    for line in path.read_bytes().splitlines(keepends=True):
        content = line.rstrip(b"\r\n")
        if not in_data:
            output.append(line)
            if content.strip() == b"...":
                in_data = True
            continue
        if not content.strip() or content.lstrip().startswith(b"#") or b"\t" not in content:
            output.append(line)
            continue
        if content in seen:
            removed += 1
            continue
        seen.add(content)
        output.append(line)
    if removed:
        path.write_bytes(b"".join(output))
    return removed


def main() -> int:
    total = 0
    dictionary_dir = ROOT / "dicts" / "eosphoros"
    imported = [
        ROOT / f"{line.strip().removeprefix('- ')}.dict.yaml"
        for line in (ROOT / "eosphoros.extended.dict.yaml")
        .read_text(encoding="utf-8-sig")
        .splitlines()
        if line.strip().startswith("- dicts/eosphoros/")
    ]
    imported_set = set(imported)
    paths = [(path, True) for path in imported]
    paths.extend(
        (path, False)
        for path in sorted(dictionary_dir.glob("*.dict.yaml"))
        if path not in imported_set
    )
    shared_seen: set[bytes] = set()
    for path, is_imported in paths:
        removed = dedupe(path, shared_seen if is_imported else None)
        if removed:
            print(f"{path.name}: removed {removed} exact duplicate row(s)")
            total += removed
    print(f"Removed {total} exact duplicate row(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
