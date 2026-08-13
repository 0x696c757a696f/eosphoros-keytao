from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Fcitx5TableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from tools.build_fcitx5_table import collect_entries

        cls.entries = collect_entries(ROOT)

    def test_main_table_is_complete_deduplicated_and_six_keys(self) -> None:
        rows = [(entry.code, entry.text) for entry in self.entries]
        self.assertGreater(len(rows), 1_000_000)
        self.assertEqual(len(rows), len(set(rows)))
        self.assertTrue(all(1 <= len(code) <= 6 for code, _ in rows))
        self.assertIn(("jxjdoo", "晨星键道"), rows)
        self.assertIn(("hyefa", "婚姻圣召"), rows)
        self.assertIn(("zqquo", "赞主曲"), rows)

    def test_config_uses_only_builtin_table_and_stable_order(self) -> None:
        from tools.build_fcitx5_table import render_config

        config = render_config()
        self.assertIn("Addon=table", config)
        self.assertIn("NoMatchAutoSelectLength=1", config)
        self.assertIn("AutoSelectLength=-1", config)
        self.assertIn("OrderPolicy=No", config)
        self.assertIn("UseContextRelatedOrder=False", config)
        self.assertIn("Learning=True", config)
        self.assertNotIn("rime", config.lower())
        self.assertNotIn("lua", config.lower())

    def test_fixed_topup_conflicts_are_explicitly_bounded(self) -> None:
        # Fcitx5 NoMatchAutoSelect reproduces all fixed topup transitions except
        # the rare case where the pressed key is also a valid longer prefix.
        # Keep this measured boundary small and visible instead of claiming
        # byte-for-byte equivalence with the Rime/Yong processor.
        from tools.build_fcitx5_table import KEY_CODE

        codes = {entry.code for entry in self.entries}
        prefixes = {code[:length] for code in codes for length in range(1, len(code) + 1)}
        topup_keys = set("avuio;")
        conflicts: list[tuple[str, str]] = []
        for code in codes:
            if len(code) >= 6:
                continue
            for key in KEY_CODE:
                fixed = (
                    (code[-1] in topup_keys and key not in topup_keys)
                    or (len(code) >= 4 and code[-1] not in topup_keys and key not in topup_keys)
                )
                if fixed and code + key in prefixes:
                    conflicts.append((code, key))
        self.assertLessEqual(len(conflicts), 50)

    def test_platform_archives_are_table_only_and_separated(self) -> None:
        from tools.build_fcitx5_table import build_packages

        with tempfile.TemporaryDirectory() as temp_dir:
            archives = build_packages(
                ROOT, Path(temp_dir), compiled_dictionary=b"LIBIME-DICT-TEST"
            )
            members = {}
            for archive in archives:
                with zipfile.ZipFile(archive) as package:
                    members[archive.name] = set(package.namelist())

        linux = members["eosphoros-fcitx5-linux.zip"]
        self.assertIn("inputmethod/eosphoros.conf", linux)
        self.assertIn("table/eosphoros.main.dict", linux)
        self.assertTrue(any(path.startswith("themes/") for path in linux))

        macos = members["eosphoros-fcitx5-macos.zip"]
        android = members["eosphoros-fcitx5-android.zip"]
        for platform in (macos, android):
            self.assertIn("eosphoros.conf", platform)
            self.assertIn("eosphoros.txt", platform)
            self.assertFalse(any(path.endswith(".schema.yaml") for path in platform))
            self.assertFalse(any(path.startswith("lua/") for path in platform))
            self.assertFalse(any(path.startswith("opencc/") for path in platform))
        self.assertIn("themes/eosphoros-auto.conf", macos)
        self.assertEqual(android, {"eosphoros.conf", "eosphoros.txt"})
        self.assertFalse(any("macos" in path.lower() for path in android))
        for package in members.values():
            self.assertFalse(any(path.startswith("fcitx5/") for path in package))
            self.assertFalse(any(path.startswith("mobile_themes/") for path in package))


if __name__ == "__main__":
    unittest.main()
