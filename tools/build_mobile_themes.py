#!/usr/bin/env python3
"""Build native Eosphoros themes for Android and iOS input methods."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "mobile_themes"
PALETTES = OUTPUT / "palettes.yaml"
ZIP_TIME = (1980, 1, 1, 0, 0, 0)
HASH_COLOR_RE = re.compile(r"#(?P<rgb>[0-9A-Fa-f]{6})(?P<alpha>[0-9A-Fa-f]{2})?")
BARE_COLOR_RE = re.compile(
    r"(?m)(?P<head>:\s*['\"]?)(?P<rgb>[0-9A-Fa-f]{6})(?P<alpha>[0-9A-Fa-f]{2})?"
    r"(?P<tail>['\"]?\s*(?:#.*)?$)"
)


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


def validate_ios_skin_archive(archive: bytes, expected_root: str) -> None:
    """Reject packages that iOS skin importers cannot identify as one skin."""
    with zipfile.ZipFile(io.BytesIO(archive)) as skin:
        names = [name.rstrip("/") for name in skin.namelist() if name.rstrip("/")]
        roots = {name.split("/", 1)[0] for name in names}
        if roots != {expected_root}:
            raise ValueError("iOS skin archive must contain exactly one wrapper directory")
        required = {
            f"{expected_root}/config.yaml",
            f"{expected_root}/demo.png",
        }
        if not required.issubset(names):
            missing = ", ".join(sorted(required.difference(names)))
            raise ValueError(f"iOS skin archive is incomplete: {missing}")
        for appearance in ("dark", "light"):
            prefix = f"{expected_root}/{appearance}/"
            if not any(name.startswith(prefix) for name in names):
                raise ValueError(f"iOS skin archive has no {appearance} resources")


HAMSTER_COLOR_ROLES = {
    "light": {
        "000000": "text",
        "575757": "secondary",
        "FFFFFF": "key",
        "FAFFF5": "accent_text",
        "ABB0BA": "pressed",
        "D1D2D9": "keyboard",
        "E8EBEA": "keyboard",
        "0279FE": "accent",
        "1A73E9": "accent",
        "88898D": "divider",
        "89898B": "divider",
        "69686A": "divider",
        "696967": "divider",
        "797B7E": "shadow",
        "383838": "divider",
    },
    "dark": {
        "FFFFFF": "text",
        "E5E5EA": "secondary",
        "FAFFF5": "accent_text",
        "BBBBBB": "key",
        "555555": "alternative",
        "707070": "key",
        "ABB0BA": "pressed",
        "2C2C2C": "keyboard",
        "E8EBEA": "keyboard",
        "0279FE": "accent",
        "1A73E9": "accent",
        "000000": "accent_text",
        "6E6E6E": "divider",
        "797B7E": "shadow",
        "383838": "divider",
        "89898B": "divider",
        "88898D": "divider",
        "4C4C4C": "pressed",
        "1E1E1E": "divider",
        "1D1D1D": "divider",
        "2A2A2A": "accent_text",
    },
}


def recolor_template_text(
    text: str,
    theme: dict[str, Any],
    relative: str,
    *,
    semantic_hamster_colors: bool,
) -> str:
    """Apply names and, for Hskin, path-aware semantic palette colors."""
    appearance = "dark" if "/dark/" in f"/{relative}" else "light"
    role_map = HAMSTER_COLOR_ROLES[appearance]
    current_section = ""

    def replacement(match: re.Match[str]) -> str:
        rgb = match.group("rgb").upper()
        alpha = match.group("alpha") or ""
        role = role_map.get(rgb)
        if (
            semantic_hamster_colors
            and appearance == "light"
            and rgb == "FFFFFF"
            and "foreground" in current_section.lower()
        ):
            role = "accent_text"
        elif (
            semantic_hamster_colors
            and "foreground" in current_section.lower()
            and role not in {None, "text", "secondary", "accent", "accent_text"}
        ):
            role = "secondary"
        if not semantic_hamster_colors or role is None:
            return match.group("rgb") + alpha
        return theme[role].removeprefix("#") + alpha

    output: list[str] = []
    for line in text.splitlines(keepends=True):
        section_match = re.match(r"^([^\s#][^:]*):", line)
        if section_match:
            current_section = section_match.group(1)
        if semantic_hamster_colors and (
            "color" in line.lower()
            or re.search(r"foreground|background|颜色", line, re.I)
        ):
            line = HASH_COLOR_RE.sub(
                lambda match: "#" + replacement(match), line
            )
            line = BARE_COLOR_RE.sub(
                lambda match: match.group("head")
                + replacement(match)
                + match.group("tail"),
                line,
            )
        output.append(line)
    return (
        "".join(output)
        .replace("万象键盘", "晨星键道")
        .replace("26键-万象", "晨星键道")
        .replace("“万象”", "“晨星”")
        .replace("'万象'", "'晨星'")
        .replace("author: 'BlackCCCat'", "author: 'eosphoros-keytao'")
    )


WANXIANG_COLOR_KEYS = {
    "字母键背景颜色-普通": "key",
    "字母键背景颜色-高亮": "pressed",
    "功能键背景颜色-普通": "alternative",
    "功能键背景颜色-高亮": "pressed",
    "enter键背景(蓝色)": "accent",
    "气泡背景颜色": "key",
    "气泡边缘颜色": "divider",
    "气泡高亮颜色": "accent",
    "底边缘颜色-普通": "divider",
    "底边缘颜色-高亮": "divider",
    "长按选中字体颜色": "accent_text",
    "长按非选中字体颜色": "text",
    "长按选中背景颜色": "accent",
    "长按背景阴影颜色": "shadow",
    "长按背景颜色": "key",
    "候选字体选中字体颜色": "accent_text",
    "候选字体未选中字体颜色": "text",
    "选中候选背景颜色": "accent",
    "toolbar按键颜色": "text",
    "划动字符颜色": "secondary",
    "按下气泡文字颜色": "text",
    "collection前景颜色": "text",
    "列表选中字体颜色": "accent",
    "列表未选中字体颜色": "text",
    "符号键盘左侧collection背景颜色": "alternative",
    "符号键盘左侧collection背景下边缘颜色": "divider",
    "符号键盘右侧collection背景颜色": "key",
    "符号键盘右侧collection背景下边缘颜色": "divider",
    "按键边缘颜色": "divider",
    "按键前景颜色": "text",
    "键盘背景颜色": "keyboard",
}


def restyle_wanxiang_source(
    text: str,
    theme: dict[str, Any],
    relative: str,
    dark_theme: dict[str, Any] | None = None,
) -> str:
    """Apply the Eosphoros palette to Wanxiang's semantic Jsonnet tokens."""
    if relative.endswith("shared/styles/color.libsonnet"):
        active_theme: dict[str, Any] | None = None
        output: list[str] = []
        for line in text.splitlines(keepends=True):
            if line.startswith("local base_light = {"):
                active_theme = theme
            elif line.startswith("local base_dark = {"):
                active_theme = dark_theme or theme
            elif line.startswith("local ios26_"):
                active_theme = None
            if active_theme is not None:
                for token, palette_key in WANXIANG_COLOR_KEYS.items():
                    color = active_theme[palette_key].removeprefix("#")
                    line = re.sub(
                        rf"(^\s*'{re.escape(token)}':\s*)'[0-9A-Fa-f]{{6,8}}'",
                        rf"\1'{color}'",
                        line,
                    )
            output.append(line)
        text = "".join(output)
    elif relative.endswith("Custom.libsonnet"):
        text = text.replace("ios26_style: true", "ios26_style: false")
        text = text.replace("cornerRadius: 8,", "cornerRadius: 11,")
    return text


