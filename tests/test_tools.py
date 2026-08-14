from __future__ import annotations

import configparser
import fnmatch
import hashlib
import http.client
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import yaml


def dict_path(root: Path, name: str) -> Path:
    path = root / "dicts" / "eosphoros" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


class FetchOpenCCTests(unittest.TestCase):
    def test_extracts_only_opencc_data_into_namespaced_directory(self) -> None:
        from tools.fetch_opencc import extract_opencc_archive

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            archive = root / "opencc.zip"
            destination = root / "opencc" / "eosphoros"
            destination.mkdir(parents=True)
            (destination / "local.lua").write_text("return {}\n", encoding="utf-8")
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr("opencc/s2tg.json", "{}")
                bundle.writestr("opencc/STGCharacters.ocd2", b"ocd2")
                bundle.writestr("README.md", "ignored")

            extracted = extract_opencc_archive(archive, destination)

            self.assertEqual(extracted, 2)
            self.assertEqual((destination / "s2tg.json").read_text(encoding="utf-8"), "{}")
            self.assertEqual((destination / "STGCharacters.ocd2").read_bytes(), b"ocd2")
            self.assertTrue((destination / "local.lua").is_file())
            self.assertFalse((destination / "opencc").exists())

    def test_rejects_archive_path_traversal(self) -> None:
        from tools.fetch_opencc import extract_opencc_archive

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            archive = root / "opencc.zip"
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr("opencc/../../escaped.json", "{}")

            with self.assertRaises(ValueError):
                extract_opencc_archive(archive, root / "opencc" / "eosphoros")


