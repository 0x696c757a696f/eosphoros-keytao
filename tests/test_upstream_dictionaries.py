from __future__ import annotations

import re
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path

from tools.sync_upstream_dictionaries import (
    GeneratedRow,
    PINYIN_PREFIX_OVERRIDES,
    RIME_WANXIANG_FILES,
    SourceRow,
    build_english_rows,
    build_emoji_extra,
    build_ice_rows,
    build_wanxiang_rows,
    ice_low_value_reason,
    is_likely_medicine_name,
    wanxiang_low_value_reason,
    load_lock,
    normalize_pinyin_syllable,
    prune_ice_collisions,
    render_danzi,
    verify_generated_hashes,
)
from tools.eosphoros_codes import code_candidates_from_full_codes, iter_dictionary_rows
from tools.upstream_sources import raw_url, read_source


ROOT = Path(__file__).resolve().parents[1]
DICT_DIR = ROOT / "dicts" / "eosphoros"


def source_text(*rows: str) -> str:
    return "# Rime dictionary\n---\nname: fixture\n...\n" + "\n".join(rows) + "\n"


class UpstreamDictionaryTests(unittest.TestCase):
    def test_upstream_lock_date_matches_the_repository_version(self) -> None:
        lock = load_lock()
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(lock["generated_on"], version)

    def test_upstream_source_adapter_supports_pinned_urls_and_local_checkouts(self) -> None:
        source = {
            "repository": "example/project",
            "commit": "a" * 40,
        }
        self.assertEqual(
            raw_url(source, "dicts/base.dict.yaml"),
            "https://raw.githubusercontent.com/example/project/"
            + "a" * 40
            + "/dicts/base.dict.yaml",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "fixture.txt").write_text("词条\n", encoding="utf-8")
            self.assertEqual(read_source(source, "fixture.txt", root), "词条\n")

    def test_scheduled_sync_reuses_the_incremental_git_cache(self) -> None:
        workflow = (ROOT / ".github/workflows/sync-upstream-dictionaries.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("uses: actions/cache@v6", workflow)
        self.assertIn("path: .tmp/upstream-git-cache", workflow)
        self.assertIn("-CacheDirectory .tmp/upstream-git-cache", workflow)

    def test_data_dictionaries_live_below_dicts_eosphoros_with_rimetool_root_index(self) -> None:
        self.assertEqual(
            {path.name for path in ROOT.glob("*.dict.yaml")},
            {
                "eosphoros.cx.dict.yaml",
                "eosphoros.extended.dict.yaml",
                "eosphoros.gbk.dict.yaml",
                "liangfen.dict.yaml",
                "pinyin_simp.dict.yaml",
            },
        )
        dictionary_dir = ROOT / "dicts" / "eosphoros"
        self.assertTrue((dictionary_dir / "pinyin_simp.dict.yaml").is_file())
        self.assertTrue((dictionary_dir / "liangfen.dict.yaml").is_file())
        main_schema = (ROOT / "eosphoros.schema.yaml").read_text(encoding="utf-8")
        self.assertIn("dictionary: eosphoros.extended", main_schema)
        for schema_name in (
            "eosphoros.cx.schema.yaml",
            "eosphoros.gbk.schema.yaml",
            "pinyin_simp.schema.yaml",
            "liangfen.schema.yaml",
        ):
            self.assertTrue((ROOT / schema_name).is_file())
        self.assertIn("dependencies:", main_schema)
        for dictionary in ("eosphoros.cx", "eosphoros.gbk", "liangfen", "pinyin_simp"):
            self.assertIn(f"dictionary: {dictionary}", main_schema)
            helper_schema = (ROOT / f"{dictionary}.schema.yaml").read_text(
                encoding="utf-8"
            )
            self.assertIn(f"dictionary: {dictionary}", helper_schema)
        root_index = (ROOT / "eosphoros.extended.dict.yaml").read_text(encoding="utf-8")
        import_block = root_index.split("import_tables:", 1)[1]
        first_import = next(
            line.strip() for line in import_block.splitlines() if line.startswith("  - ")
        )
        self.assertEqual(first_import, "- dicts/eosphoros/eosphoros.user")
        for dictionary in ("eosphoros.cx", "eosphoros.gbk", "liangfen", "pinyin_simp"):
            index = (ROOT / f"{dictionary}.dict.yaml").read_text(encoding="utf-8")
            self.assertIn(f"- dicts/eosphoros/{dictionary}", index)
        custom = (ROOT / "eosphoros.custom.yaml").read_text(encoding="utf-8")
        self.assertIn(
            "reverse_hint/pron_map_file: dicts/eosphoros/eosphoros.cx.dict.yaml",
            custom,
        )

    def test_tone_marked_pinyin_normalizes_without_losing_umlaut(self) -> None:
        self.assertEqual(normalize_pinyin_syllable("piàn"), "pian")
        self.assertEqual(normalize_pinyin_syllable("lǜ"), "lv")
        self.assertEqual(normalize_pinyin_syllable("nǚ"), "nv")

    def test_wanxiang_filter_keeps_specialist_terms_and_rejects_fragments(self) -> None:
        accepted = (
            SourceRow("吲哚美辛", ("yin", "duo", "mei", "xin"), 100, "yaopin", 0, 0),
            SourceRow("深静脉血栓", ("shen", "jing", "mai", "xue", "shuan"), 100, "yixue", 1, 0),
            SourceRow("乙烯醇", ("yi", "xi", "chun"), 100, "huaxue", 2, 0),
            SourceRow("杭州市", ("hang", "zhou", "shi"), 1000, "diming", 3, 0),
            SourceRow("台风海葵", ("tai", "feng", "hai", "kui"), 100, "taifeng", 4, 0),
        )
        rejected = (
            SourceRow("氯化亚", ("lv", "hua", "ya"), 100, "huaxue", 2, 0),
            SourceRow("甲基己", ("jia", "ji", "ji"), 100, "huaxue", 2, 0),
            SourceRow("老师的", ("lao", "shi", "de"), 100000, "jichu", 6, 0),
            SourceRow("张伟", ("zhang", "wei"), 10000, "renming", 7, 0),
        )
        self.assertTrue(all(wanxiang_low_value_reason(row) is None for row in accepted))
        self.assertTrue(all(wanxiang_low_value_reason(row) for row in rejected))

    def test_wanxiang_conversion_deduplicates_and_uses_free_stroke_codes(self) -> None:
        sources = {
            "yaopin": source_text("吲哚美辛\tyin duo mei xin\t100", "本地药\tben di yao\t99"),
            "yixue": source_text("深静脉血栓\tshen jing mai xue shuan\t100"),
            "huaxue": source_text("氯化亚\tlv hua ya\t100"),
            "diming": source_text(),
            "mingren": source_text(),
            "taifeng": source_text(),
            "jichu": source_text(),
        }
        chars = {
            "吲": ("yba",), "哚": ("dla",), "美": ("mwr",), "辛": ("xbo",),
            "深": ("ena",), "静": ("jko",), "脉": ("mda",), "血": ("xhr",), "栓": ("egr",),
        }
        prefixes = {
            "yin": "yb", "duo": "dl", "mei": "mw", "xin": "xb",
            "shen": "en", "jing": "jk", "mai": "md", "xue": "xh", "shuan": "eg",
        }
        rows, stats = build_wanxiang_rows(
            sources, chars, prefixes, {"本地药"}, {"ybmd": {"已有词"}}
        )
        self.assertEqual({row.word for row in rows}, {"吲哚美辛", "深静脉血栓"})
        self.assertEqual(stats["wanxiang_deduplicated_local"], 1)
        self.assertEqual(stats["wanxiang_skipped_low_value_incomplete"], 1)
        self.assertTrue(all(4 <= len(row.code) <= 6 for row in rows))

    def test_emoji_extra_adds_rime_ice_rows_without_overwriting_local_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            emoji_root = root / "opencc" / "eosphoros"
            emoji_root.mkdir(parents=True)
            (emoji_root / "eosphoros_emoji_chars.lua").write_text(
                'return {\n  ["笑"] = "😁",\n}\n', encoding="utf-8"
            )
            (emoji_root / "eosphoros_emoji_phrases_0.lua").write_text(
                'return {\n  ["你好"] = "👋",\n}\n', encoding="utf-8"
            )
            chars, index, phrases, stats = build_emoji_extra(
                "笑\t笑 😄\n你好\t你好 👋\n嗅\t嗅 👃\n熬夜\t熬夜 🫩\n",
                root,
                load_lock(),
            )

        self.assertNotIn('["笑"]', chars)
        self.assertNotIn('["你好"]', phrases)
        self.assertIn('["嗅"] = "嗅 👃"', chars)
        self.assertIn('["熬夜"] = "熬夜 🫩"', phrases)
        self.assertIn('["熬"] = "0"', index)
        self.assertEqual(stats["emoji_source_rows"], 4)
        self.assertEqual(stats["emoji_deduplicated_local"], 2)
        self.assertEqual(stats["emoji_extra_rows"], 2)

    def test_ice_slim_profile_only_removes_clear_long_tail_rows(self) -> None:
        def row(word: str, weight: int, source: str) -> SourceRow:
            return SourceRow(word, (), weight, source, 0, 0)

        self.assertIsNone(ice_low_value_reason(row("低频词", 1, "base")))
        self.assertIsNone(ice_low_value_reason(row("正常四字", 11, "base")))
        self.assertIsNone(ice_low_value_reason(row("七个字以内正常", 100, "ext")))
        self.assertEqual(
            ice_low_value_reason(row("低频四字", 10, "base")), "rare_base"
        )
        self.assertEqual(
            ice_low_value_reason(row("二〇二六年", 100, "ext")),
            "numeric_template",
        )
        self.assertEqual(
            ice_low_value_reason(row("超过七个字的扩展短语", 100, "ext")),
            "long_ext",
        )
        self.assertEqual(
            ice_low_value_reason(row("这是一个长度超过十一字的完整句子", 999, "base")),
            "overlong",
        )

    def test_ice_slim_profile_keeps_low_frequency_medicine_names(self) -> None:
        medicine_names = (
            "阿莫西林片",
            "奥美拉唑胶囊",
            "苯巴比妥钠注射液",
            "盐酸左氧氟沙星滴眼液",
            "注射用醋酸卡泊芬净",
        )
        for word in medicine_names:
            with self.subTest(word=word):
                row = SourceRow(word, (), 1, "base", 0, 0)
                self.assertTrue(is_likely_medicine_name(word))
                self.assertIsNone(ice_low_value_reason(row))

        self.assertFalse(is_likely_medicine_name("纪录片"))
        self.assertFalse(is_likely_medicine_name("保存图片"))
        self.assertFalse(is_likely_medicine_name("被动扩散"))
        self.assertFalse(is_likely_medicine_name("爆炒肉片"))
        self.assertFalse(is_likely_medicine_name("普通四字词"))

    def test_position_specific_codes_follow_confirmed_fly_key_rules(self) -> None:
        self.assertEqual(
            code_candidates_from_full_codes(("zfu", "qjo", "qlv")),
            ["zqq", "zqqu", "zqquo", "zqquov"],
        )
        self.assertEqual(
            code_candidates_from_full_codes(("hya", "yba", "ero", "fzu")),
            ["hyef", "hyefa", "hyefaa"],
        )
        self.assertEqual(PINYIN_PREFIX_OVERRIDES["zhao"], "fz")
        self.assertEqual(PINYIN_PREFIX_OVERRIDES["zhe"], "fe")

    def test_rime_ice_conversion_deduplicates_with_local_priority(self) -> None:
        sources = {
            "base": source_text(
                "本地词\tben di ci\t100",
                "新词\txin ci\t90",
                "重复词\tchong fu ci\t80",
                "傻逼\tsha bi\t70",
            ),
            "ext": source_text(
                "新词\txin ci\t999",
                "扩展词\tkuo zhan ci\t60",
            ),
            "others": source_text("扩展词\tkuo zhan ci"),
        }
        character_codes = {
            "新": ("xbv",),
            "词": ("cko",),
            "重": ("wyi",),
            "复": ("fju",),
            "扩": ("klv",),
            "展": ("qfv",),
        }
        prefixes = {
            "xin": "xb",
            "ci": "ck",
            "chong": "wy",
            "fu": "fj",
            "kuo": "kl",
            "zhan": "qf",
        }

        rows, stats = build_ice_rows(
            sources,
            character_codes,
            prefixes,
            {"本地词"},
            defaultdict(set),
        )

        self.assertEqual({row.word for row in rows}, {"新词", "重复词", "扩展词"})
        self.assertEqual(stats["deduplicated_local"], 1)
        self.assertEqual(stats["deduplicated_upstream"], 2)
        self.assertEqual(stats["skipped_rejected"], 1)

    def test_common_homophones_get_shorter_codes_first(self) -> None:
        sources = {
            "base": source_text(
                "新词\txin ci\t100",
                "心辞\txin ci\t10",
            ),
            "ext": source_text(),
            "others": source_text(),
        }
        character_codes = {
            "新": ("xbv",),
            "心": ("xbv",),
            "词": ("cko",),
            "辞": ("cko",),
        }
        rows, _ = build_ice_rows(
            sources,
            character_codes,
            {"xin": "xb", "ci": "ck"},
            set(),
            {"local": {"本地词"}},
        )

        codes = {row.word: row.code for row in rows}
        self.assertEqual(codes["新词"], "xbck")
        self.assertEqual(codes["心辞"], "xbckv")

    def test_short_words_take_base_codes_before_long_phrases(self) -> None:
        sources = {
            "base": source_text(
                "甲乙丙丁\tjia yi bing ding\t9999",
                "短语\tduan yu\t1",
            ),
            "ext": source_text(),
            "others": source_text(),
        }
        character_codes = {
            "甲": ("aba",),
            "乙": ("bba",),
            "丙": ("cca",),
            "丁": ("dda",),
            "短": ("aba",),
            "语": ("cda",),
        }
        prefixes = {
            "jia": "ab",
            "yi": "bb",
            "bing": "cc",
            "ding": "dd",
            "duan": "ab",
            "yu": "cd",
        }

        rows, _ = build_ice_rows(
            sources,
            character_codes,
            prefixes,
            set(),
            defaultdict(set),
        )

        codes = {row.word: row.code for row in rows}
        self.assertEqual(codes["短语"], "abcd")
        self.assertEqual(codes["甲乙丙丁"], "abcda")

    def test_collision_pruning_does_not_exceed_local_rate(self) -> None:
        local = {f"l{index}": {f"词{index}"} for index in range(98)}
        local["shared"] = {"甲", "乙"}
        rows = [
            GeneratedRow(f"唯一{index}", f"new{index}", 100, 0, index)
            for index in range(100)
        ]
        rows.extend(
            [
                GeneratedRow("高频", "new0", 90, 0, 100),
                GeneratedRow("低频", "new0", 10, 2, 101),
            ]
        )

        selected, stats = prune_ice_collisions(rows, local)

        self.assertIn("高频", {row.word for row in selected})
        self.assertNotIn("低频", {row.word for row in selected})
        self.assertLessEqual(
            stats["combined_collision_rows"] * stats["local_rows"],
            stats["local_collision_rows"] * stats["combined_rows"],
        )

    def test_collision_budget_prefers_medicine_over_ordinary_long_tail(self) -> None:
        local = {f"l{index}": {f"词{index}"} for index in range(98)}
        local["shared"] = {"甲", "乙"}
        rows = [
            GeneratedRow(f"唯一{index}", f"new{index}", 100, 0, index)
            for index in range(100)
        ]
        rows.extend(
            [
                GeneratedRow("普通长尾", "new0", 100, 0, 100),
                GeneratedRow("阿莫西林片", "new1", 1, 0, 101, True),
            ]
        )

        selected, stats = prune_ice_collisions(rows, local)
        selected_words = {row.word for row in selected}

        self.assertIn("阿莫西林片", selected_words)
        self.assertNotIn("普通长尾", selected_words)
        self.assertLessEqual(
            stats["combined_collision_rows"] * stats["local_rows"],
            stats["local_collision_rows"] * stats["combined_rows"],
        )

    def test_danzi_uses_local_name_and_pinned_source(self) -> None:
        lock = load_lock()
        rendered = render_danzi("不\tb\n宾\tbb\n滨\tbbv\n", lock)

        self.assertIn("name: eosphoros.danzi", rendered)
        self.assertIn(lock["sources"]["rime_jiandao"]["commit"], rendered)
        self.assertTrue(rendered.endswith("不\tb\n宾\tbb\n滨\tbbv\n"))

    def test_english_sources_are_namespaced_normalized_and_deduplicated(self) -> None:
        rows, stats = build_english_rows(
            {
                "en": source_text("Hello\tHello", "C++\tC++", "README.md\tREADME.md"),
                "en_ext": source_text("Hello\tHello", "C#\tC#", "纯符号\t+++", "A4\tA4"),
            },
            {"ia"},
        )

        self.assertEqual(
            rows,
            [
                ("Hello", "ihello"),
                ("C++", "icpp"),
                ("README.md", "ireadmemd"),
                ("C#", "icsharp"),
            ],
        )
        self.assertEqual(stats["english_deduplicated_upstream"], 1)
        self.assertEqual(stats["english_skipped_unreachable"], 1)
        self.assertEqual(stats["english_skipped_local_code_collision"], 1)

    def test_generated_files_match_locked_checksums(self) -> None:
        self.assertEqual(verify_generated_hashes(ROOT), [])

    def test_ice_dictionary_is_imported_after_local_wordlists(self) -> None:
        text = (ROOT / "eosphoros.extended.dict.yaml").read_text(encoding="utf-8")
        self.assertIn("  - dicts/eosphoros/eosphoros.ice", text)
        self.assertLess(
            text.index("  - dicts/eosphoros/eosphoros.fjcy"),
            text.index("  - dicts/eosphoros/eosphoros.ice"),
        )

    def test_wanxiang_dictionaries_are_split_below_dicts_eosphoros_after_ice(self) -> None:
        text = (ROOT / "eosphoros.extended.dict.yaml").read_text(encoding="utf-8")
        names = [name for name, _ in RIME_WANXIANG_FILES]
        paths = [
            ROOT / "dicts" / "eosphoros" / f"eosphoros.wanxiang.{name}.dict.yaml"
            for name in names
        ]
        for name, path in zip(names, paths, strict=True):
            table = f"dicts/eosphoros/eosphoros.wanxiang.{name}"
            self.assertIn(f"  - {table}", text)
            self.assertLess(
                text.index("  - dicts/eosphoros/eosphoros.ice"), text.index(f"  - {table}")
            )
            self.assertTrue(path.is_file())
        self.assertFalse((ROOT / "eosphoros.wanxiang.dict.yaml").exists())
        rows = [row for path in paths for row in iter_dictionary_rows(path)]
        self.assertEqual(len(rows), len({word for word, _ in rows}))
        self.assertTrue(all(re.fullmatch(r"[a-z]{3,6}", code) for _, code in rows))
        wanxiang_codes = {code for _, code in rows}
        higher_priority_codes = {
            code
            for path in DICT_DIR.glob("eosphoros.*.dict.yaml")
            if path.name != "eosphoros.en.dict.yaml" and ".wanxiang." not in path.name
            for _, code in iter_dictionary_rows(path)
        }
        self.assertEqual(wanxiang_codes & higher_priority_codes, set())
        lock = load_lock()
        self.assertEqual(lock["sources"]["rime_wanxiang"]["branch"], "wanxiang")
        self.assertEqual(lock["sources"]["rime_wanxiang"]["license"], "CC-BY-4.0")

    def test_english_dictionary_uses_main_schema_i_namespace(self) -> None:
        extended = (ROOT / "eosphoros.extended.dict.yaml").read_text(encoding="utf-8")
        schema = (ROOT / "eosphoros.schema.yaml").read_text(encoding="utf-8")
        self.assertIn("  - dicts/eosphoros/eosphoros.en", extended)
        self.assertIn("xform/^i(.+)$/$1/", schema)
        self.assertIn('prefix: "i"', schema)
        self.assertIn("max_code_length: 64", schema)
        self.assertNotIn("- eosphoros.en", schema)
        self.assertFalse((ROOT / "eosphoros.en.schema.yaml").exists())
        rows = list(iter_dictionary_rows(DICT_DIR / "eosphoros.en.dict.yaml"))
        self.assertGreater(len(rows), 20_000)
        self.assertEqual(len(rows), len(set(rows)))
        self.assertTrue(all(re.fullmatch(r"i[a-z]+", code) for _, code in rows))
        english_codes = {code for _, code in rows}
        local_files = (
            "eosphoros.user.dict.yaml",
            "eosphoros.zzc.dict.yaml",
            "eosphoros.danzi.dict.yaml",
            "eosphoros.cizu.dict.yaml",
            "eosphoros.catholicism.dict.yaml",
            "eosphoros.protestantism.dict.yaml",
            "eosphoros.orthodoxy.dict.yaml",
            "eosphoros.oriental.dict.yaml",
            "eosphoros.assyrian.dict.yaml",
            "eosphoros.core.dict.yaml",
            "eosphoros.fjcy.dict.yaml",
            "eosphoros.ice.dict.yaml",
        )
        local_codes = {
            code
            for filename in local_files
            if (DICT_DIR / filename).is_file()
            for _, code in iter_dictionary_rows(DICT_DIR / filename)
        }
        self.assertEqual(english_codes & local_codes, set())

    def test_rime_ice_emoji_overlay_is_loaded_by_the_existing_lua_filter(self) -> None:
        schema = (ROOT / "eosphoros.schema.yaml").read_text(encoding="utf-8")
        chars = (
            ROOT / "opencc" / "eosphoros" / "eosphoros_emoji_extra_chars.lua"
        ).read_text(encoding="utf-8")
        phrases = (
            ROOT / "opencc" / "eosphoros" / "eosphoros_emoji_extra_phrases_0.lua"
        ).read_text(encoding="utf-8")
        lock = load_lock()

        self.assertIn('dataset_name: "eosphoros_emoji_extra"', schema)
        self.assertIn('["嗅"] = "嗅 👃"', chars)
        self.assertIn('["熬夜"] = "熬夜 🫩"', phrases)
        self.assertIn('["指纹"] = "指纹 🫆"', phrases)
        self.assertGreater(lock["statistics"]["emoji_extra_rows"], 2_000)
        self.assertIn("opencc/emoji.txt", lock["sources"]["rime_ice"]["files"])

    def test_release_conversion_includes_ice_dictionary(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "create-release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("eosphoros.ice.dict.yaml", workflow)
        self.assertIn("Rime/eosphoros.ice.txt", workflow)
        self.assertIn("eosphoros.en.dict.yaml", workflow)
        self.assertIn("Rime/eosphoros.en.txt", workflow)
        self.assertIn("dicts/eosphoros/eosphoros.wanxiang.*.dict.yaml", workflow)
        self.assertIn("Rime/eosphoros.wanxiang.yaopin.txt", workflow)
        self.assertIn("Rime/eosphoros.wanxiang.jichu.txt", workflow)

    def test_incremental_updater_compares_pinned_git_commits(self) -> None:
        script = (ROOT / "tools" / "update_upstream_dictionaries.ps1").read_text(
            encoding="utf-8"
        )
        self.assertIn('"diff", "--name-only"', script)
        self.assertIn('"--refresh-source"', script)
        self.assertIn("update_versions.py", script)
        self.assertIn("Get-Command python", script)
        self.assertNotIn("D:\\", script)

    def test_scheduled_sync_opens_a_validated_pull_request(self) -> None:
        workflow = (
            ROOT / ".github" / "workflows" / "sync-upstream-dictionaries.yml"
        ).read_text(encoding="utf-8")
        self.assertIn('cron: "17 4 * * 1"', workflow)
        self.assertIn("update_upstream_dictionaries.ps1", workflow)
        self.assertIn("python tools/validate_repo.py", workflow)
        self.assertIn("gh pr create", workflow)
        self.assertIn("VERSION", workflow)
        self.assertIn("*.yaml", workflow)


if __name__ == "__main__":
    unittest.main()
