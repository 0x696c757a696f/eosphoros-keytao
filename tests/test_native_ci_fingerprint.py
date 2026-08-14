from __future__ import annotations

import unittest

from tools.native_ci_fingerprint import affects_native_packages


class NativeCiFingerprintTests(unittest.TestCase):
    def test_excludes_only_non_build_inputs(self) -> None:
        for path in (
            "README.md",
            "docs/release.md",
            "tests/test_tools.py",
            ".github/ISSUE_TEMPLATE/deployment.yml",
        ):
            self.assertFalse(affects_native_packages(path), path)

        for path in (
            "eosphoros.schema.yaml",
            "dicts/eosphoros/eosphoros.core.dict.yaml",
            "tools/build_fcitx5_table.py",
            ".github/workflows/package-master.yml",
            ".github/actions/fetch-opencc/action.yml",
            "pixi.lock",
        ):
            self.assertTrue(affects_native_packages(path), path)


if __name__ == "__main__":
    unittest.main()
