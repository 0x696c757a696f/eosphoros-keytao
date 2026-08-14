#!/usr/bin/env python3
"""Prepare a minimal Rabbit bundle with Eosphoros runtime files and themes."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

import yaml

try:
    from tools.dictionary_profiles import (
        PROFILES,
        excluded_dictionaries,
        profiled_dictionary_index,
    )
except ModuleNotFoundError:
    from dictionary_profiles import PROFILES, excluded_dictionaries, profiled_dictionary_index


ROOT = Path(__file__).resolve().parents[1]
RABBIT_BASE_FILES = ("punctuation.yaml", "key_bindings.yaml", "symbols.yaml")
RABBIT_STYLE = {
    "color_scheme": "EosphorosLight",
    "color_scheme_dark": "EosphorosDark",
    # Rabbit passes this value directly to AutoHotkey/CreateFont.  Unlike
    # Weasel, it does not accept a comma-separated fallback chain.
    "font_face": "Microsoft YaHei UI",
    "label_font_face": "Microsoft YaHei UI",
    "comment_font_face": "Microsoft YaHei UI",
    "font_point": 16,
    "label_font_point": 15,
    "comment_font_point": 13,
}
RABBIT_LAYOUT = {
    "corner_radius": 8,
    "round_corner": 8,
    "margin_x": 8,
    "margin_y": 6,
    "min_width": 220,
}
MERGE_LAUNCHER = r"""@echo off
setlocal
set "RABBIT_ROOT=%~dp0"
copy /Y "%RABBIT_ROOT%Rime\dicts\eosphoros\eosphoros.zzc.dict.yaml" "%RABBIT_ROOT%Data\dicts\eosphoros\eosphoros.zzc.dict.yaml" >nul
set "eosphoros_zzc_root=%RABBIT_ROOT%Data"
set "eosphoros_zzc_state_dir=%RABBIT_ROOT%Rime\zzc_state"
"%RABBIT_ROOT%Data\zzc\Merge-ZZZC.exe"
if errorlevel 1 goto fail
copy /Y "%RABBIT_ROOT%Data\dicts\eosphoros\eosphoros.zzc.dict.yaml" "%RABBIT_ROOT%Rime\dicts\eosphoros\eosphoros.zzc.dict.yaml" >nul
echo ZZZC merge completed. Redeploy Rabbit to load the merged dictionary.
if not defined CI pause
exit /b 0
:fail
echo ZZZC merge failed.
if not defined CI pause
exit /b 1
"""
ROLLBACK_LAUNCHER = r"""@echo off
setlocal
set "RABBIT_ROOT=%~dp0"
"%RABBIT_ROOT%Data\zzc\Rollback-ZZZC.exe"
if errorlevel 1 goto fail
copy /Y "%RABBIT_ROOT%Data\dicts\eosphoros\eosphoros.zzc.dict.yaml" "%RABBIT_ROOT%Rime\dicts\eosphoros\eosphoros.zzc.dict.yaml" >nul
echo ZZZC rollback completed. Redeploy Rabbit to load the restored dictionary.
if not defined CI pause
exit /b 0
:fail
echo ZZZC rollback failed or was cancelled.
if not defined CI pause
exit /b 1
"""


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8-sig")) or {}


def load_weasel_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    config = yaml.safe_load(text) or {}
    scalar_config = yaml.load(text, Loader=yaml.BaseLoader) or {}
    # Keep hexadecimal colors, including leading alpha bytes, as written.
    config["preset_color_schemes"] = scalar_config.get("preset_color_schemes", {})
    return config


def build_rabbit_config(base: dict[str, Any], weasel: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    result["config_version"] = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    result["app_options"] = {**base.get("app_options", {}), **weasel.get("app_options", {})}

    style = dict(base.get("style", {}))
    style.update(RABBIT_STYLE)
    # Rabbit uses AutoHotkey v2 Format(), not Weasel's printf-style label format.
    style["label_format"] = "{:s}. "
    layout = dict(style.get("layout", {}))
    layout.update(RABBIT_LAYOUT)
    style["layout"] = layout
    result["style"] = style

    schemes: dict[str, Any] = {}
    for name, source_scheme in weasel.get("preset_color_schemes", {}).items():
        scheme = dict(source_scheme)
        # Weasel's native hexadecimal order is BGR/AABBGGRR. Rabbit can read it
        # correctly when the source format is declared explicitly.
        scheme.setdefault("color_format", "abgr")
        schemes[name] = scheme
    result["preset_color_schemes"] = schemes
    return result


def runtime_files(root: Path, profile: str = "full") -> list[Path]:
    files = [
        root / "default.yaml",
        root / "liangfen.schema.yaml",
        root / "pinyin_simp.schema.yaml",
        root / "eosphoros.ico",
        root / "eosphoros-ascii.ico",
    ]
    files.extend(path for path in root.glob("eosphoros*.yaml") if not path.name.endswith(".custom.yaml"))
    files.extend(root.glob("*.dict.yaml"))
    for folder in ("dicts/eosphoros", "lua/eosphoros", "opencc/eosphoros"):
        files.extend(path for path in (root / folder).rglob("*") if path.is_file())
    files.append(root / "zzc_state" / "char_parts.tsv")
    excluded = set(excluded_dictionaries(profile))
    return sorted(
        path
        for path in set(files)
        if path.relative_to(root).as_posix() not in excluded
    )


def prepare(rabbit_dir: Path, root: Path = ROOT, profile: str = "full") -> None:
    data_dir = rabbit_dir / "Data"
    user_dir = rabbit_dir / "Rime"
    required = [data_dir / name for name in (*RABBIT_BASE_FILES, "rabbit.yaml")]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("Rabbit base files missing: " + ", ".join(missing))

    base_files = {name: (data_dir / name).read_bytes() for name in RABBIT_BASE_FILES}
    rabbit_config = build_rabbit_config(
        load_yaml(data_dir / "rabbit.yaml"),
        load_weasel_yaml(root / "weasel.yaml"),
    )
    shutil.rmtree(data_dir)
    data_dir.mkdir()
    for name, content in base_files.items():
        (data_dir / name).write_bytes(content)
    (data_dir / "rabbit.yaml").write_text(
        yaml.safe_dump(rabbit_config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
        newline="\n",
    )

    for source in runtime_files(root, profile):
        if not source.is_file():
            raise FileNotFoundError(f"required runtime file missing: {source}")
        target = data_dir / source.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        if source == root / "eosphoros.extended.dict.yaml" and profile != "full":
            target.write_bytes(profiled_dictionary_index(source, profile))
        else:
            shutil.copy2(source, target)

    shutil.rmtree(user_dir, ignore_errors=True)
    (user_dir / "dicts" / "eosphoros").mkdir(parents=True)
    for name in (
        "default.custom.yaml",
        "eosphoros.custom.yaml",
        "rabbit.custom.yaml",
        "rabbit_themes.yaml",
        "eosphoros.ico",
        "eosphoros-ascii.ico",
    ):
        shutil.copy2(root / name, user_dir / name)
    shutil.copy2(
        root / "dicts" / "eosphoros" / "eosphoros.user.dict.yaml",
        user_dir / "dicts" / "eosphoros" / "eosphoros.user.dict.yaml",
    )
    zzc_tools = data_dir / "zzc"
    zzc_tools.mkdir()
    shutil.copy2(root / "zzc" / "Win_词库合并.exe", zzc_tools / "Merge-ZZZC.exe")
    shutil.copy2(root / "zzc" / "Win_撤回合并.exe", zzc_tools / "Rollback-ZZZC.exe")
    (rabbit_dir / "ZZZC-Merge.cmd").write_text(MERGE_LAUNCHER, encoding="utf-8", newline="\r\n")
    (rabbit_dir / "ZZZC-Rollback.cmd").write_text(
        ROLLBACK_LAUNCHER,
        encoding="utf-8",
        newline="\r\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rabbit-dir", type=Path, required=True)
    parser.add_argument("--profile", choices=PROFILES, default="full")
    args = parser.parse_args()
    prepare(args.rabbit_dir.resolve(), profile=args.profile)
    print(f"Prepared {args.profile} Rabbit bundle: {args.rabbit_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
