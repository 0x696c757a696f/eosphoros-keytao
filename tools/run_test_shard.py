#!/usr/bin/env python3
"""Run one deterministic shard of the repository unittest suite."""

from __future__ import annotations

import argparse
import hashlib
import unittest
from collections.abc import Iterator
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def iter_tests(suite: unittest.TestSuite) -> Iterator[unittest.TestCase]:
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from iter_tests(test)
        else:
            yield test


def shard_index(test_id: str, shard_count: int) -> int:
    digest = hashlib.sha256(test_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % shard_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--count", type=int, required=True)
    args = parser.parse_args()
    if args.count < 1 or not 0 <= args.index < args.count:
        parser.error("--index must be between zero and --count minus one")

    discovered = unittest.defaultTestLoader.discover(
        str(ROOT / "tests"), pattern="test_*.py"
    )
    selected = [
        test
        for test in iter_tests(discovered)
        if shard_index(test.id(), args.count) == args.index
    ]
    if not selected:
        parser.error(f"test shard {args.index + 1}/{args.count} is empty")

    print(f"Running {len(selected)} tests in shard {args.index + 1}/{args.count}")
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(selected))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
