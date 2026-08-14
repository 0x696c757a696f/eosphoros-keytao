#!/usr/bin/env python3
"""Check or normalize tracked text files that Git attributes require as LF."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def requires_lf(metadata: bytes) -> bool:
    return (
        b"eol=lf" in metadata
        and b"i/-text" not in metadata
        and b"w/-text" not in metadata
    )


def tracked_lf_paths(root: Path = ROOT) -> tuple[Path, ...]:
    result = subprocess.run(
        ["git", "ls-files", "--eol", "-z"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
    )
    paths: list[Path] = []
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        metadata, relative = record.split(b"\t", 1)
        if requires_lf(metadata):
            paths.append(root / os.fsdecode(relative))
    return tuple(paths)


def non_lf_paths(root: Path = ROOT) -> list[Path]:
    return [
        path
        for path in tracked_lf_paths(root)
        if path.is_file() and b"\r" in path.read_bytes()
    ]


def normalize_lf(path: Path) -> bool:
    current = path.read_bytes()
    normalized = current.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if normalized == current:
        return False
    path.write_bytes(normalized)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    stale = non_lf_paths()
    if args.check:
        if stale:
            print("Tracked text files must use LF:")
            for path in stale:
                print(f"  {path.relative_to(ROOT).as_posix()}")
            print("Run: pixi run line-endings")
            return 1
        print("Tracked text files use LF")
        return 0

    for path in stale:
        normalize_lf(path)
    print(f"Normalized {len(stale)} tracked text files to LF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
