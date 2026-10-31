from __future__ import annotations

import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DICT_DIR = ROOT / "dicts" / "eosphoros"
TARGET = DICT_DIR / "eosphoros.bible.dict.yaml"


def plain(word: str) -> str:
    """只差间隔号「·」的视为同一个词。"""
    return word.replace("·", "")


class BibleTermsTests(unittest.TestCase):
    def test_dictionary_matches_generator(self) -> None:
        from tools.build_bible_terms import expected_dictionary_text

        expected, _ = expected_dictionary_text(ROOT)
        actual = TARGET.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        self.assertEqual(actual, expected)

    def test_no_word_duplicates_another_dictionary(self) -> None:
        from tools.eosphoros_codes import iter_dictionary_rows

        others = {
            plain(word)
            for path in DICT_DIR.glob("*.dict.yaml")
            if path != TARGET
            for word, _ in iter_dictionary_rows(path)
        }
        actual = [plain(word) for word, _ in iter_dictionary_rows(TARGET)]
        self.assertEqual(len(actual), len(set(actual)), "duplicate words in the dictionary")
        self.assertEqual(sorted(set(actual) & others), [])

    def test_adds_no_code_collisions(self) -> None:
        from tools.eosphoros_codes import iter_dictionary_rows

        # 与固定本地词典和本词典内部都不重码；ICE 与万象会围绕本地词典重建
        occupied: dict[str, set[str]] = defaultdict(set)
        for path in DICT_DIR.glob("*.dict.yaml"):
            if path.name == "eosphoros.ice.dict.yaml" or ".wanxiang." in path.name:
                continue
            for word, code in iter_dictionary_rows(path):
                occupied[code].add(plain(word))
        collisions = {
            code: sorted(occupied[code])
            for word, code in iter_dictionary_rows(TARGET)
            if len(occupied[code]) > 1
        }
        self.assertEqual(collisions, {})


if __name__ == "__main__":
    unittest.main()
