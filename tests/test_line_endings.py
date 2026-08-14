from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LineEndingTests(unittest.TestCase):
    def test_normalizer_converts_crlf_and_lone_cr_to_lf(self) -> None:
        from tools.normalize_line_endings import normalize_lf

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "input.txt"
            path.write_bytes(b"first\r\nsecond\rthird\n")
            self.assertTrue(normalize_lf(path))
            self.assertEqual(path.read_bytes(), b"first\nsecond\nthird\n")
            self.assertFalse(normalize_lf(path))

    def test_auto_detected_binary_files_are_excluded(self) -> None:
        from tools.normalize_line_endings import requires_lf

        self.assertFalse(requires_lf(b"i/-text w/-text attr/text=auto eol=lf"))
        self.assertTrue(requires_lf(b"i/lf w/crlf attr/text eol=lf"))

    def test_repository_tracked_text_files_use_lf(self) -> None:
        from tools.normalize_line_endings import non_lf_paths

        self.assertEqual(non_lf_paths(ROOT), [])
