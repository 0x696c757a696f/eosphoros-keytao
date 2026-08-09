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
            "licenses/rime-ice-GPL-3.0.txt",
        }
        for name, files in members.items():
            self.assertTrue(common <= files, name)
            self.assertNotIn("zzc_state/runtime_ops.tsv", files, name)
            self.assertNotIn("tools/build_platform_packages.py", files, name)

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
        self.assertNotIn("squirrel.yaml", weasel)
        self.assertNotIn("Hamster.yaml", weasel)
        self.assertNotIn("zzc/Linux_词库合并.py", weasel)

        squirrel = members["xmjd6-squirrel.zip"]
        self.assertIn("squirrel.yaml", squirrel)
        self.assertIn("squirrel.custom.yaml", squirrel)
        self.assertIn("zzc/Mac_词库合并", squirrel)
        self.assertNotIn("weasel.yaml", squirrel)
        self.assertNotIn("Hamster.yaml", squirrel)

        fcitx5_macos = members["xmjd6-fcitx5-macos.zip"]
        self.assertIn("zzc/Mac_词库合并", fcitx5_macos)
        self.assertNotIn("weasel.yaml", fcitx5_macos)
        self.assertNotIn("squirrel.yaml", fcitx5_macos)
        self.assertNotIn("Hamster.yaml", fcitx5_macos)

        fcitx5_linux = members["xmjd6-fcitx5-linux.zip"]
        self.assertIn("zzc/Linux_词库合并.py", fcitx5_linux)
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


if __name__ == "__main__":
    unittest.main()
