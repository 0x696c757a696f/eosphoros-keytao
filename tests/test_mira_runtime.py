from __future__ import annotations

import re
import unittest
from pathlib import Path

from tools.update_mira_checksums import load_lock


ROOT = Path(__file__).resolve().parents[1]


class MiraRuntimeLockTests(unittest.TestCase):
    def test_package_matrix_binaries_are_pinned_in_lock(self) -> None:
        workflow = (ROOT / ".github/workflows/package-master.yml").read_text(encoding="utf-8")
        binaries = set(re.findall(r"^\s*binary:\s*(\S+)\s*$", workflow, re.MULTILINE))
        lock = load_lock()
        self.assertEqual(binaries, set(lock["binaries"]))
        for checksum in lock["binaries"].values():
            self.assertRegex(checksum, r"^[0-9a-f]{64}$")
        self.assertIn("tools/mira_runtime.lock.json", workflow)
        self.assertIn("sha256sum --check --strict", workflow)

    def test_sync_workflow_tests_new_binaries_before_opening_pr(self) -> None:
        workflow = (ROOT / ".github/workflows/sync-mira-runtime.yml").read_text(encoding="utf-8")
        self.assertLess(
            workflow.index("tests/eosphoros.mira.test.yaml"),
            workflow.index("gh pr create"),
        )
        self.assertIn("git add -- tools/mira_runtime.lock.json", workflow)


if __name__ == "__main__":
    unittest.main()
