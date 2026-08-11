#!/usr/bin/env python3
"""Build native Eosphoros themes for Android and iOS input methods."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "mobile_themes"
PALETTES = OUTPUT / "palettes.yaml"
ZIP_TIME = (1980, 1, 1, 0, 0, 0)
COLOR_RE = re.compile(r"(?P<prefix>#?)(?P<rgb>[0-9A-Fa-f]{6})(?P<alpha>[0-9A-Fa-f]{2})?")


def load_config() -> dict[str, Any]:
    return yaml.safe_load(PALETTES.read_text(encoding="utf-8"))


def argb_int(color: str) -> int:
    value = color.removeprefix("#")
    if len(value) == 6:
        value = "FF" + value
    elif len(value) == 8:
        value = value[6:8] + value[:6]
    number = int(value, 16)
    return number - (1 << 32) if number >= (1 << 31) else number


def zip_bytes(files: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name.replace("\\", "/"), ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def write_if_changed(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)


def fcitx_theme(theme: dict[str, Any]) -> dict[str, Any]:
    color = lambda key: argb_int(theme[key])
    return {
        "name": f"{theme['name']}／{theme['english_name']}",
        "isDark": bool(theme["dark"]),
        "backgroundImage": None,
        "backgroundColor": color("background"),
        "barColor": color("bar"),
        "keyboardColor": color("keyboard"),
        "keyBackgroundColor": color("key"),
        "keyTextColor": color("text"),
        "candidateTextColor": color("text"),
        "candidateLabelColor": color("secondary"),
        "candidateCommentColor": color("secondary"),
        "altKeyBackgroundColor": color("alternative"),
        "altKeyTextColor": color("text"),
        "accentKeyBackgroundColor": color("accent"),
        "accentKeyTextColor": color("accent_text"),
        "keyPressHighlightColor": color("pressed"),
        "keyShadowColor": color("shadow"),
        "popupBackgroundColor": color("key"),
        "popupTextColor": color("text"),
        "spaceBarColor": color("key"),
        "dividerColor": color("divider"),
        "clipboardEntryColor": color("key"),
        "genericActiveBackgroundColor": color("accent"),
        "genericActiveForegroundColor": color("accent_text"),
        "version": "2.1",
    }


def build_fcitx(config: dict[str, Any]) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for theme_id, theme in config["themes"].items():
        payload = json.dumps(
            fcitx_theme(theme), ensure_ascii=False, indent=2
        ).encode("utf-8") + b"\n"
        result[f"eosphoros-{theme_id}.zip"] = zip_bytes(
            {f"eosphoros-{theme_id}.json": payload}
        )
    return result


def trime_color_scheme(theme: dict[str, Any]) -> dict[str, str]:
    color = lambda key: "0x" + theme[key].removeprefix("#").lower()
    return {
        "name": f"{theme['name']}／{theme['english_name']}",
        "author": "eosphoros-keytao",
        "back_color": color("bar"),
        "border_color": color("divider"),
        "candidate_separator_color": color("divider"),
        "candidate_text_color": color("text"),
        "comment_text_color": color("secondary"),
        "hilited_back_color": color("background"),
        "hilited_candidate_back_color": color("accent"),
        "hilited_candidate_text_color": color("accent_text"),
        "hilited_comment_text_color": color("accent_text"),
        "hilited_key_back_color": color("pressed"),
        "hilited_key_symbol_color": color("text"),
        "hilited_key_text_color": color("text"),
        "hilited_text_color": color("text"),
        "key_back_color": color("key"),
        "key_border_color": color("divider"),
        "key_symbol_color": color("secondary"),
        "key_text_color": color("text"),
        "keyboard_back_color": color("keyboard"),
        "label_color": color("secondary"),
        "off_key_back_color": color("alternative"),
        "off_key_text_color": color("text"),
        "on_key_back_color": color("accent"),
        "on_key_text_color": color("accent_text"),
        "preview_back_color": color("key"),
        "preview_text_color": color("text"),
        "shadow_color": color("shadow"),
        "text_color": color("text"),
        "text_back_color": color("background"),
    }


def build_trime(config: dict[str, Any]) -> bytes:
    document: dict[str, Any] = {
        "config_version": "3.0",
        "__include": "trime:/",
        "name": "晨星键道／Eosphoros KeyTao",
        "author": "eosphoros-keytao",
        "style": {
            "__include": "trime:/style",
            "color_scheme": "eosphoros_dawn",
            "color_scheme_dark": "eosphoros_night",
        },
        "preset_color_schemes": {
            "__include": "trime:/preset_color_schemes",
            **{
                f"eosphoros_{theme_id}": trime_color_scheme(theme)
                for theme_id, theme in config["themes"].items()
            },
        },
    }
    header = (
        "# 晨星键道 Trime 主题；继承 Trime 3.0 内置默认键盘，只覆盖配色。\n"
        "# SPDX-License-Identifier: MIT\n"
    )
    return (header + yaml.safe_dump(document, allow_unicode=True, sort_keys=False)).encode(
        "utf-8"
    )


def preview_png(theme: dict[str, Any]) -> bytes:
    image = Image.new("RGB", (900, 520), theme["keyboard"])
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=30)
    small = ImageFont.load_default(size=19)
    draw.rectangle((0, 0, 900, 92), fill=theme["bar"])
    draw.text((34, 24), theme["english_name"], fill=theme["text"], font=font)
    labels = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    for row, labels_in_row in enumerate(labels):
        width = 76
        offset = (900 - len(labels_in_row) * width) // 2
        y = 125 + row * 92
        for column, label in enumerate(labels_in_row):
            x = offset + column * width
            draw.rounded_rectangle(
                (x + 4, y + 4, x + width - 4, y + 78),
                radius=10,
                fill=theme["key"],
                outline=theme["divider"],
                width=1,
            )
            draw.text((x + 28, y + 26), label, fill=theme["text"], font=small)
    draw.rounded_rectangle((210, 416, 690, 492), radius=10, fill=theme["accent"])
    draw.text((392, 438), "RIME", fill=theme["accent_text"], font=small)
    buffer = io.BytesIO()
    image.save(buffer, "PNG", optimize=True)
    return buffer.getvalue()


def recolor_text(text: str, theme: dict[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        rgb = match.group("rgb")
        alpha = match.group("alpha") or ""
        red, green, blue = (int(rgb[index:index + 2], 16) for index in (0, 2, 4))
        luminance = (red * 299 + green * 587 + blue * 114) / 1000
        if luminance < 64:
            replacement = theme["text"]
        elif luminance < 145:
            replacement = theme["secondary"]
        elif luminance < 220:
            replacement = theme["alternative"]
        else:
            replacement = theme["key"]
        return match.group("prefix") + replacement.removeprefix("#") + alpha

    output: list[str] = []
    for line in text.splitlines(keepends=True):
        if "color" in line.lower() or re.search(r"foreground|background", line, re.I):
            line = COLOR_RE.sub(replace, line)
        output.append(line)
    return "".join(output)


def theme_archive(source: Path, theme: dict[str, Any], license_text: bytes) -> bytes:
    files: dict[str, bytes] = {}
    for path in source.rglob("*"):
        if not path.is_file() or path.name == "demo.png":
            continue
        relative = path.relative_to(source).as_posix()
        if path.suffix.lower() in {".yaml", ".yml", ".jsonnet", ".libsonnet"}:
            value = recolor_text(path.read_text(encoding="utf-8"), theme)
            if relative == "config.yaml":
                data = yaml.safe_load(value)
                data["name"] = f"{theme['name']}／{theme['english_name']}"
                data["author"] = "eosphoros-keytao（布局基于 BlackCCCat MIT 模板）"
                value = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
            files[relative] = value.encode("utf-8")
        else:
            files[relative] = path.read_bytes()
    files["demo.png"] = preview_png(theme)
    files["Eosphoros-ATTRIBUTION.txt"] = (
        "配色与预览：eosphoros-keytao，MIT。\n"
        "键盘布局模板：BlackCCCat/ResourceforHamster，MIT。\n"
        "固定模板提交：6c2b8d9a3c7116f41b77c32a662a7685770a5914。\n"
        "https://github.com/BlackCCCat/ResourceforHamster\n"
    ).encode("utf-8")
    files["THIRD_PARTY-LICENSE-MIT.txt"] = license_text
    return zip_bytes(files)


def obtain_ios_template(config: dict[str, Any], cache: Path | None) -> Path:
    if cache is not None:
        return cache
    lock = config["ios_template"]
    archive = ROOT / ".tmp" / f"ResourceforHamster-{lock['commit']}.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    if not archive.exists():
        with urllib.request.urlopen(lock["archive"], timeout=120) as response:
            archive.write_bytes(response.read())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != lock["sha256"]:
        raise ValueError(f"iOS template SHA-256 mismatch: {digest}")
    extracted = archive.with_suffix("")
    marker = extracted / ".ready"
    if not marker.exists():
        extracted.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive) as source:
            source.extractall(extracted)
        marker.write_text(lock["commit"], encoding="ascii")
    roots = [path for path in extracted.iterdir() if path.is_dir()]
    if len(roots) != 1:
        raise ValueError("unexpected iOS template archive layout")
    return roots[0]


def build_ios(config: dict[str, Any], template: Path) -> tuple[dict[str, bytes], dict[str, bytes]]:
    yuanshu_source = template / "Skin_Keyboard" / "万象-元书" / "WanxiangSkin"
    hamster_source = template / "Skin_Keyboard" / "万象-仓" / "26键-万象"
    if not yuanshu_source.is_dir() or not hamster_source.is_dir():
        raise FileNotFoundError("locked iOS keyboard template is incomplete")
    license_text = (template / "LICENSE").read_bytes()
    yuanshu: dict[str, bytes] = {}
    hamster: dict[str, bytes] = {}
    for theme_id, theme in config["themes"].items():
        yuanshu[f"eosphoros-{theme_id}.cskin"] = theme_archive(
            yuanshu_source, theme, license_text
        )
        hamster[f"eosphoros-{theme_id}.hskin"] = theme_archive(
            hamster_source, theme, license_text
        )
    return yuanshu, hamster


def readme(title: str, instructions: str) -> bytes:
    return (
        f"{title}\n{'=' * len(title)}\n\n{instructions}\n\n"
        "包含晨星·黎明、晨星·夜色、晨星·极简三套主题。\n"
        "生成日期：2026-08-11；文本编码：UTF-8。\n"
    ).encode("utf-8")


def build_committed(config: dict[str, Any], destination: Path) -> None:
    fcitx = build_fcitx(config)
    for name, data in fcitx.items():
        write_if_changed(destination / "fcitx5-android" / name, data)
    write_if_changed(destination / "trime" / "eosphoros.trime.yaml", build_trime(config))


def check_committed(config: dict[str, Any]) -> bool:
    with tempfile.TemporaryDirectory() as temporary:
        expected = Path(temporary)
        build_committed(config, expected)
        expected_files = {
            path.relative_to(expected): path.read_bytes()
            for path in expected.rglob("*") if path.is_file()
        }
        actual_files = {
            path.relative_to(OUTPUT): path.read_bytes()
            for folder in (OUTPUT / "fcitx5-android", OUTPUT / "trime")
            if folder.exists()
            for path in folder.rglob("*") if path.is_file()
        }
        return expected_files == actual_files


def embed_ios_skins(config: dict[str, Any], destination: Path, template: Path) -> None:
    yuanshu, hamster = build_ios(config, template)
    targets = {
        "eosphoros-yuanshu.zip": (
            yuanshu,
            "元书输入法晨星皮肤",
            "方案文件可直接导入；skins/ 中的 .cskin 需在元书中逐个导入。",
        ),
        "eosphoros-hamster.zip": (
            hamster,
            "仓输入法晨星皮肤",
            "方案文件可直接导入；skins/ 中的 .hskin 需通过系统共享菜单逐个导入。",
        ),
    }
    for archive_name, (skins, title, instructions) in targets.items():
        archive_path = destination / archive_name
        if not archive_path.is_file():
            raise FileNotFoundError(
                f"platform archive is missing; run build_platform_packages.py first: {archive_path}"
            )
        with zipfile.ZipFile(archive_path) as archive:
            files = {name: archive.read(name) for name in archive.namelist()}
        files.update({f"skins/{name}": data for name, data in skins.items()})
        files["README-MOBILE-SKINS.txt"] = readme(title, instructions)
        write_if_changed(archive_path, zip_bytes(files))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--platform-dir",
        type=Path,
        help="embed generated iOS skins into existing Yuanshu and Hamster platform ZIPs",
    )
    parser.add_argument("--ios-template", type=Path)
    args = parser.parse_args()
    config = load_config()
    if args.check:
        if not check_committed(config):
            print("Mobile themes are stale; run tools/build_mobile_themes.py")
            return 1
        print("Mobile themes are current")
        return 0
    build_committed(config, OUTPUT)
    if args.platform_dir:
        template = obtain_ios_template(config, args.ios_template)
        embed_ios_skins(config, args.platform_dir, template)
        print(f"Embedded iOS skins in platform archives at {args.platform_dir}")
    else:
        print("Built committed Fcitx5 Android and Trime themes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
