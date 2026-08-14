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
            archives = build_packages(ROOT, Path(temp_dir), compresslevel=0)
            members = {}
            for archive in archives:
                with zipfile.ZipFile(archive) as package:
                    members[archive.name] = set(package.namelist())

        self.assertEqual(
            set(members),
            {
                "eosphoros-rime-cross-platform.zip",
                "eosphoros-weasel-windows-rime.zip",
                "eosphoros-squirrel-macos-rime.zip",
                "eosphoros-fcitx5-macos-rime.zip",
                "eosphoros-fcitx5-linux-rime.zip",
                "eosphoros-trime-android.zip",
                "eosphoros-fcitx5-android-rime.zip",
                "eosphoros-yuanshu-ios-rime.zip",
                "eosphoros-hamster-ios-rime.zip",
            },
        )

        common = {
            "default.yaml",
            "default.custom.yaml",
            "eosphoros.schema.yaml",
            "eosphoros.ico",
            "eosphoros-ascii.ico",
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
            self.assertFalse(
                any(path.startswith("native/") for path in files),
                f"{name} must not contain the native Fcitx5 source tree",
            )

        shared_zzc = {path for path in common if path.startswith("zzc/")}
        expected_platform_zzc = {
            "eosphoros-rime-cross-platform.zip": set(),
            "eosphoros-weasel-windows-rime.zip": {
                "zzc/Win_词库合并.exe",
                "zzc/Win_撤回合并.exe",
                "zzc/Windows_词库合并.py",
                "zzc/Windows_撤回合并.py",
            },
            "eosphoros-squirrel-macos-rime.zip": {
                "zzc/Mac_词库合并",
                "zzc/Mac_撤回合并",
            },
            "eosphoros-fcitx5-macos-rime.zip": set(),
            "eosphoros-fcitx5-linux-rime.zip": set(),
            "eosphoros-trime-android.zip": set(),
            "eosphoros-fcitx5-android-rime.zip": set(),
            "eosphoros-yuanshu-ios-rime.zip": {
                "zzc/iOS_词库合并.py",
                "zzc/iOS快捷指令合并说明.md",
                "zzc/a-Shell快捷指令合并说明.md",
            },
            "eosphoros-hamster-ios-rime.zip": {
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

        core = members["eosphoros-rime-cross-platform.zip"]
        for frontend_file in (
            "weasel.yaml",
            "squirrel.yaml",
            "Hamster.yaml",
            "zzc/Win_词库合并.exe",
        ):
            self.assertNotIn(frontend_file, core)

        weasel = members["eosphoros-weasel-windows-rime.zip"]
        self.assertIn("weasel.yaml", weasel)
        self.assertIn("weasel.custom.yaml", weasel)
        self.assertIn("eosphoros.ico", weasel)
        self.assertIn("eosphoros-ascii.ico", weasel)
        self.assertIn("zzc/Win_词库合并.exe", weasel)
        self.assertIn("zzc/Windows_词库合并.py", weasel)
        self.assertIn("zzc/Windows_撤回合并.py", weasel)
        self.assertNotIn("squirrel.yaml", weasel)
        self.assertNotIn("Hamster.yaml", weasel)

        squirrel = members["eosphoros-squirrel-macos-rime.zip"]
        self.assertIn("squirrel.yaml", squirrel)
        self.assertIn("squirrel.custom.yaml", squirrel)
        self.assertIn("zzc/Mac_词库合并", squirrel)
        self.assertNotIn("weasel.yaml", squirrel)
        self.assertNotIn("Hamster.yaml", squirrel)

        trime = members["eosphoros-trime-android.zip"]
        self.assertEqual(
            {path for path in trime if path.endswith(".trime.yaml")},
            {"eosphoros.trime.yaml"},
        )
        self.assertFalse(any(path.startswith("mobile_themes/") for path in trime))

        for name in (
            "eosphoros-fcitx5-macos-rime.zip",
            "eosphoros-fcitx5-linux-rime.zip",
            "eosphoros-fcitx5-android-rime.zip",
        ):
            package = members[name]
            self.assertIn("eosphoros.schema.yaml", package)
            self.assertTrue(any(path.startswith("dicts/eosphoros/") for path in package))
            self.assertTrue(any(path.startswith("lua/eosphoros/") for path in package))
            self.assertTrue(any(path.startswith("opencc/eosphoros/") for path in package))
            self.assertTrue(any(path.startswith("themes/") for path in package))
            self.assertFalse(any(path.startswith("fcitx5/") for path in package))
            self.assertFalse(any(path.startswith("mobile_themes/") for path in package))

        for name in ("eosphoros-yuanshu-ios-rime.zip", "eosphoros-hamster-ios-rime.zip"):
            mobile = members[name]
            self.assertIn("Hamster.yaml", mobile)
            self.assertIn("include_iCloud_rime_files.txt", mobile)
            self.assertIn("include_keyboard_rime_files.txt", mobile)
            self.assertIn("zzc/iOS_词库合并.py", mobile)
            self.assertNotIn("weasel.yaml", mobile)
            self.assertNotIn("squirrel.yaml", mobile)
            self.assertNotIn("zzc/Win_词库合并.exe", mobile)

        for name in (
            "eosphoros-rime-cross-platform.zip",
            "eosphoros-weasel-windows-rime.zip",
            "eosphoros-squirrel-macos-rime.zip",
            "eosphoros-fcitx5-macos-rime.zip",
            "eosphoros-fcitx5-linux-rime.zip",
            "eosphoros-fcitx5-android-rime.zip",
            "eosphoros-trime-android.zip",
            "eosphoros-yuanshu-ios-rime.zip",
            "eosphoros-hamster-ios-rime.zip",
        ):
            self.assertFalse(
                any(path.startswith("fcitx5/") for path in members[name]), name
            )

    def test_master_rime_artifact_excludes_native_fcitx5_sources(self) -> None:
        workflow = (ROOT / ".github/workflows/package-master.yml").read_text(
            encoding="utf-8"
        )
        artifact_block = workflow.split("name: eosphoros", 1)[1]
        self.assertIn("!native/**", artifact_block)
        self.assertIn("!fcitx5/**", artifact_block)
        self.assertIn("!packaging/fcitx5/**", artifact_block)
        self.assertIn("!eosphoros-fcitx5-*.zip", artifact_block)

    def test_master_builds_real_official_table_packages(self) -> None:
        workflow = (ROOT / ".github/workflows/package-master.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("libime-bin", workflow)
        self.assertIn(
            'python tools/build_fcitx5_table.py --compiler "$(command -v libime_tabledict)"',
            workflow,
        )
        for platform in ("linux", "macos", "android"):
            self.assertIn(f"name: eosphoros-fcitx5-{platform}", workflow)
            self.assertIn(f"path: eosphoros-fcitx5-{platform}.zip", workflow)


if __name__ == "__main__":
    unittest.main()
