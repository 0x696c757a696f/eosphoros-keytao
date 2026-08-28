#!/usr/bin/env python3
"""Generate platform/profile Plum recipes from the release profile rules."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tools.dictionary_profiles import PROFILES, excluded_dictionaries
except ModuleNotFoundError:
    from dictionary_profiles import PROFILES, excluded_dictionaries


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "recipe" / "eosphoros"

COMMON_FILES = (
    "default.yaml",
    "liangfen*.yaml",
    "pinyin_simp*.yaml",
    "eosphoros*.ico",
    "eosphoros.*.dict.yaml",
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


def dictionary_imports(root: Path = ROOT) -> list[str]:
    return [
        line.strip().removeprefix("- ")
        for line in (root / "eosphoros.extended.dict.yaml")
        .read_text(encoding="utf-8-sig")
        .splitlines()
        if line.strip().startswith("- dicts/eosphoros/")
    ]


def dictionary_files(profile: str, root: Path = ROOT) -> list[str]:
    excluded = set(excluded_dictionaries(profile))
    return [
        path.relative_to(root).as_posix()
        for path in sorted((root / "dicts" / "eosphoros").glob("*.dict.yaml"))
        if path.relative_to(root).as_posix() not in excluded
    ]


def render_recipe(platform: str, profile: str, root: Path = ROOT) -> str:
    label, extras = PLATFORMS[platform]
    rx = f"recipe/eosphoros/{platform}-{profile}"
    files = (*COMMON_FILES, *dictionary_files(profile, root), *extras)
    excluded_imports = {
        path.removesuffix(".dict.yaml") for path in excluded_dictionaries(profile)
    }
    imports = [item for item in dictionary_imports(root) if item not in excluded_imports]
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
        "  eosphoros.extended.dict.yaml:",
        "    - patch/+:",
        "        import_tables:",
        *(f"          - {item}" for item in imports),
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected = expected_recipes(ROOT)
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
    print(f"Generated {len(expected)} Plum recipes in {OUTPUT_DIR.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
