#!/usr/bin/env python3
"""Build minimal generic and platform-specific eosphoros release archives."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

PACKAGE_EXTRAS: dict[str, tuple[str, ...]] = {
    "eosphoros-rime-cross-platform.zip": (),
    "eosphoros-weasel-windows.zip": (
        "weasel.yaml",
        "weasel.custom.yaml",
        "zzc/Win_词库合并.exe",
        "zzc/Win_撤回合并.exe",
        "zzc/Windows_词库合并.py",
        "zzc/Windows_撤回合并.py",
    ),
    "eosphoros-squirrel-macos.zip": (
        "squirrel.yaml",
        "squirrel.custom.yaml",
        "zzc/Mac_词库合并",
        "zzc/Mac_撤回合并",
    ),
    "eosphoros-fcitx5-macos.zip": (
        "fcitx5/macos/themes",
        "zzc/Fcitx5_macOS_词库合并.py",
        "zzc/Fcitx5_macOS_撤回合并.py",
    ),
    "eosphoros-fcitx5-linux.zip": (
        "fcitx5/linux/themes",
        "zzc/Fcitx5_Linux_词库合并.py",
        "zzc/Fcitx5_Linux_撤回合并.py",
    ),
    "eosphoros-trime-android.zip": (
        "mobile_themes/trime",
    ),
    "eosphoros-fcitx5-android.zip": (
        "mobile_themes/fcitx5-android",
    ),
    "eosphoros-yuanshu-ios.zip": (
        "Hamster.yaml",
        "exclude_iCloud_rime_files.txt",
        "include_iCloud_rime_files.txt",
        "include_keyboard_rime_files.txt",
        "zzc/iOS_词库合并.py",
        "zzc/iOS快捷指令合并说明.md",
        "zzc/a-Shell快捷指令合并说明.md",
    ),
    "eosphoros-hamster-ios.zip": (
        "Hamster.yaml",
        "exclude_iCloud_rime_files.txt",
        "include_iCloud_rime_files.txt",
        "include_keyboard_rime_files.txt",
        "zzc/iOS_词库合并.py",
        "zzc/iOS快捷指令合并说明.md",
        "zzc/a-Shell快捷指令合并说明.md",
    ),
}

PACKAGE_PREFIX_RENAMES: dict[str, tuple[tuple[str, str], ...]] = {
    "eosphoros-trime-android.zip": (
        ("mobile_themes/trime/", ""),
    ),
    "eosphoros-fcitx5-android.zip": (
        ("mobile_themes/fcitx5-android/", "themes/"),
    ),
}


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


def package_files(root: Path) -> dict[str, list[Path]]:
    common = common_runtime_files(root)
    packages: dict[str, list[Path]] = {}
    for archive_name, extras in PACKAGE_EXTRAS.items():
        extra_files: list[Path] = []
        for relative in extras:
            path = root / relative
            if path.is_dir():
                extra_files.extend(_files_below(root, relative))
            else:
                extra_files.append(path)
        files = common + extra_files
        packages[archive_name] = _validate_files(root, files)
    return packages


def _archive_name(root: Path, archive_name: str, path: Path) -> str:
    relative = path.relative_to(root).as_posix()
    for source, target in PACKAGE_PREFIX_RENAMES.get(archive_name, ()):
        if relative == source or relative.startswith(source):
            return target + relative[len(source):]
    return relative


def _write_zip(
    root: Path, destination: Path, archive_name: str, files: list[Path]
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path in files:
            relative = _archive_name(root, archive_name, path)
            info = zipfile.ZipInfo(relative, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)


def build_packages(root: Path = ROOT, output_dir: Path = ROOT) -> list[Path]:
    archives = []
    for archive_name, files in package_files(root).items():
        destination = output_dir / archive_name
        _write_zip(root, destination, archive_name, files)
        archives.append(destination)
    return archives


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate package manifests without writing archives",
    )
    args = parser.parse_args()

    if args.check:
        packages = package_files(ROOT)
        for name, files in packages.items():
            print(f"{name}: {len(files)} files")
        return 0

    for archive in build_packages(ROOT, args.output_dir.resolve()):
        print(archive)
    return 0


if __name__ == "__main__":
    sys.exit(main())
