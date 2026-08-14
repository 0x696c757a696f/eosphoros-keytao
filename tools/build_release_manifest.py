from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tools.dictionary_profiles import PROFILES
    from tools.release_catalog import STANDALONE_ASSETS, profile_assets
except ModuleNotFoundError:
    from dictionary_profiles import PROFILES
    from release_catalog import STANDALONE_ASSETS, profile_assets


def expected_assets() -> tuple[str, ...]:
    assets = set(profile_assets())
    for profile in PROFILES:
        assets.add(f"dazhu-{profile}.txt")
    assets.update(STANDALONE_ASSETS)
    return tuple(sorted(assets))


def actual_assets(directory: Path) -> set[str]:
    return {
        path.name
        for pattern in ("eosphoros-*.zip", "dazhu-*.txt")
        for path in directory.glob(pattern)
        if path.is_file()
    }


def build_manifest(directory: Path, output: Path) -> tuple[str, ...]:
    expected = expected_assets()
    actual = actual_assets(directory)
    missing = sorted(set(expected) - actual)
    unexpected = sorted(actual - set(expected))
    problems = []
    if missing:
        problems.append("missing release assets: " + ", ".join(missing))
    if unexpected:
        problems.append("unexpected release assets: " + ", ".join(unexpected))
    if problems:
        raise RuntimeError("; ".join(problems))
    output.write_text("\n".join(expected) + "\n", encoding="utf-8", newline="\n")
    return expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("release-assets.txt"))
    args = parser.parse_args()
    build_manifest(args.directory, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
