#!/usr/bin/env python3
"""Build minimal generic and platform-specific eosphoros release archives."""

from __future__ import annotations

import argparse
import os
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from tools.dictionary_profiles import (
        LITE_EXCLUDED_DICTIONARIES,
        PROFILES,
        STANDARD_EXCLUDED_DICTIONARIES,
        archive_name,
        excluded_dictionaries,
        profiled_dictionary_index,
    )
except ModuleNotFoundError:
    from dictionary_profiles import (
        LITE_EXCLUDED_DICTIONARIES,
        PROFILES,
        STANDARD_EXCLUDED_DICTIONARIES,
        archive_name,
        excluded_dictionaries,
        profiled_dictionary_index,
    )


ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
DEFAULT_ZIP_COMPRESSLEVEL = 6

PACKAGE_BASE_EXTRAS: dict[str, tuple[str, ...]] = {
    "eosphoros-rime.zip": (),
    "eosphoros-weasel-windows-rime.zip": (
        "weasel.yaml",
        "weasel.custom.yaml",
        "zzc/Win_词库合并.exe",
        "zzc/Win_撤回合并.exe",
        "zzc/Windows_词库合并.py",
        "zzc/Windows_撤回合并.py",
    ),
    "eosphoros-squirrel-macos-rime.zip": (
        "squirrel.yaml",
        "squirrel.custom.yaml",
        "zzc/Mac_词库合并",
        "zzc/Mac_撤回合并",
    ),
    "eosphoros-fcitx5-macos-rime.zip": (
        "fcitx5/macos/themes",
    ),
    "eosphoros-fcitx5-linux-rime.zip": (
        "fcitx5/linux/themes",
    ),
    "eosphoros-trime-android.zip": (
        "mobile_themes/trime",
    ),
    "eosphoros-fcitx5-android-rime.zip": (
        "mobile_themes/fcitx5-android",
    ),
    "eosphoros-yuanshu-ios-rime.zip": (
        "Hamster.yaml",
        "exclude_iCloud_rime_files.txt",
        "include_iCloud_rime_files.txt",
        "include_keyboard_rime_files.txt",
        "zzc/iOS_词库合并.py",
        "zzc/iOS快捷指令合并说明.md",
        "zzc/a-Shell快捷指令合并说明.md",
    ),
    "eosphoros-hamster-ios-rime.zip": (
        "Hamster.yaml",
        "exclude_iCloud_rime_files.txt",
        "include_iCloud_rime_files.txt",
        "include_keyboard_rime_files.txt",
        "zzc/iOS_词库合并.py",
        "zzc/iOS快捷指令合并说明.md",
        "zzc/a-Shell快捷指令合并说明.md",
    ),
}
PACKAGE_EXTRAS = {
    archive_name(base_name, profile): extras
    for base_name, extras in PACKAGE_BASE_EXTRAS.items()
    for profile in PROFILES
}

PACKAGE_BASE_PREFIX_RENAMES: dict[str, tuple[tuple[str, str], ...]] = {
    "eosphoros-trime-android.zip": (
        ("mobile_themes/trime/", ""),
    ),
    "eosphoros-fcitx5-macos-rime.zip": (
        ("fcitx5/macos/themes/", "themes/"),
    ),
    "eosphoros-fcitx5-linux-rime.zip": (
        ("fcitx5/linux/themes/", "themes/"),
    ),
    "eosphoros-fcitx5-android-rime.zip": (
        ("mobile_themes/fcitx5-android/", "themes/"),
    ),
}
PACKAGE_PREFIX_RENAMES = {
    archive_name(base_name, profile): renames
    for base_name, renames in PACKAGE_BASE_PREFIX_RENAMES.items()
    for profile in PROFILES
}


def package_profile(archive_name_value: str) -> str:
    return next(profile for profile in PROFILES if archive_name_value.endswith(f"-{profile}.zip"))


def _files_below(root: Path, relative: str) -> list[Path]:
    path = root / relative
    if not path.is_dir():
        raise FileNotFoundError(f"required directory is missing: {relative}")
    return sorted(item for item in path.rglob("*") if item.is_file())


def common_runtime_files(root: Path) -> list[Path]:
    files = [
        root / "default.yaml",
        root / "default.custom.yaml",
        root / "liangfen.schema.yaml",
        root / "pinyin_simp.schema.yaml",
        root / "eosphoros.ico",
        root / "eosphoros-ascii.ico",
        root / "zzc_state" / "char_parts.tsv",
        root / "README.md",
        root / "THIRD_PARTY.md",
        root / "LICENSE.md",
        root / "CONTRIBUTING.md",
        root / "VERSION",
        root / "zzc" / "README.md",
        root / "zzc" / "自造词使用教程.md",
        root / "zzc" / "自造词使用教程.png",
        root / "zzc" / "eosphoros_词库合并.py",
        root / "zzc" / "eosphoros_撤回合并.py",
    ]
    files.extend(sorted(root.glob("eosphoros*.yaml")))
    files.extend(sorted(root.glob("*.dict.yaml")))
    files.extend(_files_below(root, "dicts/eosphoros"))
    files.extend(_files_below(root, "lua/eosphoros"))
    files.extend(_files_below(root, "opencc/eosphoros"))
    files.extend(_files_below(root, "licenses"))
    return _validate_files(root, files)


