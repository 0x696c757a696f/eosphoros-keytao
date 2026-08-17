from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PlatformPackageTests(unittest.TestCase):
    def test_release_archives_use_balanced_deflate_level(self) -> None:
        from tools.build_platform_packages import DEFAULT_ZIP_COMPRESSLEVEL

        self.assertEqual(DEFAULT_ZIP_COMPRESSLEVEL, 6)

    def test_package_bases_can_be_split_between_parallel_jobs(self) -> None:
        from tools.build_platform_packages import PACKAGE_EXTRAS, package_files

        weasel_base = "eosphoros-weasel-windows-rime.zip"
        weasel = package_files(ROOT, only_base_names={weasel_base})
        native = package_files(ROOT, excluded_base_names={weasel_base})

        self.assertEqual(
            set(weasel),
            {
                "eosphoros-weasel-windows-rime-full.zip",
                "eosphoros-weasel-windows-rime-standard.zip",
                "eosphoros-weasel-windows-rime-lite.zip",
            },
        )
        self.assertTrue(set(weasel).isdisjoint(native))
        self.assertEqual(set(weasel) | set(native), set(PACKAGE_EXTRAS))

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
        from tools.build_platform_packages import (
            PACKAGE_EXTRAS,
            build_packages,
            package_profile,
        )
        from tools.dictionary_profiles import excluded_dictionaries

        with tempfile.TemporaryDirectory() as temp_dir:
            archives = build_packages(ROOT, Path(temp_dir), compresslevel=0)
            members = {}
            dictionary_indexes = {}
            for archive in archives:
                with zipfile.ZipFile(archive) as package:
                    members[archive.name] = set(package.namelist())
                    dictionary_indexes[archive.name] = package.read(
                        "eosphoros.extended.dict.yaml"
                    ).decode("utf-8")

        self.assertEqual(set(members), set(PACKAGE_EXTRAS))

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
        profile_exclusions = {
            name: set(excluded_dictionaries(package_profile(name)))
            for name in members
        }
        for name, files in members.items():
            excluded = profile_exclusions.get(name, set())
            self.assertTrue((common - excluded) <= files, name)
            self.assertTrue(excluded.isdisjoint(files), name)
            self.assertNotIn("zzc_state/runtime_ops.tsv", files, name)
            self.assertNotIn("tools/build_platform_packages.py", files, name)
            self.assertFalse(
                any(path.startswith("native/") for path in files),
                f"{name} must not contain the native Fcitx5 source tree",
            )

        shared_zzc = {path for path in common if path.startswith("zzc/")}
        expected_base_zzc = {
            "eosphoros-rime.zip": set(),
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
        def base_archive_name(name: str) -> str:
            profile = package_profile(name)
            return name.removesuffix(f"-{profile}.zip") + ".zip"

        for name, files in members.items():
            self.assertEqual(
                {path for path in files if path.startswith("zzc/")},
                shared_zzc | expected_base_zzc[base_archive_name(name)],
                name,
            )

        for core_name in (
            "eosphoros-rime-full.zip",
            "eosphoros-rime-standard.zip",
            "eosphoros-rime-lite.zip",
        ):
            core = members[core_name]
            for frontend_file in (
                "weasel.yaml",
                "squirrel.yaml",
                "Hamster.yaml",
                "zzc/Win_词库合并.exe",
            ):
                self.assertNotIn(frontend_file, core)

        for name, excluded in profile_exclusions.items():
            index = dictionary_indexes[name]
            for relative in excluded:
                import_name = relative.removesuffix(".dict.yaml")
                self.assertIn(
                    f"  - {import_name}\n",
                    dictionary_indexes["eosphoros-rime-full.zip"],
                    relative,
                )
                self.assertNotIn(f"  - {import_name}\n", index, name)

        weasel = members["eosphoros-weasel-windows-rime-full.zip"]
        self.assertIn("weasel.yaml", weasel)
        self.assertIn("weasel.custom.yaml", weasel)
        self.assertIn("eosphoros.ico", weasel)
        self.assertIn("eosphoros-ascii.ico", weasel)
        self.assertIn("zzc/Win_词库合并.exe", weasel)
        self.assertIn("zzc/Windows_词库合并.py", weasel)
        self.assertIn("zzc/Windows_撤回合并.py", weasel)
        self.assertNotIn("squirrel.yaml", weasel)
        self.assertNotIn("Hamster.yaml", weasel)

        squirrel = members["eosphoros-squirrel-macos-rime-full.zip"]
        self.assertIn("squirrel.yaml", squirrel)
        self.assertIn("squirrel.custom.yaml", squirrel)
        self.assertIn("zzc/Mac_词库合并", squirrel)
        self.assertNotIn("weasel.yaml", squirrel)
        self.assertNotIn("Hamster.yaml", squirrel)

        trime = members["eosphoros-trime-android-full.zip"]
        self.assertEqual(
            {path for path in trime if path.endswith(".trime.yaml")},
            {"eosphoros.trime.yaml"},
        )
        self.assertFalse(any(path.startswith("mobile_themes/") for path in trime))

        for name in (
            archive_name
            for archive_name in members
            if "eosphoros-fcitx5-" in archive_name and "-rime-" in archive_name
        ):
            package = members[name]
            self.assertIn("eosphoros.schema.yaml", package)
            self.assertTrue(any(path.startswith("dicts/eosphoros/") for path in package))
            self.assertTrue(any(path.startswith("lua/eosphoros/") for path in package))
            self.assertTrue(any(path.startswith("opencc/eosphoros/") for path in package))
            self.assertTrue(any(path.startswith("themes/") for path in package))
            self.assertFalse(any(path.startswith("fcitx5/") for path in package))
            self.assertFalse(any(path.startswith("mobile_themes/") for path in package))

        for name in (
            archive_name
            for archive_name in members
            if "yuanshu-ios-rime" in archive_name or "hamster-ios-rime" in archive_name
        ):
            mobile = members[name]
            self.assertIn("Hamster.yaml", mobile)
            self.assertIn("include_iCloud_rime_files.txt", mobile)
            self.assertIn("include_keyboard_rime_files.txt", mobile)
            self.assertIn("zzc/iOS_词库合并.py", mobile)
            self.assertNotIn("weasel.yaml", mobile)
            self.assertNotIn("squirrel.yaml", mobile)
            self.assertNotIn("zzc/Win_词库合并.exe", mobile)

        for name in members:
            self.assertFalse(
                any(path.startswith("fcitx5/") for path in members[name]), name
            )

    def test_master_combined_artifact_excludes_native_build_sources(self) -> None:
        workflow = (ROOT / ".github/workflows/package-master.yml").read_text(
            encoding="utf-8"
        )
        artifact_block = workflow.split("name: eosphoros", 1)[1]
        self.assertIn("!native/**", artifact_block)
        self.assertIn("!packaging/fcitx5/**", artifact_block)
        self.assertNotIn("!fcitx5/**", artifact_block)
        self.assertNotIn("!eosphoros-fcitx5-*.zip", artifact_block)

    def test_master_builds_real_official_table_packages(self) -> None:
        workflow = (ROOT / ".github/workflows/package-master.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("libime-bin", workflow)
        self.assertIn("pixi run python tools/build_fcitx5_table.py", workflow)
        self.assertIn('--compiler "$(command -v libime_tabledict)"', workflow)
        for platform in ("linux", "macos", "android"):
            self.assertNotIn(f"name: eosphoros-fcitx5-{platform}", workflow)
        self.assertIn("name: Upload complete build", workflow)
        self.assertEqual(workflow.count("actions/upload-artifact@"), 1)


if __name__ == "__main__":
    unittest.main()