class RepositoryValidationTests(unittest.TestCase):
    @classmethod
    def ios_skins(cls) -> tuple[dict[str, bytes], dict[str, bytes]]:
        if not hasattr(cls, "_ios_skins"):
            from tools.build_mobile_themes import build_ios, load_config

            cls._ios_skins = build_ios(load_config(), compresslevel=0)
        return cls._ios_skins

    def test_current_project_uses_eosphoros_names_without_legacy_paths(self) -> None:
        root = Path(__file__).resolve().parents[1]
        main_schema_path = root / "eosphoros.schema.yaml"
        self.assertTrue(main_schema_path.is_file())
        main_schema = main_schema_path.read_text(encoding="utf-8")
        self.assertIn("schema_id: eosphoros", main_schema)
        self.assertIn("name: 晨星键道", main_schema)
        custom_schema = (root / "eosphoros.custom.yaml").read_text(encoding="utf-8")
        self.assertIn("schema/name: 🌟晨星", custom_schema)
        self.assertNotIn("🌟🐈", custom_schema)
        for relative in (
            "dicts/eosphoros",
            "lua/eosphoros",
            "opencc/eosphoros",
        ):
            self.assertTrue((root / relative).is_dir(), relative)

        legacy_paths = []
        for path in root.rglob("*"):
            relative = path.relative_to(root)
            if (
                relative.parts
                and relative.parts[0] in {".git", ".pixi", ".tmp", "build"}
            ) or "__pycache__" in relative.parts:
                continue
            if ("xm" + "jd6") in path.name.lower():
                legacy_paths.append(relative.as_posix())
        self.assertEqual(legacy_paths, [])

    def test_fcitx5_theme_collections_match_desktop_sources(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "tools/build_fcitx5_themes.py", "--check"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        manifest = yaml.safe_load(
            (root / "fcitx5" / "themes.yaml").read_text(encoding="utf-8")
        )
        theme_ids = {item["id"] for item in manifest["themes"]}
        artifact_ids = {item["artifact"] for item in manifest["themes"]}
        self.assertIn("EosphorosLight", theme_ids)
        self.assertIn("EosphorosDark", theme_ids)
        self.assertIn("EosphorosMono", theme_ids)
        self.assertIn("mono", artifact_ids)
        self.assertGreater(len(theme_ids), 50)

        linux_root = root / "fcitx5" / "linux" / "themes"
        macos_root = root / "fcitx5" / "macos" / "themes"
        self.assertEqual(
            {path.name.removeprefix("eosphoros-") for path in linux_root.iterdir()},
            artifact_ids,
        )
        self.assertEqual(
            {
                path.stem.removeprefix("eosphoros-")
                for path in macos_root.glob("eosphoros-*.conf")
                if path.stem != "eosphoros-auto"
            },
            artifact_ids,
        )

        for path in linux_root.glob("*/theme.conf"):
            parser = configparser.ConfigParser(interpolation=None)
            parser.optionxform = str
            parser.read(path, encoding="utf-8")
            self.assertIn("Metadata", parser, path)
            self.assertIn("InputPanel", parser, path)
            self.assertIn("InputPanel/Background", parser, path)
            self.assertIn("InputPanel/Highlight", parser, path)
            self.assertRegex(parser["InputPanel"]["NormalColor"], r"^#[0-9A-F]{8}$")

        auto_theme = configparser.ConfigParser(interpolation=None)
        auto_theme.optionxform = str
        auto_theme.read(macos_root / "eosphoros-auto.conf", encoding="utf-8")
        self.assertEqual(auto_theme["LightMode"]["OverrideDefault"], "True")
        self.assertEqual(auto_theme["DarkMode"]["OverrideDefault"], "True")
        self.assertEqual(auto_theme["DarkMode"]["SameWithLightMode"], "False")
        self.assertEqual(auto_theme["LightMode"]["HighlightColor"], "#1E1D1AFF")
        self.assertEqual(auto_theme["DarkMode"]["HighlightColor"], "#F1EEE8FF")
        self.assertEqual(auto_theme["DarkMode"]["TextColor"], "#E6E1D8FF")
        self.assertEqual(auto_theme["Typography"]["WritingMode"], "Horizontal top-bottom")

        mac_color_fields = {
            "HighlightColor",
            "HighlightHoverColor",
            "HighlightTextColor",
            "HighlightTextPressColor",
            "HighlightLabelColor",
            "HighlightCommentColor",
            "HighlightMarkColor",
            "PanelColor",
            "TextColor",
            "LabelColor",
            "CommentColor",
            "PagingButtonColor",
            "DisabledPagingButtonColor",
            "AuxColor",
            "PreeditColorPreCaret",
            "PreeditColorCaret",
            "PreeditColorPostCaret",
            "BorderColor",
            "DividerColor",
        }
        for path in macos_root.glob("*.conf"):
            parser = configparser.ConfigParser(interpolation=None)
            parser.optionxform = str
            parser.read(path, encoding="utf-8")
            for section in ("LightMode", "DarkMode"):
                self.assertTrue(mac_color_fields <= set(parser[section]), path)
                for field in mac_color_fields:
                    self.assertRegex(parser[section][field], r"^#[0-9A-F]{8}$")

    def test_release_embeds_fcitx5_themes_in_platform_archives(self) -> None:
        root = Path(__file__).resolve().parents[1]
        release_workflow = (root / ".github/workflows/create-release.yml").read_text(
            encoding="utf-8"
        )
        package_workflow = (root / ".github/workflows/package-master.yml").read_text(
            encoding="utf-8"
        )
        for platform in ("linux", "macos"):
            artifact = f"fcitx5-{platform}-eosphoros-themes"
            self.assertNotIn(f"{artifact}.zip", release_workflow)
            self.assertRegex(
                release_workflow,
                rf"(?m)^\s+eosphoros-fcitx5-{platform}\.zip$",
            )
            self.assertNotIn(f"name: {artifact}", package_workflow)
        self.assertIn("name: Upload complete build", package_workflow)
        self.assertNotIn("!fcitx5/**", package_workflow)

    def test_native_mobile_themes_are_current_and_importable(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "tools/build_mobile_themes.py", "--check"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        required = {
            "name",
            "isDark",
            "backgroundImage",
            "backgroundColor",
            "barColor",
            "keyboardColor",
            "keyBackgroundColor",
            "keyTextColor",
            "candidateTextColor",
            "candidateLabelColor",
            "candidateCommentColor",
            "altKeyBackgroundColor",
            "altKeyTextColor",
            "accentKeyBackgroundColor",
            "accentKeyTextColor",
            "keyPressHighlightColor",
            "keyShadowColor",
            "popupBackgroundColor",
            "popupTextColor",
            "spaceBarColor",
            "dividerColor",
            "clipboardEntryColor",
            "genericActiveBackgroundColor",
            "genericActiveForegroundColor",
            "version",
        }
        theme_dir = root / "mobile_themes" / "fcitx5-android"
        self.assertEqual(
            {path.name for path in theme_dir.glob("*.zip")},
            {"eosphoros-dawn.zip", "eosphoros-night.zip", "eosphoros-mono.zip"},
        )
        for archive_path in theme_dir.glob("*.zip"):
            with zipfile.ZipFile(archive_path) as archive:
                self.assertEqual(len(archive.namelist()), 1)
                payload = json.loads(archive.read(archive.namelist()[0]))
            self.assertEqual(set(payload), required)
            self.assertEqual(payload["version"], "2.1")
            self.assertIsNone(payload["backgroundImage"])

        trime_dir = root / "mobile_themes" / "trime"
        self.assertEqual(
            {path.name for path in trime_dir.glob("*.trime.yaml")},
            {"eosphoros.trime.yaml"},
        )
        for path in trime_dir.glob("*.trime.yaml"):
            trime = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertEqual(trime["config_version"], "3.0")
            self.assertEqual(trime["name"], "晨星键道·格调")
            self.assertNotIn("__include", trime)
            self.assertIn("preset_keyboards", trime)
            self.assertIn("preset_keys", trime)
            self.assertIn("liquid_keyboard", trime)
            self.assertEqual(trime["style"]["color_scheme"], "eosphoros_dawn")
            self.assertEqual(trime["style"]["color_scheme_dark"], "eosphoros_night")
            # The distributed keyboard follows the user-reviewed 格调 layout,
            # not mytrime's stock classic geometry.
            self.assertEqual(trime["height"][6], 4)
            self.assertEqual(trime["round_corner"][1], 3)
            default_keyboard = trime["preset_keyboards"]["default"]
            self.assertEqual(default_keyboard["width"], 11.12)
            self.assertEqual(default_keyboard["keys"][0]["width"], 10)
            self.assertEqual(default_keyboard["keys"][10]["width"], 0)
            self.assertEqual(default_keyboard["keys"][20]["width"], 0)
            self.assertEqual(default_keyboard["keys"][33]["width"], 27)
            self.assertEqual(default_keyboard["keys"][36]["width"], 14)
            self.assertEqual(
                set(trime["preset_color_schemes"]),
                {"eosphoros_dawn", "eosphoros_night", "eosphoros_mono"},
            )
            layout_color_roles = {
                "bkg", "tkg", "benter", "tenter", "bgn", "tgn", "bbs",
                "tbs", "baoe", "taoe", "bh1", "th1", "bh2", "th2",
                "bh3", "th3", "bh4", "th4", "bh5", "bh6", "c1", "c2",
                "c3", "c4", "c5", "c7",
            }
            for scheme_name in ("eosphoros_dawn", "eosphoros_night", "eosphoros_mono"):
                self.assertTrue(
                    layout_color_roles.issubset(
                        trime["preset_color_schemes"][scheme_name]
                    )
                )
                scheme = trime["preset_color_schemes"][scheme_name]
                self.assertEqual(scheme["bh6"], scheme["key_back_color"])
                self.assertEqual(scheme["c5"], scheme["off_key_back_color"])
            self.assertEqual(default_keyboard["keys"][30]["key_text_color"], "tgn")
            self.assertEqual(default_keyboard["keys"][31]["key_text_color"], "tgn")
            self.assertEqual(default_keyboard["keys"][35]["click"], "Keyboard_letter1")
            self.assertIn(
                {"keys/@33/label": "英文"},
                trime["preset_keyboards"]["letter"]["__patch"],
            )

    def test_mobile_zip_check_ignores_container_compression_bytes(self) -> None:
        from tools.build_mobile_themes import artifact_contents

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            stored = root / "stored.zip"
            deflated = root / "deflated.zip"
            with zipfile.ZipFile(stored, "w", compression=zipfile.ZIP_STORED) as archive:
                archive.writestr("theme.json", b'{"version":"2.1"}\n')
            with zipfile.ZipFile(
                deflated, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
            ) as archive:
                archive.writestr("theme.json", b'{"version":"2.1"}\n')

            self.assertNotEqual(stored.read_bytes(), deflated.read_bytes())
            self.assertEqual(artifact_contents(stored), artifact_contents(deflated))

    def test_locked_mobile_template_download_retries_transient_disconnects(self) -> None:
        from tools.build_mobile_themes import download_locked

        payload = b"locked mobile skin template"

        class Response:
            def __enter__(self) -> Response:
                return self

            def __exit__(self, *_args: object) -> None:
                return None

            def read(self) -> bytes:
                return payload

        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "tools.build_mobile_themes.urllib.request.urlopen",
            side_effect=[http.client.RemoteDisconnected(), Response()],
        ) as urlopen, patch("tools.build_mobile_themes.time.sleep") as sleep:
            destination = Path(temp_dir) / "template.cskin"
            result = download_locked(
                "https://example.invalid/template.cskin",
                hashlib.sha256(payload).hexdigest(),
                destination,
            )

        self.assertEqual(result, payload)
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(1)

    def test_release_embeds_native_mobile_themes_in_platform_archives(self) -> None:
        root = Path(__file__).resolve().parents[1]
        release = (root / ".github/workflows/create-release.yml").read_text(
            encoding="utf-8"
        )
        package = (root / ".github/workflows/package-master.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("python tools/build_mobile_themes.py --platform-dir .", release)
        for archive in (
            "eosphoros-trime-android.zip",
            "eosphoros-fcitx5-android.zip",
            "eosphoros-yuanshu-ios-rime.zip",
            "eosphoros-hamster-ios-rime.zip",
        ):
            self.assertRegex(release, rf"(?m)^\s+{re.escape(archive)}$")
        for obsolete_archive in (
            "eosphoros-mobile.zip",
            "fcitx5-linux-eosphoros-themes.zip",
            "fcitx5-macos-eosphoros-themes.zip",
            "fcitx5-android-eosphoros-themes.zip",
            "trime-eosphoros-theme.zip",
            "yuanshu-eosphoros-skins.zip",
            "hamster-eosphoros-skins.zip",
        ):
            self.assertNotRegex(release, rf"(?m)^\s+{re.escape(obsolete_archive)}$")
        self.assertIn("name: Upload complete build", package)
        self.assertNotIn("!mobile_themes/**", package)

    def test_ios_skins_are_embedded_under_platform_skin_directories(self) -> None:
        from tools.build_mobile_themes import (
            embed_ios_skins,
            load_config,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for archive_name in (
                "eosphoros-yuanshu-ios-rime.zip",
                "eosphoros-hamster-ios-rime.zip",
            ):
                with zipfile.ZipFile(root / archive_name, "w") as archive:
                    archive.writestr("eosphoros.schema.yaml", "schema:\n")

            with patch(
                "tools.build_mobile_themes.build_ios",
                return_value=self.ios_skins(),
            ):
                embed_ios_skins(load_config(), root, compresslevel=0)

            expected = {
                "eosphoros-yuanshu-ios-rime.zip": ".cskin",
                "eosphoros-hamster-ios-rime.zip": ".hskin",
            }
            for archive_name, suffix in expected.items():
                with zipfile.ZipFile(root / archive_name) as archive:
                    names = archive.namelist()
                    self.assertIn("eosphoros.schema.yaml", names)
                    self.assertIn("README-MOBILE-SKINS.txt", names)
                    self.assertEqual(
                        len(
                            [
                                name
                                for name in names
                                if name.startswith("skins/") and name.endswith(suffix)
                            ]
                        ),
                        2,
                    )
                    for skin_name in (
                        f"skins/eosphoros{suffix}",
                        f"skins/eosphoros-mono{suffix}",
                    ):
                        with zipfile.ZipFile(io.BytesIO(archive.read(skin_name))) as skin:
                            skin_names = skin.namelist()
                            skin_root = Path(skin_name).stem
                            self.assertNotIn("config.yaml", skin_names)
                            self.assertIn(f"{skin_root}/config.yaml", skin_names)
                            self.assertIn(f"{skin_root}/demo.png", skin_names)
                            self.assertTrue(
                                any(name.startswith(f"{skin_root}/dark/") for name in skin_names)
                            )
                            self.assertTrue(
                                any(name.startswith(f"{skin_root}/light/") for name in skin_names)
                            )
                            self.assertIn(f"{skin_root}/README.md", skin_names)
                            config = yaml.safe_load(
                                skin.read(f"{skin_root}/config.yaml")
                            )
                            self.assertEqual(config["author"], "eosphoros-keytao")
                            self.assertTrue(config["name"].startswith("晨星"))
                            keyboard_types = (
                                ("pinyin", "alphabetic", "numeric")
                                if suffix == ".hskin"
                                else tuple(
                                    name
                                    for name in ("pinyin", "alphabetic", "numeric")
                                    if name in config
                                )
                            )
                            for keyboard_type in keyboard_types:
                                devices = (
                                    config[keyboard_type].values()
                                    if suffix == ".cskin"
                                    else (config[keyboard_type]["iPhone"],)
                                )
                                for device in devices:
                                    for keyboard_name in device.values():
                                        for appearance in ("dark", "light"):
                                            self.assertIn(
                                                f"{skin_root}/{appearance}/{keyboard_name}.yaml",
                                                skin_names,
                                            )
                            pinyin_name = config["pinyin"]["iPhone"]["portrait"]
                            pinyin = yaml.safe_load(
                                skin.read(f"{skin_root}/light/{pinyin_name}.yaml")
                            )
                            pinyin_text = skin.read(
                                f"{skin_root}/light/{pinyin_name}.yaml"
                            ).decode("utf-8")
                            self.assertIn("keyboardStyle", pinyin)
                            self.assertGreater(len(pinyin["keyboardLayout"]), 0)
                            if suffix == ".cskin":
                                self.assertNotIn("toolbar", pinyin)
                                self.assertNotIn("preedit", pinyin)
                                self.assertIn("toolbarStyle", pinyin)
                                self.assertIn("toolbarLayout", pinyin)
                                self.assertIn("preeditStyle", pinyin)
                                self.assertGreaterEqual(pinyin["preeditHeight"], 28)
                                self.assertEqual(
                                    pinyin["preeditStyle"]["backgroundStyle"],
                                    "preeditBackgroundStyle",
                                )
                                self.assertIn("preeditBackgroundStyle", pinyin)
                                self.assertNotEqual(
                                    pinyin["preeditStyle"]["backgroundStyle"],
                                    pinyin["horizontalCandidatesStyle"]["backgroundStyle"],
                                )
                                self.assertIn("horizontalCandidatesLayout", pinyin)
                                self.assertIn("verticalCandidatesLayout", pinyin)
                                self.assertIn("buttonStyleType", pinyin_text)
                                self.assertIn("#showPasteboardView", pinyin_text)
                                self.assertIn("#showPhraseView", pinyin_text)
                                self.assertIn('"keyboardType": "emojis"', pinyin_text)
                                self.assertIn("#RimeSwitcher", pinyin_text)
                                self.assertIn('"keyboardType": "symbolic"', pinyin_text)
                                self.assertIn("#toggleScriptView", pinyin_text)
                                self.assertIn("#keyboardMenu", pinyin_text)
                                self.assertIn("#三选上屏", pinyin_text)
                                self.assertIn("temp_pinyin", config)
                                self.assertIn("panel", config)
                                self.assertIn(
                                    f"{skin_root}/jsonnet/main.jsonnet", skin_names
                                )
                            else:
                                self.assertIn("toolbar", pinyin)
                                self.assertIn("preedit", pinyin)
                                self.assertNotIn("toolbarStyle", pinyin)
                                self.assertNotIn("toolbarLayout", pinyin)
                                self.assertNotIn("preeditStyle", pinyin)
                                self.assertNotIn("buttonStyleType", pinyin_text)
                                self.assertNotRegex(
                                    pinyin_text,
                                    r"(?m)^\s+\w*[Cc]olor:\s+['\"]?#",
                                )
                                for feature in (
                                    "emoji",
                                    "float_app",
                                    "float_panel",
                                    "righthand",
                                    "lefthand",
                                ):
                                    self.assertIn(feature, config)
                                self.assertNotEqual(
                                    config["pinyin"]["iPhone"]["portrait"],
                                    config["pinyin"]["iPhone"]["landscape"],
                                )
                                self.assertTrue(
                                    any(
                                        name.startswith(f"{skin_root}/light/resources/")
                                        for name in skin_names
                                    )
                                )
                                expected_foregrounds = (
                                    {
                                        "light": {"172033", "66738A", "C68A2C"},
                                        "dark": {"F5F0E3", "AAB7CF", "E4B34B", "101522"},
                                    }
                                    if skin_root == "eosphoros"
                                    else {
                                        "light": {"000000", "666666", "FFFFFF"},
                                        "dark": {"000000", "666666", "FFFFFF"},
                                    }
                                )
                                for appearance, allowed in expected_foregrounds.items():
                                    for yaml_name in (
                                        name for name in skin_names
                                        if name.startswith(f"{skin_root}/{appearance}/")
                                        and name.endswith(".yaml")
                                    ):
                                        section = ""
                                        for line in skin.read(yaml_name).decode("utf-8").splitlines():
                                            section_match = re.match(r"^([^\s#][^:]*):", line)
                                            if section_match:
                                                section = section_match.group(1)
                                            color_match = re.match(
                                                r"^\s+(?:normalColor|highlightColor|textColor):"
                                                r"\s*['\"]?([0-9A-Fa-f]{6})",
                                                line,
                                            )
                                            if color_match and "foreground" in section.lower():
                                                self.assertIn(
                                                    color_match.group(1).upper(),
                                                    allowed,
                                                    f"unexpected foreground color in {yaml_name}",
                                                )
                            self.assertNotIn("万象键盘", pinyin_text)
                            self.assertNotIn("26键-万象", pinyin_text)

    def test_yuanshu_skins_import_as_two_named_themes_with_uniform_toolbar(self) -> None:
        yuanshu, _ = self.ios_skins()
        self.assertEqual(set(yuanshu), {"eosphoros.cskin", "eosphoros-mono.cskin"})
        expected_names = {
            "eosphoros.cskin": "晨星·昼夜／Eosphoros Adaptive",
            "eosphoros-mono.cskin": "晨星·极简／Eosphoros Mono",
        }
        actual_names = set()
        for archive_name, skin_data in yuanshu.items():
            with zipfile.ZipFile(io.BytesIO(skin_data)) as skin:
                names = skin.namelist()
                skin_root = Path(archive_name).stem
                self.assertEqual(
                    {name.split("/", 1)[0] for name in names}, {skin_root}
                )
                self.assertNotIn("config.yaml", names)
                self.assertIn(f"{skin_root}/config.yaml", names)
                self.assertIn(f"{skin_root}/demo.png", names)
                self.assertTrue(any(name.startswith(f"{skin_root}/light/") for name in names))
                self.assertTrue(any(name.startswith(f"{skin_root}/dark/") for name in names))
                config = yaml.safe_load(skin.read(f"{skin_root}/config.yaml"))
                self.assertEqual(config["name"], expected_names[archive_name])
                actual_names.add(config["name"])

                pinyin_name = config["pinyin"]["iPhone"]["portrait"]
                for appearance in ("light", "dark"):
                    keyboard = yaml.safe_load(
                        skin.read(f"{skin_root}/{appearance}/{pinyin_name}.yaml")
                    )
                    for slide_name in (
                        "toolbarSlideButtonsLeft",
                        "toolbarSlideButtonsRight",
                        "toolbarSlideButtonsCenter",
                    ):
                        self.assertEqual(
                            keyboard[slide_name]["backgroundStyle"],
                            "toolbarButtonBackgroundStyle",
                        )
                    self.assertEqual(
                        keyboard["toolbarcollectionCellBackgroundStyle"]["normalColor"],
                        0,
                    )
        self.assertEqual(len(actual_names), 2)

    def test_release_publishes_platform_packages(self) -> None:
        root = Path(__file__).resolve().parents[1]
        release = (root / ".github/workflows/create-release.yml").read_text(
            encoding="utf-8"
        )
        package = (root / ".github/workflows/package-master.yml").read_text(
            encoding="utf-8"
        )
        pixi = (root / "pixi.toml").read_text(encoding="utf-8")

        self.assertIn("python tools/build_platform_packages.py", release)
        self.assertIn("pixi run generated-quick", package)
        self.assertIn("python tools/build_platform_packages.py --check", pixi)
        self.assertIn("## 平台与词库版本", release)
        self.assertIn("| 平台 | 输入法 / 引擎 | 下载文件 | 词库档位 |", release)
        self.assertIn("releases/latest/download/eosphoros-rime-full.zip) | 完整版", release)
        self.assertIn("releases/latest/download/eosphoros-rime-standard.zip) | 标准版", release)
        self.assertIn("releases/latest/download/eosphoros-rime-lite.zip) | 精简版", release)
        for archive in (
            "eosphoros-rime-full.zip",
            "eosphoros-rime-standard.zip",
            "eosphoros-rime-lite.zip",
            "eosphoros-weasel-windows-rime.zip",
            "eosphoros-squirrel-macos-rime.zip",
            "eosphoros-fcitx5-macos.zip",
            "eosphoros-fcitx5-linux.zip",
            "eosphoros-fcitx5-macos-rime.zip",
            "eosphoros-fcitx5-linux-rime.zip",
            "eosphoros-trime-android.zip",
            "eosphoros-fcitx5-android.zip",
            "eosphoros-fcitx5-android-rime.zip",
            "eosphoros-yuanshu-ios-rime.zip",
            "eosphoros-hamster-ios-rime.zip",
        ):
            self.assertRegex(release, rf"(?m)^\s+{re.escape(archive)}$")

    def test_rabbit_release_is_minimal_and_uses_weasel_themes(self) -> None:
        from tools.prepare_rabbit_release import build_rabbit_config, load_weasel_yaml

        root = Path(__file__).resolve().parents[1]
        weasel = load_weasel_yaml(root / "weasel.yaml")
        merged = build_rabbit_config(
            {
                "suspend_hotkey": None,
                "style": {"label_format": "{:s}. "},
                "preset_color_schemes": {"aqua": {}},
            },
            weasel,
        )
        self.assertEqual(merged["style"]["color_scheme"], "EosphorosLight")
        self.assertEqual(merged["style"]["color_scheme_dark"], "EosphorosDark")
        self.assertEqual(merged["style"]["label_format"], "{:s}. ")
        self.assertEqual(merged["style"]["font_face"], "Microsoft YaHei UI")
        self.assertEqual(merged["style"]["font_point"], 16)
        self.assertEqual(merged["style"]["layout"]["min_width"], 220)
        self.assertEqual(
            merged["preset_color_schemes"]["EosphorosLight"]["color_format"],
            "abgr",
        )
        self.assertRegex(
            merged["preset_color_schemes"]["EosphorosLight"]["back_color"],
            r"^0x[0-9A-Fa-f]{6,8}$",
        )
        custom = yaml.safe_load((root / "rabbit.custom.yaml").read_text(encoding="utf-8"))
        self.assertEqual(custom["patch"]["style/color_scheme"], "EosphorosLight")
        self.assertEqual(custom["patch"]["style/color_scheme_dark"], "EosphorosDark")

        release = (root / ".github/workflows/create-release.yml").read_text(encoding="utf-8")
        self.assertIn("tools/prepare_rabbit_release.py --rabbit-dir Rabbit", release)
        self.assertIn("github.rest.repos.getLatestRelease", release)
        self.assertIn("`rabbit-${tag}-x64.zip`", release)
        self.assertIn("asset.digest", release)
        self.assertIn("sha256sum --check --strict", release)
        self.assertNotIn("RABBIT_TAG: v", release)
        self.assertNotIn("Prepare Rime directory for Rabbit", release)
        self.assertNotIn("cp -r Rime/. Rabbit/Data", release)

        preparer = (root / "tools/prepare_rabbit_release.py").read_text(encoding="utf-8")
        for name in (
            "ZZZC-Merge.cmd",
            "ZZZC-Rollback.cmd",
            "Merge-ZZZC.exe",
            "Rollback-ZZZC.exe",
        ):
            self.assertIn(name, preparer)
        self.assertIn("eosphoros_zzc_root=%RABBIT_ROOT%Data", preparer)
        self.assertIn("eosphoros_zzc_state_dir=%RABBIT_ROOT%Rime\\zzc_state", preparer)
        self.assertIn('root / "eosphoros.ico"', preparer)
        self.assertIn('root / "eosphoros-ascii.ico"', preparer)

    def test_release_uses_one_native_upload_with_checksums(self) -> None:
        root = Path(__file__).resolve().parents[1]
        release = (root / ".github/workflows/create-release.yml").read_text(
            encoding="utf-8"
        )
        workflow = yaml.safe_load(release)

        self.assertNotIn("shogo82148/actions-", release)
        self.assertIn('sha256sum "${assets[@]}" > SHA256SUMS', release)
        self.assertIn('gh release create "$RELEASE_TAG" "${assets[@]}"', release)
        self.assertIn('--repo "$GITHUB_REPOSITORY"', release)
        self.assertIn("GITHUB_RUN_NUMBER", release)
        self.assertIn("GITHUB_RUN_ATTEMPT", release)
        self.assertIn('--target "$GITHUB_SHA"', release)
        self.assertIn("inputs.dry_run == true", release)
        self.assertIn("inputs.dry_run != true", release)
        self.assertIn("name: release-dry-run-${{ github.run_number }}", release)
        self.assertNotIn("gh release upload", release)
        self.assertNotIn("gh release edit", release)
        self.assertNotIn("--clobber", release)
        self.assertIn("pattern: release-*-assets", release)
        self.assertIn("merge-multiple: true", release)
        self.assertNotIn("actions: write", release)
        jobs = workflow["jobs"]
        for job in (
            "build-native-release",
            "build-rabbit-release",
            "build-yong-release",
        ):
            self.assertIn(job, jobs)
            self.assertNotIn("validate-source", jobs[job]["needs"])
        self.assertEqual(
            set(jobs["release"]["needs"]),
            {
                "check_release_needed",
                "validate-source",
                "build-native-release",
                "build-rabbit-release",
                "build-yong-release",
            },
        )

    def test_release_yong_archive_is_the_full_portable_build(self) -> None:
        root = Path(__file__).resolve().parents[1]
        release = (root / ".github/workflows/create-release.yml").read_text(
            encoding="utf-8"
        )
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertNotIn("YONG_INI_URL", release)
        self.assertNotIn("prepare_yong_config.py", release)
        self.assertIn("packaging/yong/yong.ini", release)
        self.assertIn("zip -r ../eosphoros-yong-windows.zip yong", release)
        self.assertIn("YONG_LINUX_URL", release)
        self.assertNotIn("YONG_WIN_SHA256", release)
        self.assertNotIn("YONG_LINUX_SHA256", release)
        self.assertNotIn("warn_if_yong_changed", release)
        self.assertIn("7z x yong-lin.7z -oyong_linux_temp", release)
        self.assertIn("zip -r ../eosphoros-yong-linux.zip yong", release)
        self.assertNotIn("zip -r eosphoros-yong-windows.zip .yong", release)
        self.assertNotIn("yong-eosphoros-full.zip", release)
        self.assertNotIn("yong-eosphoros-full.zip", readme)

    def test_yong_config_is_native_to_eosphoros(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = (root / "packaging/yong/yong.ini").read_text(encoding="utf-8")

        self.assertIn("0=eosphoros", config)
        self.assertIn("[eosphoros]", config)
        self.assertIn("name=晨星键道", config)
        self.assertIn("arg=mb/eosphoros/eosphoros.txt", config)
        self.assertIn("a_caret=1", config)
        self.assertNotIn("xmjd6", config)
        self.assertNotIn("星猫", config)

    def test_yong_package_validator_checks_all_active_file_references(self) -> None:
        from tools.validate_yong_package import validate_package

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "yong"
            config_dir = package / ".yong"
            table_dir = config_dir / "mb" / "eosphoros"
            table_dir.mkdir(parents=True)
            # Yong accepts built-in assets at the executable root as well as .yong overrides.
            (package / "skin").mkdir()
            (table_dir / "eosphoros.txt").write_text("[DATA]\n", encoding="utf-8")
            (table_dir / "emoji.txt").write_text("[DATA]\n", encoding="utf-8")
            (config_dir / "yong.ini").write_text(
                "[IM]\nskin=skin\n[key]\ncrab=CTRL_SHIFT_ALT_H\n[eosphoros]\n"
                "arg=mb/eosphoros/eosphoros.txt\n"
                "dicts=mb/eosphoros/emoji.txt\n",
                encoding="utf-8-sig",
            )
            self.assertEqual(validate_package(package), [])
            command = subprocess.run(
                [sys.executable, "tools/validate_yong_package.py", str(package)],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(command.returncode, 0, command.stdout + command.stderr)

            (table_dir / "emoji.txt").unlink()
            errors = validate_package(package)
            self.assertEqual(len(errors), 1)
            self.assertIn("missing dicts target: mb/eosphoros/emoji.txt", errors[0])

    def test_yong_package_validator_checks_ready_android_skins(self) -> None:
        from tools.validate_yong_package import validate_package

        with tempfile.TemporaryDirectory() as temp_dir:
            package = Path(temp_dir) / "yong"
            config_dir = package / ".yong"
            android_dir = config_dir / "android"
            android_dir.mkdir(parents=True)
            (config_dir / "yong.ini").write_text("[IM]\n", encoding="utf-8")

            skin = android_dir / "Eosphoros-Dawn.zip"
            with zipfile.ZipFile(skin, "w") as archive:
                archive.writestr("keyboard.html", "<html></html>\n")
                archive.writestr("keyboard.css", "body {}\n")
            self.assertEqual(validate_package(package), [])

            with zipfile.ZipFile(skin, "w") as archive:
                archive.writestr("keyboard.html", "<html></html>\n")
            self.assertEqual(
                validate_package(package),
                ["Android skin Eosphoros-Dawn.zip is missing: keyboard.css"],
            )

    def test_yong_release_includes_offline_help_and_validates_the_archive(self) -> None:
        root = Path(__file__).resolve().parents[1]
        release = (root / ".github/workflows/create-release.yml").read_text(
            encoding="utf-8"
        )
        readme = (root / "README.md").read_text(encoding="utf-8")
        help_text = (root / "packaging/yong/README.txt").read_text(encoding="utf-8")

        self.assertIn(
            "cp packaging/yong/README.txt yong_temp/yong/README-Eosphoros.txt",
            release,
        )
        self.assertIn("python tools/validate_yong_package.py yong_temp/yong", release)
        self.assertIn("python tools/validate_yong_package.py yong_android/yong", release)
        self.assertIn(
            "python tools/validate_yong_package.py yong_linux_temp/yong", release
        )
        self.assertIn(
            "packaging/yong/android/skin --theme dawn", release
        )
        self.assertIn(
            "packaging/yong/android/skin --theme night", release
        )
        self.assertIn(".yong/android/Eosphoros-Dawn.zip", release)
        self.assertIn(".yong/android/Eosphoros-Night.zip", release)
        self.assertNotIn("yong/theme-builder", release)
        self.assertRegex(release, r"(?m)^\s+eosphoros-yong-windows\.zip$")
        self.assertRegex(release, r"(?m)^\s+eosphoros-yong-android\.zip$")
        self.assertRegex(release, r"(?m)^\s+eosphoros-yong-linux\.zip$")
        self.assertRegex(release, r"(?m)^\s+eosphoros-yong-desktop-skins\.zip$")
        self.assertIn("Ctrl + 空格", help_text)
        self.assertIn("eosphoros.txt", help_text)

        android_config = (root / "packaging/yong/android/yong.ini").read_text(
            encoding="utf-8"
        )
        android_help = (root / "packaging/yong/android/README.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn("arg=mb/eosphoros/eosphoros.txt", android_config)
        self.assertRegex(android_config, r"(?m)^\[android\]\nandroid_code_in_keyboard=0$")
        self.assertNotRegex(android_config, r"(?m)^skin=")
        self.assertNotIn("xmjd6", android_config)
        self.assertIn("/storage/emulated/0/yong/.yong/", android_help)
        self.assertIn("不需要运行 Python", android_help)
        linux_help = (root / "packaging/yong/linux/README.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn("Linux 完整包", linux_help)
        self.assertIn("$XDG_CONFIG_HOME/yong/", linux_help)
        self.assertIn("yong-tool.sh --install", linux_help)
        self.assertIn("Default5 SVG", readme)
        self.assertIn("Android 皮肤制作参考", readme)
        self.assertIn("tankb52/fcitx5-andoird-themes", readme)
        self.assertIn("fcitx5-android.github.io/theme-designer", readme)

        desktop_config = (root / "packaging/yong/yong.ini").read_text(
            encoding="utf-8"
        )
        self.assertIn("skin=skin/Eosphoros-Mono", desktop_config)

        for skin_name in ("Eosphoros-Mono", "Eosphoros-Dawn", "Eosphoros-Graphite"):
            skin_path = root / "packaging" / "yong" / "skins" / skin_name / "skin.ini"
            skin = configparser.ConfigParser(interpolation=None)
            skin.read(skin_path, encoding="utf-8")
            self.assertEqual(
                set(skin.sections()),
                {"about", "main", "main-dark", "input", "input-dark", "tray"},
            )
            self.assertEqual(skin.get("main", "scale"), "0")
            self.assertEqual(skin.get("input", "line"), "2")
            self.assertEqual(skin.get("tray", "icon"), "tray1.ico tray2.ico")

    def test_yong_android_theme_builder_preserves_base_skin(self) -> None:
        from tools.build_yong_android_skin import build

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            base = root / "base.zip"
            output = root / "themed.zip"
            with zipfile.ZipFile(base, "w") as archive:
                archive.writestr("keyboard.html", "<html></html>\n")
                archive.writestr("keyboard.css", ":root { --背景色1: #fff; }\n")
                archive.writestr("layout.js", "const layout = {};\n")

            build(base, "night", output)

            with zipfile.ZipFile(output) as archive:
                self.assertEqual(
                    set(archive.namelist()),
                    {"keyboard.html", "keyboard.css", "layout.js"},
                )
                css = archive.read("keyboard.css").decode("utf-8")
                self.assertIn("eosphoros-theme:start", css)
                self.assertIn("--surface: #11151b", css)
                self.assertEqual(archive.read("layout.js"), b"const layout = {};\n")

    def test_yong_android_original_source_builds_ready_skins(self) -> None:
        from tools.build_yong_android_skin import build

        root = Path(__file__).resolve().parents[1]
        base = root / "packaging/yong/android/skin"
        html = (base / "keyboard.html").read_text(encoding="utf-8")
        self.assertIn("const Keyboards = {", html)
        self.assertIn("class Tools", html)
        self.assertIn("const TOOL_ICONS = {", html)
        self.assertIn('span.setAttribute("aria-label", list[i].label)', html)
        self.assertIn("<svg", html)
        self.assertIn('label:"撤销"', html)
        self.assertIn('label:"重做"', html)
        self.assertIn("App.key(CTRL_MASK|KEYCODE_z)", html)
        self.assertIn("App.key(CTRL_MASK|KEYCODE_y)", html)
        self.assertIn("{v:'123',r:1.1", html)
        self.assertIn("{v:'晨星',r:2.7", html)
        self.assertIn("{v:'中/En',r:1.4", html)
        self.assertIn("{v:'⇧',c:KEYCODE_SHIFT", html)
        self.assertNotIn("document.title.charAt(0)", html)
        self.assertNotIn("Render._candidatePanel.style.paddingLeft", html)
        self.assertNotIn("{v:'l'},{v:';'}", html)
        self.assertNotIn('{title:"🎙"', html)
        self.assertNotIn('{title:"😀"', html)
        self.assertIn('overlay("clipboard",true)', html)
        self.assertIn("editor(0)", html)
        self.assertIn("emoji(0)", html)
        self.assertIn("App.voice()", html)
        self.assertIn('App.action("switchInputMethod")', html)
        self.assertIn('App.action("paste")', html)
        self.assertIn('App.action("selectAll")', html)
        self.assertIn('App.action("copy")', html)
        self.assertIn('App.action("cut")', html)
        self.assertNotRegex(html, r"https?://|fetch\(|XMLHttpRequest|WebSocket")
        self.assertNotRegex(html, r"简约|iOS圖|深彩|浅彩|游戏|天气|翻译")
        self.assertEqual(
            {path.name for path in base.iterdir()},
            {"keyboard.html", "keyboard.css", "fonts"},
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            for theme in ("dawn", "night"):
                output = Path(temp_dir) / f"Eosphoros-{theme}.zip"
                build(base, theme, output)
                with zipfile.ZipFile(output) as archive:
                    self.assertIn("keyboard.html", archive.namelist())
                    self.assertIn("keyboard.css", archive.namelist())
                    self.assertIn("fonts/Keyboard-Symbols.woff2", archive.namelist())
                    css = archive.read("keyboard.css").decode("utf-8")
                    self.assertIn("eosphoros-theme:start", css)
                    self.assertIn(".keyboard-candidate-panel", css)
                    self.assertIn(".overlay", css)
                    self.assertIn("height: 3.6rem", css)
                    self.assertIn("height: 2.8rem", css)
                    self.assertIn("margin-bottom: 0.38rem", css)
                    self.assertIn("border-radius: 0.3rem", css)
                    self.assertIn("text-transform: uppercase", css)
                    self.assertIn('.keyboard[data-layout="english"] .keyboard-row:nth-child(2)', css)
                    self.assertIn("padding-inline: 5%", css)
                    self.assertIn("grid-template-columns: repeat(4, minmax(0, 1fr))", css)
                    self.assertIn("font-family: Sans-serif", css)
                    self.assertIn(
                        ".keyboard-code-panel {\n  border-color: var(--divider);\n  background: var(--surface);",
                        css,
                    )
                    self.assertIn("position: relative", css)
                    self.assertRegex(css, r"min-height:\s*2rem")
        self.assertIn("{v:'⇧',c:KEYCODE_SHIFT,r:1,s:true}", html)
        self.assertIn("{v:'⌫',c:KEYCODE_DEL,r:1,s:true}", html)
        self.assertIn("{v:'晨星',r:2.7,c:KEYCODE_SPACE,s:false}", html)

    def test_generated_eosphoros_user_text_database_is_not_distributed(self) -> None:
        root = Path(__file__).resolve().parents[1]

        self.assertFalse((root / "eosphoros_user.txt").exists())
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", "--no-index", "eosphoros_user.txt"],
            cwd=root,
            check=False,
        )
        self.assertEqual(ignored.returncode, 0)

    def test_plum_recipes_install_frontend_specific_runtime_files(self) -> None:
        root = Path(__file__).resolve().parents[1]
        recipe_files = {
            "core": root / "recipe.yaml",
            "weasel": root / "weasel.recipe.yaml",
            "rabbit": root / "rabbit.recipe.yaml",
            "squirrel": root / "squirrel.recipe.yaml",
            "mobile": root / "mobile.recipe.yaml",
        }
        recipes = {
            name: path.read_text(encoding="utf-8")
            for name, path in recipe_files.items()
        }
        patterns = {
            name: recipe.split("install_files: >-", 1)[1]
            .split("patch_files:", 1)[0]
            .split()
            for name, recipe in recipes.items()
        }

        runtime_files = [
            *root.glob("*.yaml"),
            *(root / "dicts" / "eosphoros").glob("*.dict.yaml"),
            *(root / "lua" / "eosphoros").rglob("*.lua"),
            *(root / "opencc" / "eosphoros").rglob("*.lua"),
        ]
        runtime_names = {
            path.relative_to(root).as_posix()
            for path in runtime_files
            if not path.name.endswith("recipe.yaml")
            and not path.name.endswith(".custom.yaml")
        }
        installed_names = {
            name
            for name in runtime_names
            if any(
                fnmatch.fnmatchcase(name, pattern)
                for recipe_patterns in patterns.values()
                for pattern in recipe_patterns
            )
        }

        self.assertEqual(installed_names, runtime_names)
        for recipe_patterns in patterns.values():
            self.assertFalse(
                any(fnmatch.fnmatchcase("recipe.yaml", pattern) for pattern in recipe_patterns)
            )
        for custom_name in (
            "default.custom.yaml",
            "squirrel.custom.yaml",
            "weasel.custom.yaml",
            "rabbit.custom.yaml",
        ):
            for name, recipe_patterns in patterns.items():
                self.assertFalse(
                    any(
                        fnmatch.fnmatchcase(custom_name, pattern)
                        for pattern in recipe_patterns
                    ),
                    f"{name}: {custom_name}",
                )

        for recipe in recipes.values():
            self.assertIn("patch_files:", recipe)
            self.assertIn("default.custom.yaml:", recipe)
            self.assertIn("- schema: eosphoros", recipe)
        for name, recipe_patterns in patterns.items():
            self.assertIn("eosphoros.custom.yaml", recipe_patterns, name)
            for icon_name in ("eosphoros.ico", "eosphoros-ascii.ico"):
                self.assertTrue(
                    any(fnmatch.fnmatchcase(icon_name, pattern) for pattern in recipe_patterns),
                    f"{name}: {icon_name}",
                )
            self.assertEqual(
                [item for item in recipe_patterns if item.startswith("zzc_state/")],
                ["zzc_state/char_parts.tsv"],
                name,
            )
            for shared_zzc in (
                "zzc/README.md",
                "zzc/自造词使用教程.md",
                "zzc/自造词使用教程.png",
                "zzc/eosphoros_词库合并.py",
                "zzc/eosphoros_撤回合并.py",
            ):
                self.assertIn(shared_zzc, recipe_patterns, name)

        self.assertFalse(any("weasel" in item for item in patterns["core"]))
        self.assertFalse(any("squirrel" in item for item in patterns["core"]))
        self.assertFalse(any("Hamster" in item for item in patterns["core"]))
        self.assertTrue(any("weasel" in item for item in patterns["weasel"]))
        self.assertFalse(any("weasel" in item for item in patterns["rabbit"]))
        self.assertIn("rabbit_themes.yaml", patterns["rabbit"])
        self.assertTrue(any("squirrel" in item for item in patterns["squirrel"]))
        self.assertTrue(any("Hamster" in item for item in patterns["mobile"]))
        for weasel_zzc in (
            "zzc/Win_词库合并.exe",
            "zzc/Win_撤回合并.exe",
            "zzc/Windows_词库合并.py",
            "zzc/Windows_撤回合并.py",
        ):
            self.assertIn(weasel_zzc, patterns["weasel"])
        for squirrel_zzc in ("zzc/Mac_词库合并", "zzc/Mac_撤回合并"):
            self.assertIn(squirrel_zzc, patterns["squirrel"])
        for mobile_zzc in (
            "zzc/iOS_词库合并.py",
            "zzc/iOS快捷指令合并说明.md",
            "zzc/a-Shell快捷指令合并说明.md",
        ):
            self.assertIn(mobile_zzc, patterns["mobile"])
        shared_zzc = {
            "zzc/README.md",
            "zzc/自造词使用教程.md",
            "zzc/自造词使用教程.png",
            "zzc/eosphoros_词库合并.py",
            "zzc/eosphoros_撤回合并.py",
        }
        platform_zzc = {
            "core": set(),
            "weasel": {
                "zzc/Win_词库合并.exe",
                "zzc/Win_撤回合并.exe",
                "zzc/Windows_词库合并.py",
                "zzc/Windows_撤回合并.py",
            },
            "rabbit": {
                "zzc/Win_词库合并.exe",
                "zzc/Win_撤回合并.exe",
                "zzc/Windows_词库合并.py",
                "zzc/Windows_撤回合并.py",
            },
            "squirrel": {"zzc/Mac_词库合并", "zzc/Mac_撤回合并"},
            "mobile": {
                "zzc/iOS_词库合并.py",
                "zzc/iOS快捷指令合并说明.md",
                "zzc/a-Shell快捷指令合并说明.md",
            },
        }
        for name, recipe_patterns in patterns.items():
            self.assertEqual(
                {item for item in recipe_patterns if item.startswith("zzc/")},
                shared_zzc | platform_zzc[name],
                name,
            )

    def test_plum_install_keeps_the_eosphoros_scheme_icon(self) -> None:
        root = Path(__file__).resolve().parents[1]
        schema = (root / "eosphoros.schema.yaml").read_text(encoding="utf-8")
        custom = (root / "eosphoros.custom.yaml").read_text(encoding="utf-8")

        for name in (
            "recipe.yaml",
            "weasel.recipe.yaml",
            "rabbit.recipe.yaml",
            "squirrel.recipe.yaml",
            "mobile.recipe.yaml",
        ):
            recipe = (root / name).read_text(encoding="utf-8")
            install_block = recipe.split("install_files: >-", 1)[1].split(
                "patch_files:", 1
            )[0]
            patterns = install_block.split()
            self.assertTrue(
                any(
                    fnmatch.fnmatchcase("eosphoros.custom.yaml", pattern)
                    for pattern in patterns
                ),
                name,
            )
        self.assertIn('  icon: ""', schema)
        self.assertIn('schema/icon: "eosphoros.ico"', custom)
        self.assertIn('schema/ascii_icon: "eosphoros-ascii.ico"', custom)

    def test_icon_check_ignores_equivalent_ico_container_bytes(self) -> None:
        from tools.build_eosphoros_icons import icons_visually_equal

        root = Path(__file__).resolve().parents[1]
        expected = (root / "eosphoros-ascii.ico").read_bytes()
        # ICO readers ignore harmless trailing container bytes. This models the
        # platform encoder difference seen between Windows and Ubuntu runners.
        self.assertNotEqual(expected + b"\0", expected)
        self.assertTrue(icons_visually_equal(expected + b"\0", expected))

    def test_desktop_style_files_use_current_consistent_defaults(self) -> None:
        root = Path(__file__).resolve().parents[1]
        weasel = yaml.safe_load((root / "weasel.yaml").read_text(encoding="utf-8-sig"))
        squirrel = yaml.safe_load(
            (root / "squirrel.yaml").read_text(encoding="utf-8-sig")
        )
        weasel_custom = yaml.safe_load(
            (root / "weasel.custom.yaml").read_text(encoding="utf-8-sig")
        )["patch"]
        squirrel_custom = yaml.safe_load(
            (root / "squirrel.custom.yaml").read_text(encoding="utf-8-sig")
        )["patch"]

        for config, custom in (
            (weasel, weasel_custom),
            (squirrel, squirrel_custom),
        ):
            schemes = config["preset_color_schemes"]
            self.assertIn("EosphorosLight", schemes)
            self.assertIn("EosphorosDark", schemes)
            self.assertIn("EosphorosMono", schemes)
            self.assertEqual(config["style"]["color_scheme"], "EosphorosLight")
            self.assertEqual(config["style"]["color_scheme_dark"], "EosphorosDark")
            self.assertEqual(config["style"]["candidate_list_layout"], "stacked")
            self.assertEqual(custom["style/color_scheme"], "EosphorosLight")
            self.assertEqual(custom["style/color_scheme_dark"], "EosphorosDark")
            self.assertEqual(custom["style/candidate_list_layout"], "stacked")
            self.assertNotIn("win10", schemes)
            self.assertEqual(
                schemes["win10_MDL_blue"]["hilited_candidate_back_color"],
                0xD77800,
            )
            self.assertEqual(
                schemes["win10_MDL_darkblue"]["hilited_candidate_back_color"],
                0xD47800,
            )
            self.assertEqual(
                schemes["win10_weasel"]["hilited_candidate_back_color"],
                0xFFE8CC,
            )
            self.assertEqual(
                schemes["win11_weasel"]["hilited_candidate_back_color"],
                0xF0F0F0,
            )
            self.assertEqual(
                schemes["win11_weasel"]["hilited_mark_color"],
                0xC06700,
            )

        squirrel_style = squirrel["style"]
        self.assertIn("memorize_size", squirrel_style)
        self.assertNotIn("remember_size", squirrel_style)
        self.assertIn("mutual_exclusive", squirrel_style)
        self.assertIn("translucency", squirrel_style)
        self.assertEqual(
            squirrel_style["candidate_format"],
            "[label]. [candidate] [comment]",
        )
        for scheme in squirrel["preset_color_schemes"].values():
            if isinstance(scheme, dict):
                self.assertNotIn("horizontal", scheme)
                candidate_format = str(scheme.get("candidate_format", ""))
                self.assertNotIn("%c", candidate_format)
                self.assertNotIn("%@", candidate_format)

    def test_reviewed_xmjd6_terms_use_free_standard_codes(self) -> None:
        from tools.clean_dictionary_quality import valid_word_codes
        from tools.eosphoros_codes import (
            iter_dictionary_rows,
            load_character_code_options,
        )

        root = Path(__file__).resolve().parents[1]
        lock = json.loads(
            (root / "tools/legacy_upstream.lock.json").read_text(encoding="utf-8")
        )
        selected = set(lock["review"]["selected_terms"])
        options = load_character_code_options(
            root / "dicts/eosphoros/eosphoros.danzi.dict.yaml"
        )
        rows_by_word: dict[str, list[str]] = {}
        words_by_code: dict[str, set[str]] = {}
        for path in sorted((root / "dicts/eosphoros").glob("*.dict.yaml")):
            for word, code in iter_dictionary_rows(path):
                rows_by_word.setdefault(word, []).append(code)
                words_by_code.setdefault(code, set()).add(word)

        self.assertEqual(selected, set(rows_by_word) & selected)
        for word in selected:
            self.assertEqual(len(rows_by_word[word]), 1, word)
            code = rows_by_word[word][0]
            self.assertIn(code, valid_word_codes(word, options), (word, code))
            self.assertEqual(words_by_code[code], {word}, (word, code))

    def test_xmjd6_upstream_checker_uses_review_lock(self) -> None:
        from tools import check_legacy_upstream

        lock = json.loads(check_legacy_upstream.LOCK_PATH.read_text(encoding="utf-8"))
        with patch.object(
            check_legacy_upstream,
            "remote_commit",
            return_value=lock["reviewed_commit"],
        ):
            report = check_legacy_upstream.build_report()
        self.assertFalse(report["update_available"])
        self.assertEqual(report["reviewed_commit"], lock["reviewed_commit"])

    def test_desktop_style_yaml_has_no_duplicate_keys(self) -> None:
        root = Path(__file__).resolve().parents[1]

        def duplicate_keys(path: Path) -> list[str]:
            document = yaml.compose(path.read_text(encoding="utf-8-sig"))
            duplicates: list[str] = []

            def visit(node: yaml.Node, prefix: str = "") -> None:
                if isinstance(node, yaml.MappingNode):
                    seen: set[str] = set()
                    for key_node, value_node in node.value:
                        key = str(key_node.value)
                        if key in seen:
                            duplicates.append(f"{prefix}/{key}")
                        seen.add(key)
                        visit(value_node, f"{prefix}/{key}")
                elif isinstance(node, yaml.SequenceNode):
                    for index, value_node in enumerate(node.value):
                        visit(value_node, f"{prefix}/{index}")

            if document is not None:
                visit(document)
            return duplicates

        for filename in (
            "weasel.yaml",
            "squirrel.yaml",
            "weasel.custom.yaml",
            "squirrel.custom.yaml",
            "Hamster.yaml",
        ):
            self.assertEqual(duplicate_keys(root / filename), [], filename)

    def test_desktop_theme_names_are_canonical_and_palettes_are_usable(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = yaml.safe_load(
            (root / "tools" / "desktop_theme_names.yaml").read_text(
                encoding="utf-8"
            )
        )
        canonical_names = manifest["names"]
        removed = set(manifest["removed"])
        seen: set[str] = set()

        for filename in ("weasel.yaml", "squirrel.yaml"):
            document = yaml.safe_load(
                (root / filename).read_text(encoding="utf-8-sig")
            )
            schemes = document["preset_color_schemes"]
            self.assertTrue(removed.isdisjoint(schemes), filename)
            for scheme_id, scheme in schemes.items():
                self.assertIn(scheme_id, canonical_names, filename)
                self.assertIsInstance(scheme, dict, f"{filename}: {scheme_id}")
                self.assertEqual(
                    scheme.get("name"),
                    canonical_names[scheme_id],
                    f"{filename}: {scheme_id}",
                )
                self.assertNotIn("creat_time", scheme, f"{filename}: {scheme_id}")
                if scheme_id != "native":
                    self.assertIn("back_color", scheme, f"{filename}: {scheme_id}")
                    self.assertTrue(
                        any(
                            key in scheme
                            for key in ("candidate_text_color", "text_color")
                        ),
                        f"{filename}: {scheme_id}",
                    )
                seen.add(scheme_id)

        self.assertEqual(seen, set(canonical_names))

    def test_main_schema_exposes_explicit_switch_defaults_for_rimetool(self) -> None:
        root = Path(__file__).resolve().parents[1]
        schema = (root / "eosphoros.schema.yaml").read_text(encoding="utf-8")
        expected_defaults = {
            "ascii_mode": 0,
            "jffh": 0,
            "completion": 1,
            "emoji_cn": 1,
            "direct_symbols": 1,
            "smarttwo": 0,
            "jisuanqi": 1,
            "auto_fallback": 0,
            "sbb_hint": 1,
            "mars": 0,
            "full_shape": 0,
        }

        for name, reset in expected_defaults.items():
            self.assertIn(
                f"- name: {name}",
                schema,
            )
            switch_block = schema.split(f"- name: {name}", 1)[1].split("- name:", 1)[0]
            self.assertIn(f"reset: {reset}", switch_block, name)

    def test_main_schema_supports_rimetool_mint_template_with_live_aliases(self) -> None:
        root = Path(__file__).resolve().parents[1]
        schema = (root / "eosphoros.schema.yaml").read_text(encoding="utf-8")
        opencc_filter = (root / "lua" / "eosphoros" / "eosphoros_opencc_filter.lua").read_text(
            encoding="utf-8"
        )
        processor = (root / "lua" / "eosphoros" / "eosphoros_processor.lua").read_text(
            encoding="utf-8"
        )

        for node in (
            "melt_eng:",
            "  - name: transcription",
            "  - name: emoji",
            "  - name: ascii_punct",
            "menu:\n  page_size:",
        ):
            self.assertIn(node, schema)
        self.assertLess(schema.index("  - name: transcription"), schema.index("  - name: emoji"))
        self.assertLess(schema.index("melt_eng:"), schema.index("  - name: ascii_punct"))
        self.assertIn("options: [ jffh, transcription ]", schema)
        self.assertEqual(schema.count("options: [ emoji_cn, emoji ]"), 2)
        self.assertIn('ctx:get_option("emoji_cn") or ctx:get_option("emoji")', opencc_filter)
        self.assertIn('config:get_string("melt_eng/prefix")', processor)

    def test_explicit_lua_component_namespace_resolves_module_path(self) -> None:
        from tools import validate_repo

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "lua" / "eosphoros").mkdir(parents=True)
            (root / "lua" / "eosphoros" / "filter.lua").write_text(
                "return {}\n", encoding="utf-8"
            )
            (root / "eosphoros.schema.yaml").write_text(
                "filters:\n  - lua_filter@*eosphoros/filter@filter_namespace\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            with patch.object(validate_repo, "ROOT", root):
                validate_repo.validate_module_references(errors)

        self.assertEqual(errors, [])

    def test_main_schema_gives_opencc_filter_a_stable_namespace(self) -> None:
        root = Path(__file__).resolve().parents[1]
        schema = (root / "eosphoros.schema.yaml").read_text(encoding="utf-8")

        self.assertIn(
            "lua_filter@*eosphoros/eosphoros_opencc_filter@eosphoros_opencc_filter",
            schema,
        )

    def test_modular_ascii_handler_owns_uppercase_and_shift_behavior(self) -> None:
        root = Path(__file__).resolve().parents[1]
        schema = (root / "eosphoros.schema.yaml").read_text(encoding="utf-8")
        custom = (root / "eosphoros.custom.yaml").read_text(encoding="utf-8")

        self.assertNotIn("uppercase:", schema)
        self.assertIn("Shift_L: commit_code", schema)
        self.assertIn("Shift_R: commit_code", schema)
        self.assertIn("Shift_L: commit_code", custom)
        self.assertIn("Shift_R: commit_code", custom)

    def test_zzc_merge_targets_the_eosphoros_cizu_dictionary(self) -> None:
        root = Path(__file__).resolve().parents[1]
        script = root / "zzc" / "eosphoros_词库合并.py"
        spec = importlib.util.spec_from_file_location("eosphoros_zzc_merge_test", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader if spec else None)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)

        self.assertEqual(
            module.target_dict_name_options("eosphoros"),
            [["eosphoros.cizu.dict.yaml"], ["eosphoros.fjcy.dict.yaml"]],
        )
        self.assertEqual(
            module.resolve_target_dicts(root, "eosphoros"),
            [
                root / "dicts" / "eosphoros" / "eosphoros.cizu.dict.yaml",
                root / "dicts" / "eosphoros" / "eosphoros.fjcy.dict.yaml",
            ],
        )
        with self.assertRaisesRegex(ValueError, "expected eosphoros"):
            module.target_dict_name_options("other")
        with self.assertRaisesRegex(ValueError, "expected eosphoros"):
            module.target_dict_name_options("xmjd7")

    def test_zzc_merge_integrates_numbered_eosphoros_operation_files(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        dictionary_header = """# Rime dictionary
---
name: {name}
version: "2026-08-09"
sort: by_weight
...
"""
        operation_header = """# Rime dictionary
# encoding: utf-8
---
name: eosphoros.zzc
version: "2026-08-09"
sort: by_weight
use_preset_vocabulary: false
columns:
  - text
  - code
...
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            zzc_dir = root / "zzc"
            zzc_dir.mkdir()
            shutil.copy2(repository / "zzc" / "eosphoros_词库合并.py", zzc_dir)
            dict_path(root, "eosphoros.cizu.dict.yaml").write_text(
                dictionary_header.format(name="eosphoros.cizu"), encoding="utf-8"
            )
            dict_path(root, "eosphoros.fjcy.dict.yaml").write_text(
                dictionary_header.format(name="eosphoros.fjcy"), encoding="utf-8"
            )
            dict_path(root, "eosphoros.zzc.dict(1).yaml").write_text(
                operation_header + "100\tadd\t测试自造词\tcszc\t+\n",
                encoding="utf-8",
            )
            state_dir = root / "zzc_state"
            state_dir.mkdir()
            (state_dir / "runtime_ops.tsv").write_text("", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(zzc_dir / "eosphoros_词库合并.py")],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            self.assertEqual(
                result.returncode,
                0,
                (result.stdout or "") + (result.stderr or ""),
            )
            merged = dict_path(root, "eosphoros.cizu.dict.yaml").read_text(encoding="utf-8")
            self.assertIn("测试自造词\tcszc", merged)
            self.assertFalse(dict_path(root, "eosphoros.zzc.dict(1).yaml").exists())
            self.assertEqual(
                dict_path(root, "eosphoros.zzc.dict.yaml").read_text(encoding="utf-8"),
                operation_header,
            )
            for state_name in (
                "runtime_ops.tsv",
                "runtime_exact.tsv",
                "effective_state.tsv",
            ):
                self.assertEqual(
                    (root / "zzc_state" / state_name).read_bytes(),
                    b"\n",
                    state_name,
                )

    def test_zzc_lua_keeps_logically_empty_state_files_icloud_safe(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        lua = shutil.which("lua5.4") or shutil.which("lua") or shutil.which("luajit")
        if not lua:
            self.skipTest("Lua runtime is unavailable")

        with tempfile.TemporaryDirectory() as temp_dir:
            state_dir = Path(temp_dir) / "zzc_state"
            state_dir.mkdir()
            (Path(temp_dir) / "dicts" / "eosphoros").mkdir(parents=True)
            env = os.environ.copy()
            env["ZZC_TEST_DATA_DIR"] = temp_dir
            result = subprocess.run(
                [lua, "tests/zzc_icloud_state_test.lua"],
                cwd=repository,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                (result.stdout or "") + (result.stderr or ""),
            )

    def test_typing_stats_migrates_to_namespaced_zzc_state(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        lua = shutil.which("lua5.4") or shutil.which("lua") or shutil.which("luajit")
        if not lua:
            self.skipTest("Lua runtime is unavailable")

        with tempfile.TemporaryDirectory() as temp_dir:
            (Path(temp_dir) / "zzc_state").mkdir()
            env = os.environ.copy()
            env["TYPING_STATS_TEST_DATA_DIR"] = temp_dir
            result = subprocess.run(
                [lua, "tests/typing_stats_state_test.lua"],
                cwd=repository,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                (result.stdout or "") + (result.stderr or ""),
            )

    @unittest.skipUnless(sys.platform == "win32", "committed EXE is Windows-only")
    def test_windows_merge_executable_runs_current_eosphoros_behavior(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        dictionary_header = """# Rime dictionary
---
name: {name}
version: "2026-08-04"
sort: by_weight
...
"""
        operation_header = """# Rime dictionary
# encoding: utf-8
---
name: eosphoros.zzc
version: "2026-08-04"
sort: by_weight
use_preset_vocabulary: false
columns:
  - text
  - code
...
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            zzc_dir = root / "zzc"
            zzc_dir.mkdir()
            shutil.copy2(repository / "zzc" / "Win_词库合并.exe", zzc_dir)
            dict_path(root, "eosphoros.cizu.dict.yaml").write_text(
                dictionary_header.format(name="eosphoros.cizu"), encoding="utf-8"
            )
            dict_path(root, "eosphoros.fjcy.dict.yaml").write_text(
                dictionary_header.format(name="eosphoros.fjcy"), encoding="utf-8"
            )
            dict_path(root, "eosphoros.zzc.dict(1).yaml").write_text(
                operation_header + "100\tadd\tEXE当前逻辑\texedq\t+\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [str(zzc_dir / "Win_词库合并.exe")],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
                check=False,
            )

            self.assertEqual(
                result.returncode,
                0,
                (result.stdout or "") + (result.stderr or ""),
            )
            merged = dict_path(root, "eosphoros.cizu.dict.yaml").read_text(encoding="utf-8")
            self.assertIn("EXE当前逻辑\texedq", merged)
            self.assertFalse(dict_path(root, "eosphoros.zzc.dict(1).yaml").exists())
            self.assertTrue(dict_path(root, "eosphoros.zzc.dict.yaml").is_file())

    @unittest.skipUnless(sys.platform == "win32", "committed EXE is Windows-only")
    def test_windows_rollback_executable_restores_latest_merge(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        dictionary_header = """# Rime dictionary
---
name: {name}
version: "2026-08-04"
sort: by_weight
...
"""
        operation_header = """# Rime dictionary
# encoding: utf-8
---
name: eosphoros.zzc
version: "2026-08-04"
sort: by_weight
use_preset_vocabulary: false
columns:
  - text
  - code
...
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            zzc_dir = root / "zzc"
            zzc_dir.mkdir()
            for executable in ("Win_词库合并.exe", "Win_撤回合并.exe"):
                shutil.copy2(repository / "zzc" / executable, zzc_dir)
            original_cizu = dictionary_header.format(name="eosphoros.cizu") + "原词\tycw\n"
            dict_path(root, "eosphoros.cizu.dict.yaml").write_text(original_cizu, encoding="utf-8")
            dict_path(root, "eosphoros.fjcy.dict.yaml").write_text(
                dictionary_header.format(name="eosphoros.fjcy"), encoding="utf-8"
            )
            original_ops = operation_header + "100\tadd\t待撤回词\tdcht\t+\n"
            dict_path(root, "eosphoros.zzc.dict.yaml").write_text(original_ops, encoding="utf-8")

            merge = subprocess.run(
                [str(zzc_dir / "Win_词库合并.exe")],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
                check=False,
            )
            self.assertEqual(merge.returncode, 0, (merge.stdout or "") + (merge.stderr or ""))
            self.assertIn(
                "待撤回词\tdcht",
                dict_path(root, "eosphoros.cizu.dict.yaml").read_text(encoding="utf-8"),
            )

            rollback = subprocess.run(
                [str(zzc_dir / "Win_撤回合并.exe")],
                cwd=root,
                input="1\nYES\n",
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
                check=False,
            )

            self.assertEqual(
                rollback.returncode,
                0,
                (rollback.stdout or "") + (rollback.stderr or ""),
            )
            self.assertEqual(
                dict_path(root, "eosphoros.cizu.dict.yaml").read_text(encoding="utf-8"),
                original_cizu,
            )
            self.assertEqual(
                dict_path(root, "eosphoros.zzc.dict.yaml").read_text(encoding="utf-8"),
                original_ops,
            )

    def test_committed_windows_executables_match_sources_and_lock(self) -> None:
        from tools.build_zzc_windows_exe import validate_committed_outputs

        self.assertEqual(validate_committed_outputs(), [])

    def test_windows_executables_are_binary_git_assets(self) -> None:
        root = Path(__file__).resolve().parents[1]
        attributes = (root / ".gitattributes").read_text(encoding="utf-8")

        self.assertRegex(attributes, r"(?m)^\*\.exe\s+binary\s*$")

    def test_only_release_rebuilds_windows_executables(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflows = root / ".github" / "workflows"
        package = (workflows / "package-master.yml").read_text(encoding="utf-8")
        release = (workflows / "create-release.yml").read_text(encoding="utf-8")

        for release_only in (
            "build-windows-executables:",
            "windows-latest",
            "pixi run python tools/build_zzc_windows_exe.py",
            "name: zzc-windows-executables",
        ):
            self.assertNotIn(release_only, package)
            self.assertIn(release_only, release)

        self.assertNotIn("actions/setup-python", release)
        self.assertNotIn("python -m pip install", release)
        self.assertIn("validate-source:", release)
        self.assertIn("pixi run check", release)
        self.assertNotIn("actions/setup-python", package)
        self.assertNotIn("python -m pip install", package)
        self.assertIn("pixi run test", package)
        self.assertIn("pixi run quality", package)
        self.assertIn("pixi run generated-quick", package)
        self.assertIn("tests:", package)
        self.assertIn("generated-quality:", package)
        self.assertIn("build-native:", package)
        self.assertIn("cancel-in-progress: true", package)
        self.assertIn("Build Fcitx5 packages and compile Rime core in parallel", package)

        for executable_check in (
            "test_windows_merge_executable_runs_current_eosphoros_behavior",
            "test_windows_rollback_executable_restores_latest_merge",
            "test_committed_windows_executables_match_sources_and_lock",
        ):
            self.assertIn(executable_check, release)

    def test_every_python_workflow_forces_utf8_io(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflows = root / ".github" / "workflows"

        for path in workflows.glob("*.yml"):
            workflow = path.read_text(encoding="utf-8")
            if "actions/setup-python@" not in workflow:
                continue
            self.assertIn('PYTHONUTF8: "1"', workflow, path.name)
            self.assertIn('PYTHONIOENCODING: "utf-8"', workflow, path.name)
            self.assertIn('PYTHONNOUSERSITE: "1"', workflow, path.name)

    def test_python_dependency_workflows_pin_pip(self) -> None:
        workflow_dir = Path(__file__).resolve().parents[1] / ".github" / "workflows"
        for path in workflow_dir.glob("*.yml"):
            workflow = path.read_text(encoding="utf-8")
            if "python -m pip install -r requirements-dev.txt" not in workflow:
                continue
            self.assertIn(
                "python -m pip install --upgrade -r requirements-ci.txt",
                workflow,
                path.name,
            )

    def test_dependency_manifests_are_aligned_and_automated(self) -> None:
        from tools.sync_dependency_manifests import render_pixi

        root = Path(__file__).resolve().parents[1]
        self.assertEqual(
            (root / "pixi.toml").read_text(encoding="utf-8"),
            render_pixi(),
        )
        dependabot = (root / ".github/dependabot.yml").read_text(encoding="utf-8")
        sync = (
            root / ".github/workflows/sync-development-dependencies.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("package-ecosystem: pip", dependabot)
        self.assertIn("package-ecosystem: github-actions", dependabot)
        self.assertIn("./.github/actions/setup-pixi", sync)
        self.assertLess(
            sync.index("./.github/actions/setup-pixi"),
            sync.index("Align Pixi manifest with Dependabot-managed requirements"),
        )
        self.assertIn("pixi update", sync)
        self.assertIn("pixi run check", sync)
        self.assertIn("gh pr create", sync)

    def test_heavy_automation_reuses_pixi_without_pip_bootstrap(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflows = root / ".github" / "workflows"
        for name in (
            "package-master.yml",
            "create-release.yml",
            "check-txjx-upstream.yml",
            "sync-development-dependencies.yml",
            "sync-upstream-dictionaries.yml",
        ):
            workflow = (workflows / name).read_text(encoding="utf-8")
            self.assertIn("./.github/actions/setup-pixi", workflow, name)
            self.assertNotIn("python -m pip install", workflow, name)
            self.assertNotIn("actions/setup-python", workflow, name)

        setup_action = (root / ".github/actions/setup-pixi/action.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("prefix-dev/setup-pixi@v0.10.0", setup_action)
        self.assertIn("run-install: true", setup_action)
        package = (workflows / "package-master.yml").read_text(encoding="utf-8")
        release = (workflows / "create-release.yml").read_text(encoding="utf-8")
        self.assertIn("generated-quality:", package)
        self.assertIn("pixi run test-shard", package)
        self.assertEqual(package.count("index:"), 3)
        self.assertEqual(package.count("actions/upload-artifact@v7"), 1)
        self.assertIn("./.github/actions/check-workflows", package)
        self.assertIn("tools/native_ci_fingerprint.py", package)
        self.assertIn("native-packages-v1-", package)
        self.assertIn("steps.native-cache.outputs.cache-hit != 'true'", package)
        self.assertNotIn("restore-keys:", package)
        self.assertIn("./.github/actions/fetch-opencc", package)
        self.assertIn("Build Fcitx5 packages and compile Rime core in parallel", package)
        self.assertIn("validate-source:", release)
        self.assertEqual(release.count("./.github/actions/fetch-opencc"), 2)
        self.assertIn("Build Fcitx5 packages and compile Rime core in parallel", release)

    def test_core_dictionary_prioritizes_project_name(self) -> None:
        root = Path(__file__).resolve().parents[1]
        core = dict_path(root, "eosphoros.core.dict.yaml").read_text(encoding="utf-8")
        imports = (root / "eosphoros.extended.dict.yaml").read_text(encoding="utf-8")
        self.assertIn("晨星键道\tjxjdoo\n", core)
        self.assertLess(
            imports.index("dicts/eosphoros/eosphoros.core"),
            imports.index("dicts/eosphoros/eosphoros.ice"),
        )

    def test_tracked_text_assets_are_valid_utf8(self) -> None:
        root = Path(__file__).resolve().parents[1]
        text_extensions = {
            ".conf",
            ".ini",
            ".json",
            ".lua",
            ".md",
            ".ps1",
            ".py",
            ".sh",
            ".txt",
            ".yaml",
            ".yml",
        }
        tracked = subprocess.run(
            [
                "git", "-c", "core.quotepath=false", "ls-files",
                "--cached", "--others", "--exclude-standard", "-z",
            ],
            cwd=root,
            capture_output=True,
            check=True,
        ).stdout.decode("utf-8")

        for relative in tracked.split("\0"):
            if not relative:
                continue
            path = root / relative
            if not path.is_file():
                continue
            if path.suffix.lower() not in text_extensions and path.name != "VERSION":
                continue
            try:
                path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError as exc:
                self.fail(f"{relative} is not valid UTF-8: {exc}")

    def test_windows_executable_builder_reconfigures_stdio_to_utf8(self) -> None:
        root = Path(__file__).resolve().parents[1]
        code = """
import sys
sys.stdout.reconfigure(encoding="cp1252", errors="strict")
sys.stderr.reconfigure(encoding="cp1252", errors="strict")
from tools.build_zzc_windows_exe import configure_utf8_stdio
configure_utf8_stdio()
print("Win_词库合并.exe")
print("Win_撤回合并.exe", file=sys.stderr)
"""

        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=root,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        self.assertEqual(result.stdout.decode("utf-8").strip(), "Win_词库合并.exe")
        self.assertEqual(result.stderr.decode("utf-8").strip(), "Win_撤回合并.exe")

    def test_bundled_zzc_sources_reconfigure_stdio_to_utf8(self) -> None:
        root = Path(__file__).resolve().parents[1]
        scripts = (
            root / "zzc" / "eosphoros_词库合并.py",
            root / "zzc" / "eosphoros_撤回合并.py",
        )
        code = """
import importlib.util
import sys
sys.stdout.reconfigure(encoding="cp1252", errors="strict")
sys.stderr.reconfigure(encoding="cp1252", errors="strict")
for index, path in enumerate(sys.argv[1:]):
    spec = importlib.util.spec_from_file_location(f"zzc_utf8_{index}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.configure_utf8_stdio()
print("合并完成")
print("撤回完成", file=sys.stderr)
"""

        result = subprocess.run(
            [sys.executable, "-c", code, *(str(path) for path in scripts)],
            cwd=root,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        self.assertEqual(result.stdout.decode("utf-8").strip(), "合并完成")
        self.assertEqual(result.stderr.decode("utf-8").strip(), "撤回完成")

    def test_detects_generated_dictionary_drift(self) -> None:
        from tools import validate_repo

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tools_dir = root / "tools"
            tools_dir.mkdir()
            (root / "generated.dict.yaml").write_text("changed\n", encoding="utf-8")
            (tools_dir / "upstream_dictionaries.lock.json").write_text(
                '{"generated":{"generated.dict.yaml":{"sha256":"expected"}}}\n',
                encoding="utf-8",
            )
            errors: list[str] = []

            with patch.object(validate_repo, "ROOT", root):
                validate_repo.validate_generated_dictionaries(errors)

        self.assertEqual(
            errors,
            ["generated.dict.yaml: content differs from upstream dictionary lock"],
        )

    def test_scheduled_code_check_has_no_local_absolute_path(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github" / "workflows" / "check-txjx-upstream.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "tools/adapt_txjx_upstream.py --write --update-lock --json", workflow
        )
        self.assertIn("gh pr create", workflow)
        self.assertIn("steps.adapt.outputs.blocked == 'true'", workflow)
        self.assertIn("pixi run check", workflow)
        self.assertIn("pixi run lua tests/run.lua", workflow)
        self.assertNotIn("build_zzc_windows_exe.py", workflow)
        self.assertNotIn("D:\\", workflow)
        self.assertNotIn("D:/", workflow)

    def test_workflows_use_native_node24_actions(self) -> None:
        root = Path(__file__).resolve().parents[1]
        action_sources = [
            *sorted((root / ".github" / "workflows").glob("*.yml")),
            *sorted((root / ".github" / "actions").glob("*/action.yml")),
        ]
        workflows = "\n".join(
            path.read_text(encoding="utf-8")
            for path in action_sources
        )

        self.assertNotIn("FORCE_JAVASCRIPT_ACTIONS_TO_NODE24", workflows)
        for deprecated in (
            "actions/checkout@v4",
            "actions/setup-python@v5",
            "actions/upload-artifact@v4",
            "actions/github-script@v8",
        ):
            self.assertNotIn(deprecated, workflows)
        for native_node24 in (
            "actions/checkout@v7",
            "actions/setup-python@v7",
            "actions/cache@v6",
            "actions/upload-artifact@v7",
            "actions/download-artifact@v8",
            "actions/github-script@v9",
            "prefix-dev/setup-pixi@v0.10.0",
        ):
            self.assertIn(native_node24, workflows)

    def test_release_changelog_compares_against_triggering_commit(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github" / "workflows" / "create-release.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("head: context.sha", workflow)
        self.assertNotIn("head: 'main'", workflow)

    def test_release_changelog_survives_missing_previous_tag(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github" / "workflows" / "create-release.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("if (error.status !== 404) throw error", workflow)
        self.assertIn("Previous release tag is unavailable", workflow)

    def test_release_runs_twice_monthly_and_skips_unchanged_schedules(self) -> None:
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github" / "workflows" / "create-release.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn('cron: "17 4 1,15 * *"', workflow)
        self.assertIn("check_release_needed:", workflow)
        self.assertIn("context.eventName === 'workflow_dispatch'", workflow)
        self.assertIn("compare.data.ahead_by > 0", workflow)
        self.assertIn("needs: check_release_needed", workflow)
        self.assertIn(
            "if: needs.check_release_needed.outputs.should_release == 'true'",
            workflow,
        )

    def test_falls_back_to_lupa_when_luac_cannot_execute(self) -> None:
        from tools import validate_repo

        errors: list[str] = []
        with (
            patch.object(validate_repo.shutil, "which", return_value="luac.EXE"),
            patch.object(validate_repo.subprocess, "run", side_effect=PermissionError(5)),
            patch.object(
                validate_repo,
                "validate_lua_with_lupa",
                return_value="Lupa/Lua 5.5",
                create=True,
            ) as fallback,
        ):
            runtime = validate_repo.validate_lua_syntax(errors)

        self.assertEqual(runtime, "Lupa/Lua 5.5")
        self.assertEqual(errors, [])
        fallback.assert_called_once_with(errors)


if __name__ == "__main__":
    unittest.main()