def _validate_files(root: Path, files: list[Path]) -> list[Path]:
    missing = [path.relative_to(root).as_posix() for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError("required package files are missing: " + ", ".join(missing))
    return sorted(set(files), key=lambda path: path.relative_to(root).as_posix())


def package_files(
    root: Path,
    only_base_names: set[str] | None = None,
    excluded_base_names: set[str] | None = None,
) -> dict[str, list[Path]]:
    common = common_runtime_files(root)
    packages: dict[str, list[Path]] = {}
    only_base_names = only_base_names or set(PACKAGE_BASE_EXTRAS)
    excluded_base_names = excluded_base_names or set()
    selected_bases = only_base_names - excluded_base_names
    unknown = selected_bases - set(PACKAGE_BASE_EXTRAS)
    if unknown:
        raise ValueError("unknown package bases: " + ", ".join(sorted(unknown)))
    for base_name, extras in PACKAGE_BASE_EXTRAS.items():
        if base_name not in selected_bases:
            continue
        for profile in PROFILES:
            profile_archive_name = archive_name(base_name, profile)
            packages[profile_archive_name] = _package_files_for_archive(
                root, common, profile_archive_name, extras
            )
    return packages


def _package_files_for_archive(
    root: Path,
    common: list[Path],
    archive_name_value: str,
    extras: tuple[str, ...],
) -> list[Path]:
    extra_files: list[Path] = []
    for relative in extras:
        path = root / relative
        if path.is_dir():
            extra_files.extend(_files_below(root, relative))
        else:
            extra_files.append(path)
    excluded = set(excluded_dictionaries(package_profile(archive_name_value)))
    files = [
        path
        for path in common + extra_files
        if path.relative_to(root).as_posix() not in excluded
    ]
    return _validate_files(root, files)


def _archive_name(root: Path, archive_name: str, path: Path) -> str:
    relative = path.relative_to(root).as_posix()
    for source, target in PACKAGE_PREFIX_RENAMES.get(archive_name, ()):
        if relative == source or relative.startswith(source):
            return target + relative[len(source):]
    return relative


def _write_zip(
    root: Path,
    destination: Path,
    archive_name: str,
    files: list[Path],
    compresslevel: int = DEFAULT_ZIP_COMPRESSLEVEL,
    profile: str = "full",
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        destination,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=compresslevel,
    ) as archive:
        for path in files:
            relative = _archive_name(root, archive_name, path)
            info = zipfile.ZipInfo(relative, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            content = (
                profiled_dictionary_index(path, profile)
                if relative == "eosphoros.extended.dict.yaml" and profile != "full"
                else path.read_bytes()
            )
            archive.writestr(info, content, compresslevel=compresslevel)


def build_packages(
    root: Path = ROOT,
    output_dir: Path = ROOT,
    compresslevel: int = DEFAULT_ZIP_COMPRESSLEVEL,
    only_base_names: set[str] | None = None,
    excluded_base_names: set[str] | None = None,
) -> list[Path]:
    package_specs = list(
        package_files(root, only_base_names, excluded_base_names).items()
    )

    def build_package(spec: tuple[str, list[Path]]) -> Path:
        archive_name, files = spec
        destination = output_dir / archive_name
        _write_zip(
            root,
            destination,
            archive_name,
            files,
            compresslevel,
            package_profile(archive_name),
        )
        return destination

    workers = min(4, os.cpu_count() or 1, len(package_specs))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(build_package, package_specs))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate package manifests without writing archives",
    )
    parser.add_argument(
        "--only-base",
        action="append",
        choices=sorted(PACKAGE_BASE_EXTRAS),
        help="build only this profile-expanded base archive; repeat as needed",
    )
    parser.add_argument(
        "--exclude-base",
        action="append",
        default=[],
        choices=sorted(PACKAGE_BASE_EXTRAS),
        help="exclude this profile-expanded base archive; repeat as needed",
    )
    args = parser.parse_args()
    only_base_names = set(args.only_base) if args.only_base else None
    excluded_base_names = set(args.exclude_base)

    if args.check:
        packages = package_files(ROOT, only_base_names, excluded_base_names)
        for name, files in packages.items():
            print(f"{name}: {len(files)} files")
        return 0

    for archive in build_packages(
        ROOT,
        args.output_dir.resolve(),
        only_base_names=only_base_names,
        excluded_base_names=excluded_base_names,
    ):
        print(archive)
    return 0


if __name__ == "__main__":
    sys.exit(main())
