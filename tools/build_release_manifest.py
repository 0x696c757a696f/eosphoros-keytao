from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tools.build_platform_packages import PACKAGE_EXTRAS
    from tools.dictionary_profiles import PROFILES, archive_name
except ModuleNotFoundError:
    from build_platform_packages import PACKAGE_EXTRAS
    from dictionary_profiles import PROFILES, archive_name


FCITX5_PLATFORMS = ("macos", "android", "linux")
YONG_PLATFORMS = ("windows", "android", "linux")


def expected_assets() -> tuple[str, ...]:
    assets = set(PACKAGE_EXTRAS)
    for platform in FCITX5_PLATFORMS:
        for profile in PROFILES:
            assets.add(archive_name(f"eosphoros-fcitx5-{platform}.zip", profile))
    for profile in PROFILES:
        assets.add(archive_name("eosphoros-rabbit-windows-rime.zip", profile))
        assets.add(f"dazhu-{profile}.txt")
    for platform in YONG_PLATFORMS:
        for profile in PROFILES:
            assets.add(archive_name(f"eosphoros-yong-{platform}.zip", profile))
    assets.add("eosphoros-yong-desktop-skins.zip")
    assets.add("eosphoros-fcitx5-android-themes.zip")
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
