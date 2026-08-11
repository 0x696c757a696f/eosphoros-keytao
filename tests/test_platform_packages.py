from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PlatformPackageTests(unittest.TestCase):
    def test_rime_smoke_test_requires_compiled_core_artifacts(self) -> None:
        from tools.smoke_test_rime_deployment import (
            REQUIRED_BUILD_OUTPUTS,
            deployer_command,
            validate_outputs,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            build = root / "build"
            build.mkdir()
            for name in REQUIRED_BUILD_OUTPUTS[:-1]:
                output = build / name
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(b"test")
            self.assertEqual(validate_outputs(root), [REQUIRED_BUILD_OUTPUTS[-1]])
            (build / REQUIRED_BUILD_OUTPUTS[-1]).write_bytes(b"test")
            self.assertEqual(validate_outputs(root), [])
            shared_data = Path("/usr/share/rime-data")
            self.assertEqual(
                deployer_command("rime_deployer", root, shared_data),
                [
                    "rime_deployer",
                    "--build",
                    str(root),
                    str(shared_data),
                ],
            )

    def test_builds_minimal_core_and_platform_archives(self) -> None:
        from tools.build_platform_packages import build_packages

        with tempfile.TemporaryDirectory() as temp_dir:
            archives = build_packages(ROOT, Path(temp_dir))
            members = {}
            for archive in archives:
                with zipfile.ZipFile(archive) as package:
                    members[archive.name] = set(package.namelist())

        self.assertEqual(
            set(members),
            {
                "eosphoros.zip",
                "eosphoros-weasel.zip",
                "eosphoros-squirrel.zip",
                "eosphoros-fcitx5-macos.zip",
                "eosphoros-fcitx5-linux.zip",
                "eosphoros-trime.zip",
                "eosphoros-fcitx5-android.zip",
                "eosphoros-yuanshu.zip",
                "eosphoros-hamster.zip",
            },
        )

        common = {
            "default.yaml",
            "default.custom.yaml",
            "eosphoros.schema.yaml",
            "eosphoros.cx.schema.yaml",
            "eosphoros.gbk.schema.yaml",
            "liangfen.schema.yaml",
            "pinyin_simp.schema.yaml",
            "eosphoros.cx.dict.yaml",
            "eosphoros.gbk.dict.yaml",
            "liangfen.dict.yaml",
            "pinyin_simp.dict.yaml",
            "dicts/eosphoros/eosphoros.danzi.dict.yaml",
            "dicts/eosphoros/eosphoros.wanxiang.yaopin.dict.yaml",
            "lua/eosphoros/eosphoros_core.lua",
            "opencc/eosphoros/eosphoros_emoji_chars.lua",
            "zzc_state/char_parts.tsv",
            "README.md",
            "THIRD_PARTY.md",
            "LICENSE.md",
            "CONTRIBUTING.md",
            "VERSION",
            "zzc/README.md",
            "zzc/自造词使用教程.md",
            "zzc/自造词使用教程.png",
            "zzc/eosphoros_词库合并.py",
            "zzc/eosphoros_撤回合并.py",
            "licenses/rime-ice-GPL-3.0.txt",
        }
        for name, files in members.items():
            self.assertTrue(common <= files, name)
            self.assertNotIn("zzc_state/runtime_ops.tsv", files, name)
            self.assertNotIn("tools/build_platform_packages.py", files, name)

        shared_zzc = {path for path in common if path.startswith("zzc/")}
        expected_platform_zzc = {
            "eosphoros.zip": set(),
            "eosphoros-weasel.zip": {
                "zzc/Win_词库合并.exe",
                "zzc/Win_撤回合并.exe",
                "zzc/Windows_词库合并.py",
                "zzc/Windows_撤回合并.py",
            },
            "eosphoros-squirrel.zip": {
                "zzc/Mac_词库合并",
                "zzc/Mac_撤回合并",
            },
            "eosphoros-fcitx5-macos.zip": {
                "zzc/Fcitx5_macOS_词库合并.py",
                "zzc/Fcitx5_macOS_撤回合并.py",
            },
            "eosphoros-fcitx5-linux.zip": {
                "zzc/Fcitx5_Linux_词库合并.py",
                "zzc/Fcitx5_Linux_撤回合并.py",
            },
            "eosphoros-trime.zip": set(),
            "eosphoros-fcitx5-android.zip": set(),
            "eosphoros-yuanshu.zip": {
                "zzc/iOS_词库合并.py",
                "zzc/iOS快捷指令合并说明.md",
                "zzc/a-Shell快捷指令合并说明.md",
            },
            "eosphoros-hamster.zip": {
                "zzc/iOS_词库合并.py",
                "zzc/iOS快捷指令合并说明.md",
                "zzc/a-Shell快捷指令合并说明.md",
            },
        }
        for name, files in members.items():
            self.assertEqual(
                {path for path in files if path.startswith("zzc/")},
                shared_zzc | expected_platform_zzc[name],
                name,
            )

        core = members["eosphoros.zip"]
        for frontend_file in (
            "weasel.yaml",
            "squirrel.yaml",
            "Hamster.yaml",
            "zzc/Win_词库合并.exe",
        ):
            self.assertNotIn(frontend_file, core)

        weasel = members["eosphoros-weasel.zip"]
        self.assertIn("weasel.yaml", weasel)
        self.assertIn("weasel.custom.yaml", weasel)
        self.assertIn("eosphoros.ico", weasel)
        self.assertIn("zzc/Win_词库合并.exe", weasel)
        self.assertIn("zzc/Windows_词库合并.py", weasel)
        self.assertIn("zzc/Windows_撤回合并.py", weasel)
        self.assertNotIn("squirrel.yaml", weasel)
        self.assertNotIn("Hamster.yaml", weasel)

        squirrel = members["eosphoros-squirrel.zip"]
        self.assertIn("squirrel.yaml", squirrel)
        self.assertIn("squirrel.custom.yaml", squirrel)
        self.assertIn("zzc/Mac_词库合并", squirrel)
        self.assertNotIn("weasel.yaml", squirrel)
        self.assertNotIn("Hamster.yaml", squirrel)

        fcitx5_macos = members["eosphoros-fcitx5-macos.zip"]
        self.assertIn("zzc/Fcitx5_macOS_词库合并.py", fcitx5_macos)
        self.assertIn("zzc/Fcitx5_macOS_撤回合并.py", fcitx5_macos)
        self.assertIn("fcitx5/macos/themes/eosphoros-auto.conf", fcitx5_macos)
        self.assertNotIn(
            "fcitx5/linux/themes/eosphoros-light/theme.conf", fcitx5_macos
        )
        self.assertNotIn("weasel.yaml", fcitx5_macos)
        self.assertNotIn("squirrel.yaml", fcitx5_macos)
        self.assertNotIn("Hamster.yaml", fcitx5_macos)

        fcitx5_linux = members["eosphoros-fcitx5-linux.zip"]
        self.assertIn("zzc/eosphoros_词库合并.py", fcitx5_linux)
        self.assertIn("zzc/Fcitx5_Linux_词库合并.py", fcitx5_linux)
        self.assertIn("zzc/Fcitx5_Linux_撤回合并.py", fcitx5_linux)
        self.assertIn(
            "fcitx5/linux/themes/eosphoros-light/theme.conf", fcitx5_linux
        )
        self.assertNotIn("fcitx5/macos/themes/eosphoros-auto.conf", fcitx5_linux)
        self.assertNotIn("zzc/Fcitx5_macOS_词库合并.py", fcitx5_linux)
        self.assertNotIn("weasel.yaml", fcitx5_linux)
        self.assertNotIn("squirrel.yaml", fcitx5_linux)
        self.assertNotIn("Hamster.yaml", fcitx5_linux)

        trime = members["eosphoros-trime.zip"]
        self.assertIn("eosphoros.trime.yaml", trime)
        self.assertFalse(any(path.startswith("mobile_themes/") for path in trime))

        fcitx5_android = members["eosphoros-fcitx5-android.zip"]
        self.assertEqual(
            {path for path in fcitx5_android if path.startswith("themes/")},
            {
                "themes/eosphoros-dawn.zip",
                "themes/eosphoros-night.zip",
                "themes/eosphoros-mono.zip",
            },
        )

        for name in ("eosphoros-yuanshu.zip", "eosphoros-hamster.zip"):
            mobile = members[name]
            self.assertIn("Hamster.yaml", mobile)
            self.assertIn("include_iCloud_rime_files.txt", mobile)
            self.assertIn("include_keyboard_rime_files.txt", mobile)
            self.assertIn("zzc/iOS_词库合并.py", mobile)
            self.assertNotIn("weasel.yaml", mobile)
            self.assertNotIn("squirrel.yaml", mobile)
            self.assertNotIn("zzc/Win_词库合并.exe", mobile)

        for name in (
            "eosphoros.zip",
            "eosphoros-weasel.zip",
            "eosphoros-squirrel.zip",
            "eosphoros-trime.zip",
            "eosphoros-yuanshu.zip",
            "eosphoros-hamster.zip",
        ):
            self.assertFalse(
                any(path.startswith("fcitx5/") for path in members[name]), name
            )


if __name__ == "__main__":
    unittest.main()
