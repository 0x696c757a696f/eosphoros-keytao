#!/usr/bin/env python3
"""Generate platform/profile Plum recipes from the release profile rules."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tools.dictionary_profiles import (
        PROFILES,
        excluded_dictionaries,
        profile_dictionary_name,
        profiled_dictionary_index,
    )
except ModuleNotFoundError:
    from dictionary_profiles import (
        PROFILES,
        excluded_dictionaries,
        profile_dictionary_name,
        profiled_dictionary_index,
    )


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "recipe" / "eosphoros"

COMMON_FILES = (
    "default.yaml",
    "liangfen*.yaml",
    "pinyin_simp*.yaml",
    "eosphoros*.ico",
    "eosphoros.cx.dict.yaml",
    "eosphoros.gbk.dict.yaml",
    "liangfen.dict.yaml",
    "pinyin_simp.dict.yaml",
    "eosphoros.*.schema.yaml",
    "eosphoros.schema.yaml",
    "eosphoros.symbols.yaml",
    "eosphoros.custom.yaml",
    "lua/eosphoros/*.lua",
    "lua/eosphoros/*/*.lua",
    "opencc/eosphoros/*.lua",
    "zzc_state/char_parts.tsv",
    "zzc/README.md",
    "zzc/自造词使用教程.md",
    "zzc/自造词使用教程.png",
    "zzc/eosphoros_词库合并.py",
    "zzc/eosphoros_撤回合并.py",
)

PLATFORMS: dict[str, tuple[str, tuple[str, ...]]] = {
    "rime": ("通用 Rime", ()),
    "weasel-windows-rime": (
        "Windows 小狼毫",
        (
            "weasel.yaml",
            "zzc/Win_词库合并.exe",
            "zzc/Win_撤回合并.exe",
            "zzc/Windows_词库合并.py",
            "zzc/Windows_撤回合并.py",
        ),
    ),
    "rabbit-windows-rime": (
        "Windows 玉兔毫",
        (
            "rabbit_themes.yaml",
            "zzc/Win_词库合并.exe",
            "zzc/Win_撤回合并.exe",
            "zzc/Windows_词库合并.py",
            "zzc/Windows_撤回合并.py",
        ),
    ),
    "squirrel-macos-rime": (
        "macOS 鼠须管",
        ("squirrel.yaml", "zzc/Mac_词库合并", "zzc/Mac_撤回合并"),
    ),
    "fcitx5-macos-rime": ("macOS Fcitx5 + Rime", ()),
    "trime-android": ("Android 同文", ()),
    "fcitx5-android-rime": ("Android Fcitx5 + Rime", ()),
    "yuanshu-ios-rime": (
        "iOS 元书输入法",
        (
            "Hamster.yaml",
            "exclude_iCloud_rime_files.txt",
            "include_iCloud_rime_files.txt",
            "include_keyboard_rime_files.txt",
            "zzc/iOS_词库合并.py",
            "zzc/iOS快捷指令合并说明.md",
            "zzc/a-Shell快捷指令合并说明.md",
        ),
    ),
    "hamster-ios-rime": (
        "iOS 仓输入法",
        (
            "Hamster.yaml",
            "exclude_iCloud_rime_files.txt",
            "include_iCloud_rime_files.txt",
            "include_keyboard_rime_files.txt",
            "zzc/iOS_词库合并.py",
            "zzc/iOS快捷指令合并说明.md",
            "zzc/a-Shell快捷指令合并说明.md",
        ),
    ),
    "fcitx5-linux-rime": ("Linux Fcitx5 + Rime", ()),
}


def dictionary_files(profile: str, root: Path = ROOT) -> list[str]:
    excluded = set(excluded_dictionaries(profile))
    return [
        path.relative_to(root).as_posix()
        for path in sorted((root / "dicts" / "eosphoros").glob("*.dict.yaml"))
        if path.relative_to(root).as_posix() not in excluded
    ]


def render_profile_index(profile: str, root: Path = ROOT) -> str:
    name = profile_dictionary_name(profile)
    text = profiled_dictionary_index(root / "eosphoros.full.dict.yaml", profile).decode()
    return text.replace("name: eosphoros.full", f"name: {name}", 1)


def render_recipe(platform: str, profile: str, root: Path = ROOT) -> str:
    label, extras = PLATFORMS[platform]
    rx = f"recipe/eosphoros/{platform}-{profile}"
    files = (
        *COMMON_FILES,
        f"{profile_dictionary_name(profile)}.dict.yaml",
        *dictionary_files(profile, root),
        *extras,
    )
    lines = [
        "# encoding: utf-8",
        "---",
        "recipe:",
        f"  Rx: {rx}",
        "  description: >-",
        f"    为 {label} 安装或更新晨星键道 {profile.capitalize()} 词库档位。",
        "install_files: >-",
        *(f"  {item}" for item in files),
        "patch_files:",
        "  default.custom.yaml:",
        "    - patch/+:",
        "        schema_list/+/+:",
        "          - schema: eosphoros",
        "  eosphoros.custom.yaml:",
        "    - patch/+:",
        f"        translator/dictionary: {profile_dictionary_name(profile)}",
    ]
    if platform == "rabbit-windows-rime":
        lines.extend(
            (
                "  rabbit.custom.yaml:",
                "    - patch/+:",
                "        style/color_scheme: EosphorosLight",
                "        style/color_scheme_dark: EosphorosDark",
                '        style/font_face: "Microsoft YaHei UI"',
                '        style/preedit_font_face: "Microsoft YaHei UI"',
                '        style/label_font_face: "Microsoft YaHei UI"',
                '        style/comment_font_face: "Microsoft YaHei UI"',
                "        style/font_point: 16",
                "        style/label_font_point: 15",
                "        style/comment_font_point: 13",
                '        style/label_format: "{:s}. "',
                "        style/layout/margin_x: 8",
                "        style/layout/margin_y: 6",
                "        style/layout/min_width: 220",
                "        preset_color_schemes/EosphorosLight:",
                "          __include: rabbit_themes:/preset_color_schemes/EosphorosLight",
                "        preset_color_schemes/EosphorosDark:",
                "          __include: rabbit_themes:/preset_color_schemes/EosphorosDark",
                "        preset_color_schemes/EosphorosMono:",
                "          __include: rabbit_themes:/preset_color_schemes/EosphorosMono",
            )
        )
    return "\n".join(lines) + "\n"


def expected_recipes(root: Path = ROOT) -> dict[Path, str]:
    return {
        root / "recipe" / "eosphoros" / f"{platform}-{profile}.recipe.yaml": render_recipe(
            platform, profile, root
        )
        for platform in PLATFORMS
        for profile in PROFILES
    }


def expected_profile_indexes(root: Path = ROOT) -> dict[Path, str]:
    return {
        root / f"{profile_dictionary_name(profile)}.dict.yaml": render_profile_index(
            profile, root
        )
        for profile in PROFILES
        if profile != "full"
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = {**expected_recipes(ROOT), **expected_profile_indexes(ROOT)}
    stale = [path for path, text in expected.items() if not path.is_file() or path.read_text(encoding="utf-8-sig") != text]
    unexpected = sorted(OUTPUT_DIR.glob("*.recipe.yaml")) if OUTPUT_DIR.is_dir() else []
    unexpected = [path for path in unexpected if path not in expected]
    if args.check:
        for path in (*stale, *unexpected):
            print(f"stale Plum recipe: {path.relative_to(ROOT).as_posix()}")
        return 1 if stale or unexpected else 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for path, text in expected.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    for path in unexpected:
        path.unlink()
    print(
        f"Generated {len(expected_recipes(ROOT))} Plum recipes and "
        f"{len(expected_profile_indexes(ROOT))} derived profile indexes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