def recolor_template_preview(data: bytes, theme: dict[str, Any]) -> bytes:
    with Image.open(io.BytesIO(data)) as source:
        rgba = source.convert("RGBA")
        grayscale = ImageOps.grayscale(rgba.convert("RGB"))
        if theme["dark"]:
            darkest, middle, lightest = (
                theme["keyboard"],
                theme["key"],
                theme["text"],
            )
        else:
            darkest, middle, lightest = (
                theme["text"],
                theme["alternative"],
                theme["key"],
            )
        colored = ImageOps.colorize(
            grayscale,
            black=darkest,
            mid=middle,
            white=lightest,
        ).convert("RGBA")
        colored.putalpha(rgba.getchannel("A"))
        if colored.width / colored.height > 1.2:
            # The mature Yuanshu preview contains the upstream skin name and
            # author baked into pixels. Preserve the keyboard render but replace
            # those two label areas with neutral Eosphoros branding.
            draw = ImageDraw.Draw(colored)
            background = theme["key"]
            text_color = theme["secondary"]
            draw.rectangle(
                (int(colored.width * 0.76), 0, colored.width, int(colored.height * 0.82)),
                fill=background,
            )
            draw.rectangle(
                (0, int(colored.height * 0.84), int(colored.width * 0.66), colored.height),
                fill=background,
            )
            title_font = ImageFont.load_default(size=max(28, colored.width // 38))
            credit_font = ImageFont.load_default(size=max(18, colored.width // 65))
            draw.multiline_text(
                (int(colored.width * 0.80), int(colored.height * 0.18)),
                "EOSPHOROS\nKEYTAO",
                fill=text_color,
                font=title_font,
                spacing=12,
            )
            draw.text(
                (int(colored.width * 0.10), int(colored.height * 0.90)),
                "Eosphoros KeyTao",
                fill=text_color,
                font=credit_font,
            )
        output = io.BytesIO()
        colored.save(output, "PNG", optimize=True)
        return output.getvalue()


def adapt_mature_skin(
    source_archive: bytes,
    theme: dict[str, Any],
    root_name: str,
    license_text: bytes,
    source_repository: str,
    dark_theme: dict[str, Any] | None = None,
) -> bytes:
    """Rename and lightly restyle a known-working upstream skin archive."""
    files: dict[str, bytes] = {}
    with tempfile.TemporaryDirectory() as temporary:
        work = Path(temporary)
        skin_root = work / root_name
        with zipfile.ZipFile(io.BytesIO(source_archive)) as source:
            semantic_hamster_colors = not any(
                info.filename.endswith("/jsonnet/main.jsonnet")
                for info in source.infolist()
            )
            source_roots = {
                name.split("/", 1)[0]
                for name in source.namelist()
                if name.rstrip("/")
            }
            if len(source_roots) != 1:
                raise ValueError("upstream iOS skin must contain one wrapper directory")
            source_root = source_roots.pop()
            for info in source.infolist():
                if info.is_dir() or not info.filename.startswith(f"{source_root}/"):
                    continue
                relative = info.filename[len(source_root) + 1:]
                data = source.read(info)
                suffix = Path(relative).suffix.lower()
                file_theme = (
                    dark_theme
                    if dark_theme is not None and "/dark/" in f"/{relative}"
                    else theme
                )
                if relative == "demo.png":
                    data = recolor_template_preview(data, theme)
                elif suffix in {".yaml", ".yml", ".jsonnet", ".libsonnet", ".md", ".txt"}:
                    content = recolor_template_text(
                        data.decode("utf-8-sig"),
                        file_theme,
                        relative,
                        semantic_hamster_colors=semantic_hamster_colors,
                    )
                    content = restyle_wanxiang_source(
                        content,
                        theme,
                        relative,
                        dark_theme,
                    )
                    data = content.encode("utf-8")
                target = skin_root / Path(relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)

        main_jsonnet = skin_root / "jsonnet" / "main.jsonnet"
        if main_jsonnet.is_file():
            generated = work / "generated"
            (generated / "light").mkdir(parents=True)
            (generated / "dark").mkdir(parents=True)
            subprocess.run(
                ["jsonnet", "-S", "-m", str(generated), str(main_jsonnet)],
                cwd=skin_root,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            for generated_file in generated.rglob("*"):
                if generated_file.is_file():
                    relative = generated_file.relative_to(generated)
                    target = skin_root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(generated_file.read_bytes())

        config_path = skin_root / "config.yaml"
        config_value = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        config_value["name"] = f"{theme['name']}／{theme['english_name']}"
        config_value["author"] = "eosphoros-keytao"
        config_path.write_text(
            yaml.safe_dump(config_value, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
            newline="\n",
        )
        for path in skin_root.rglob("*"):
            if path.is_file():
                files[f"{root_name}/{path.relative_to(skin_root).as_posix()}"] = path.read_bytes()
    files[f"{root_name}/Eosphoros-ATTRIBUTION.txt"] = (
        "晨星名称、配色与轻量界面调整：eosphoros-keytao。\n"
        f"键盘布局与功能底稿：{source_repository}（MIT）。\n"
        f"https://github.com/{source_repository}\n"
    ).encode("utf-8")
    files.setdefault(
        f"{root_name}/README.md",
        (
            f"# {theme['name']}／{theme['english_name']}\n\n"
            "本皮肤保留成熟模板的功能、横竖屏与多设备布局，"
            "仅调整晨星名称、配色及少量视觉细节。\n\n"
            f"布局底稿：{source_repository}（MIT）。\n"
        ).encode("utf-8"),
    )
    files[f"{root_name}/THIRD_PARTY-LICENSE-MIT.txt"] = license_text
    result = zip_bytes(files)
    validate_ios_skin_archive(result, root_name)
    return result


def download_locked(url: str, sha256: str, destination: Path) -> bytes:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        with urllib.request.urlopen(url, timeout=120) as response:
            destination.write_bytes(response.read())
    data = destination.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != sha256.lower():
        raise ValueError(f"iOS template SHA-256 mismatch: {digest}")
    return data


def obtain_ios_templates(config: dict[str, Any]) -> tuple[bytes, bytes, bytes, bytes]:
    lock = config["ios_template"]
    cache = ROOT / ".tmp" / "ios-skin-templates"
    hamster_repository = download_locked(
        lock["hamster_archive"],
        lock["hamster_sha256"],
        cache / f"{lock['hamster_commit']}.zip",
    )
    yuanshu = download_locked(
        lock["yuanshu_release"],
        lock["yuanshu_sha256"],
        cache / "WanxiangSkin-2026.05.05.2.cskin",
    )
    with zipfile.ZipFile(io.BytesIO(hamster_repository)) as repository:
        hskin_name = next(
            name for name in repository.namelist()
            if name.endswith("/Skin_Keyboard/万象-仓/26键-万象.hskin")
        )
        license_name = next(
            name for name in repository.namelist() if name.endswith("/LICENSE")
        )
        hamster = repository.read(hskin_name)
        hamster_license = repository.read(license_name)
    return yuanshu, hamster, hamster_license, hamster_license


def build_ios(
    config: dict[str, Any],
    templates: tuple[bytes, bytes, bytes, bytes] | None = None,
) -> tuple[dict[str, bytes], dict[str, bytes]]:
    yuanshu_source, hamster_source, yuanshu_license, hamster_license = (
        templates or obtain_ios_templates(config)
    )
    yuanshu: dict[str, bytes] = {}
    hamster: dict[str, bytes] = {}
    dawn = dict(config["themes"]["dawn"])
    dawn.update(name="晨星键道", english_name="Eosphoros KeyTao")
    variants = (
        ("eosphoros", dawn, config["themes"]["night"]),
        ("eosphoros-mono", config["themes"]["mono"], None),
    )
    for root_name, theme, dark_theme in variants:
        yuanshu[f"{root_name}.cskin"] = adapt_mature_skin(
            yuanshu_source,
            theme,
            root_name,
            yuanshu_license,
            "BlackCCCat/ResourceforHamster",
            dark_theme,
        )
        hamster[f"{root_name}.hskin"] = adapt_mature_skin(
            hamster_source,
            theme,
            root_name,
            hamster_license,
            "BlackCCCat/ResourceforHamster",
            dark_theme,
        )
    return yuanshu, hamster


def readme(title: str, instructions: str) -> bytes:
    return (
        f"{title}\n{'=' * len(title)}\n\n{instructions}\n\n"
        "包含自动跟随系统明暗模式的晨星键道主题，以及晨星·极简主题。\n"
        "生成日期：2026-08-11；文本编码：UTF-8。\n"
    ).encode("utf-8")


def build_committed(config: dict[str, Any], destination: Path) -> None:
    fcitx = build_fcitx(config)
    for name, data in fcitx.items():
        write_if_changed(destination / "fcitx5-android" / name, data)
    write_if_changed(destination / "trime" / "eosphoros.trime.yaml", build_trime(config))


def artifact_contents(path: Path) -> bytes | dict[str, bytes]:
    """Compare generated ZIP payloads independently of the host zlib build."""
    if path.suffix.lower() != ".zip":
        return path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in sorted(archive.namelist())}


def check_committed(config: dict[str, Any]) -> bool:
    with tempfile.TemporaryDirectory() as temporary:
        expected = Path(temporary)
        build_committed(config, expected)
        expected_files = {
            path.relative_to(expected): artifact_contents(path)
            for path in expected.rglob("*") if path.is_file()
        }
        actual_files = {
            path.relative_to(OUTPUT): artifact_contents(path)
            for folder in (OUTPUT / "fcitx5-android", OUTPUT / "trime")
            if folder.exists()
            for path in folder.rglob("*") if path.is_file()
        }
        return expected_files == actual_files


def embed_ios_skins(config: dict[str, Any], destination: Path) -> None:
    yuanshu, hamster = build_ios(config)
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
        embed_ios_skins(config, args.platform_dir)
        print(f"Embedded iOS skins in platform archives at {args.platform_dir}")
    else:
        print("Built committed Fcitx5 Android and Trime themes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
