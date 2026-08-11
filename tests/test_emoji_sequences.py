from __future__ import annotations

import unittest

from tools.validate_emoji_sequences import sequence_errors, validate_repository


class EmojiSequenceTests(unittest.TestCase):
    def test_accepts_well_formed_emoji_sequences(self) -> None:
        for value in (
            "0⃣ 1️⃣",
            "👨‍👩‍👧‍👦",
            "🧚🏻‍♀",
            "🏻 🏼 🏽 🏾 🏿",
            "🇨🇳 🇩🇪",
            "🏴\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f",
        ):
            self.assertEqual(sequence_errors(value), [], value)

    def test_rejects_broken_emoji_control_sequences(self) -> None:
        invalid = {
            "‍👩": "orphan or repeated ZWJ",
            "️😀": "orphan or repeated variation selector",
            "A⃣": "keycap mark without #, *, or digit base",
            "🇨": "unpaired regional-indicator flag code point",
        }
        for value, expected in invalid.items():
            self.assertIn(expected, sequence_errors(value), value)

    def test_repository_emoji_tables_are_structurally_valid(self) -> None:
        self.assertEqual(validate_repository(), [])


if __name__ == "__main__":
    unittest.main()
