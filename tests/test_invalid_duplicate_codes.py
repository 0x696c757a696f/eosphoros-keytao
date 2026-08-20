from __future__ import annotations

import unittest
from pathlib import Path

from tools.clean_invalid_duplicate_codes import plan_removals


ROOT = Path(__file__).resolve().parents[1]


class InvalidDuplicateCodeTests(unittest.TestCase):
    def test_no_invalid_duplicate_code_rows_remain(self) -> None:
        self.assertEqual(plan_removals(ROOT), ())


if __name__ == "__main__":
    unittest.main()
