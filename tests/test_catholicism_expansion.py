from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CatholicismExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from tools.build_catholicism_expansion import expected_dictionary_text

        cls.expected, cls.result = expected_dictionary_text(ROOT)

    def test_builds_a_large_expansion_without_unreviewed_collisions(self) -> None:
        result = self.result
        words = {entry.word for entry in result.entries}
        codes = [entry.code for entry in result.entries]

        self.assertGreaterEqual(len(result.entries), 220)
        self.assertEqual(len(codes), len(set(codes)))
        self.assertTrue(
            {
                "圣道礼仪",
                "圣体游行",
                "宗座代牧区",
                "宗座圣轮法院",
                "至圣三位",
                "逾越三日庆典",
                "信仰不同的婚姻",
            }.issubset(words)
        )
        self.assertFalse(result.collisions)
        self.assertEqual(
            result.allowed_collisions,
            (("婚姻圣召", "hyefa", ("洪山",)),),
        )

        codes_by_word = {entry.word: entry.code for entry in result.entries}
        self.assertEqual(codes_by_word["婚姻圣召"], "hyefa")
        self.assertEqual(codes_by_word["赞主曲"], "zqquo")

    def test_renders_a_visible_divider_before_dictionary_rows(self) -> None:
        from tools.build_catholicism_expansion import render_section

        section = render_section(self.result.entries)
        divider = section.index("# 2026-08-04 天主教词汇扩建")
        first_row = next(
            index
            for index, line in enumerate(section.splitlines())
            if line and not line.startswith("#") and "\t" in line
        )

        self.assertEqual(divider, 0)
        self.assertGreater(first_row, 2)

    def test_committed_expansion_is_current(self) -> None:
        actual = (ROOT / "dicts" / "eosphoros" / "eosphoros.catholicism.dict.yaml").read_text(
            encoding="utf-8-sig"
        ).replace("\r\n", "\n")

        self.assertEqual(actual, self.expected)

    def test_includes_requested_devotions_and_eastern_catholic_terms(self) -> None:
        from tools.build_catholicism_expansion import iter_rows_from_text

        words = {word for word, _ in iter_rows_from_text(self.expected)}

        self.assertTrue(
            {
                "三钟经",
                "慈悲串经",
                "天主慈悲串经",
                "慈悲九日敬礼",
                "天主教东方礼教会",
                "东方礼天主教会",
                "自治教会",
                "拜占庭礼",
                "神圣礼仪",
                "金口圣若望神圣礼仪",
                "乌克兰希腊礼天主教会",
                "加色丁礼天主教会",
                "马龙尼礼天主教会",
                "弥撒礼成",
                "自科绝罚",
                "圣母无染原罪",
                "瓜达卢佩圣母",
                "若望保禄二世",
                "圣名",
                "主保圣人",
                "受洗名",
                "主教座堂",
                "宗座圣殿",
            }.issubset(words)
        )


if __name__ == "__main__":
    unittest.main()
