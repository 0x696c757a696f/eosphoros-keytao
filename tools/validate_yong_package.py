#!/usr/bin/env python3
"""Validate file references in a generated Yong portable package."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path, PurePosixPath


SINGLE_PATH_KEYS = {
    "arg",
    "config",
    "crab",
    "history",
    "key_desc",
    "menu",
    "overlay",
    "redirect",
    "skin",
}

ANDROID_SKIN_REQUIRED = {"keyboard.html", "keyboard.css"}


def decode_config(data: bytes) -> str:
    """Decode the two encodings supported by maintained Yong configurations."""
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    raise ValueError("yong.ini is neither UTF-8 nor GB18030")


def iter_references(config: str) -> list[tuple[int, str, str]]:
    references: list[tuple[int, str, str]] = []
    section = ""
    for line_number, raw_line in enumerate(config.splitlines(), start=1):
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            continue
        if not line or line.startswith(("#", ";")) or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if not value or value.upper() == "NONE":
            continue
        # `crab` is a table path in [IM], but a hotkey action in [key].
        if key == "crab" and section != "IM":
            continue
        if key == "dicts":
            values = value.split()
        elif key in {"assist", "quick"}:
            parts = value.split(maxsplit=1)
            values = parts[1:]  # The first token is the guide key.
        elif key in SINGLE_PATH_KEYS:
            values = [value]
        else:
            continue
        references.extend((line_number, key, item.strip()) for item in values)
    return references


def validate_package(package_root: Path) -> list[str]:
    package_root = package_root.resolve()
    config_path = package_root / ".yong" / "yong.ini"
    if not config_path.is_file():
        return ["missing .yong/yong.ini"]

    config = decode_config(config_path.read_bytes())
    errors: list[str] = []
    for line_number, key, raw_reference in iter_references(config):
        reference = raw_reference.replace("\\", "/").rstrip("/")
        path = PurePosixPath(reference)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"line {line_number}: unsafe {key} path: {raw_reference}")
            continue
        relative_target = Path(*path.parts)
        targets = (package_root / ".yong" / relative_target, package_root / relative_target)
        if not any(target.exists() for target in targets):
            errors.append(f"line {line_number}: missing {key} target: {raw_reference}")

    android_dir = package_root / ".yong" / "android"
    if android_dir.is_dir():
        for skin_path in sorted(android_dir.glob("*.zip")):
            if not zipfile.is_zipfile(skin_path):
                errors.append(f"invalid Android skin ZIP: {skin_path.name}")
                continue
            with zipfile.ZipFile(skin_path) as skin:
                files: set[str] = set()
                unsafe = False
                for member in skin.infolist():
                    path = PurePosixPath(member.filename.replace("\\", "/"))
                    if path.is_absolute() or ".." in path.parts:
                        errors.append(
                            f"unsafe Android skin member in {skin_path.name}: "
                            f"{member.filename}"
                        )
                        unsafe = True
                        break
                    if not member.is_dir():
                        files.add(path.as_posix())
                if unsafe:
                    continue
                missing = sorted(ANDROID_SKIN_REQUIRED - files)
                if missing:
                    errors.append(
                        f"Android skin {skin_path.name} is missing: {', '.join(missing)}"
                    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root", type=Path, help="directory containing .yong")
    args = parser.parse_args()

    errors = validate_package(args.package_root)
    if errors:
        print("Yong package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Yong package references are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
