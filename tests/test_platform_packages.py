from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PlatformPackageTests(unittest.TestCase):
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
                "xmjd6.zip",
                "xmjd6-weasel.zip",
                "xmjd6-squirrel.zip",
                "xmjd6-fcitx5-macos.zip",
                "xmjd6-fcitx5-linux.zip",
                "xmjd6-mobile.zip",
            },
        )

        common = {
            "default.yaml",
            "default.custom.yaml",
            "xmjd6.schema.yaml",
            "xmjd6.danzi.dict.yaml",
            "lua/xmjd6/xmjd6_core.lua",
            "opencc/xmjd6/xmjd6_emoji_chars.lua",
            "zzc_state/char_parts.tsv",
            "README.md",
            "THIRD_PARTY.md",
            "VERSION",
            "zzc/README.md",
            "zzc/自造词使用教程.md",
            "zzc/自造词使用教程.png",
            "zzc/xmjd6_词库合并.py",
            "zzc/xmjd6_撤回合并.py",
            "licenses/rime-ice-GPL-3.0.txt",
        }
        for name, files in members.items():
            self.assertTrue(common <= files, name)
            self.assertNotIn("zzc_state/runtime_ops.tsv", files, name)
            self.assertNotIn("tools/build_platform_packages.py", files, name)

        shared_zzc = {path for path in common if path.startswith("zzc/")}
        expected_platform_zzc = {
            "xmjd6.zip": set(),
            "xmjd6-weasel.zip": {
                "zzc/Win_词库合并.exe",
                "zzc/Win_撤回合并.exe",
                "zzc/Windows_词库合并.py",
                "zzc/Windows_撤回合并.py",
            },
            "xmjd6-squirrel.zip": {
                "zzc/Mac_词库合并",
                "zzc/Mac_撤回合并",
            },
            "xmjd6-fcitx5-macos.zip": {
                "zzc/Fcitx5_macOS_词库合并.py",
                "zzc/Fcitx5_macOS_撤回合并.py",
            },
            "xmjd6-fcitx5-linux.zip": {
                "zzc/Fcitx5_Linux_词库合并.py",
                "zzc/Fcitx5_Linux_撤回合并.py",
            },
            "xmjd6-mobile.zip": {
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

        core = members["xmjd6.zip"]
        for frontend_file in (
            "weasel.yaml",
            "squirrel.yaml",
            "Hamster.yaml",
            "zzc/Win_词库合并.exe",
        ):
            self.assertNotIn(frontend_file, core)

        weasel = members["xmjd6-weasel.zip"]
        self.assertIn("weasel.yaml", weasel)
        self.assertIn("weasel.custom.yaml", weasel)
        self.assertIn("xmjd6.ico", weasel)
        self.assertIn("zzc/Win_词库合并.exe", weasel)
        self.assertIn("zzc/Windows_词库合并.py", weasel)
        self.assertIn("zzc/Windows_撤回合并.py", weasel)
        self.assertNotIn("squirrel.yaml", weasel)
        self.assertNotIn("Hamster.yaml", weasel)

        squirrel = members["xmjd6-squirrel.zip"]
        self.assertIn("squirrel.yaml", squirrel)
        self.assertIn("squirrel.custom.yaml", squirrel)
        self.assertIn("zzc/Mac_词库合并", squirrel)
        self.assertNotIn("weasel.yaml", squirrel)
        self.assertNotIn("Hamster.yaml", squirrel)

        fcitx5_macos = members["xmjd6-fcitx5-macos.zip"]
        self.assertIn("zzc/Fcitx5_macOS_词库合并.py", fcitx5_macos)
        self.assertIn("zzc/Fcitx5_macOS_撤回合并.py", fcitx5_macos)
        self.assertIn("fcitx5/macos/themes/xmjd6-auto.conf", fcitx5_macos)
        self.assertNotIn(
            "fcitx5/linux/themes/xmjd6-CatLight/theme.conf", fcitx5_macos
        )
        self.assertNotIn("weasel.yaml", fcitx5_macos)
        self.assertNotIn("squirrel.yaml", fcitx5_macos)
        self.assertNotIn("Hamster.yaml", fcitx5_macos)

        fcitx5_linux = members["xmjd6-fcitx5-linux.zip"]
        self.assertIn("zzc/xmjd6_词库合并.py", fcitx5_linux)
        self.assertIn("zzc/Fcitx5_Linux_词库合并.py", fcitx5_linux)
        self.assertIn("zzc/Fcitx5_Linux_撤回合并.py", fcitx5_linux)
        self.assertIn(
            "fcitx5/linux/themes/xmjd6-CatLight/theme.conf", fcitx5_linux
        )
        self.assertNotIn("fcitx5/macos/themes/xmjd6-auto.conf", fcitx5_linux)
        self.assertNotIn("zzc/Fcitx5_macOS_词库合并.py", fcitx5_linux)
        self.assertNotIn("weasel.yaml", fcitx5_linux)
        self.assertNotIn("squirrel.yaml", fcitx5_linux)
        self.assertNotIn("Hamster.yaml", fcitx5_linux)

        mobile = members["xmjd6-mobile.zip"]
        self.assertIn("Hamster.yaml", mobile)
        self.assertIn("include_iCloud_rime_files.txt", mobile)
        self.assertIn("include_keyboard_rime_files.txt", mobile)
        self.assertIn("zzc/iOS_词库合并.py", mobile)
        self.assertNotIn("weasel.yaml", mobile)
        self.assertNotIn("squirrel.yaml", mobile)
        self.assertNotIn("zzc/Win_词库合并.exe", mobile)

        for name in (
            "xmjd6.zip",
            "xmjd6-weasel.zip",
            "xmjd6-squirrel.zip",
            "xmjd6-mobile.zip",
        ):
            self.assertFalse(
                any(path.startswith("fcitx5/") for path in members[name]), name
            )


if __name__ == "__main__":
    unittest.main()
