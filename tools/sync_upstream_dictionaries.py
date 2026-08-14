#!/usr/bin/env python3
"""Sync pinned Jiandao and Rime-Ice sources into native eosphoros dictionaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.clean_dictionary_quality import is_rejected
from tools.eosphoros_codes import code_candidates_from_full_codes, iter_dictionary_rows
from tools.upstream_sources import read_source, resolve_ref


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "tools" / "upstream_dictionaries.lock.json"
DICTIONARY_DIR = ROOT / "dicts" / "eosphoros"
DANZI_TARGET = DICTIONARY_DIR / "eosphoros.danzi.dict.yaml"
ICE_TARGET = DICTIONARY_DIR / "eosphoros.ice.dict.yaml"
WANXIANG_SOURCE_NAMES = (
    "yaopin", "yixue", "huaxue", "diming", "mingren", "taifeng", "jichu"
)
WANXIANG_TARGETS = {
    source_name: DICTIONARY_DIR / f"eosphoros.wanxiang.{source_name}.dict.yaml"
    for source_name in WANXIANG_SOURCE_NAMES
}
ENGLISH_TARGET = DICTIONARY_DIR / "eosphoros.en.dict.yaml"
EMOJI_EXTRA_CHARS_TARGET = ROOT / "opencc" / "eosphoros" / "eosphoros_emoji_extra_chars.lua"
EMOJI_EXTRA_INDEX_TARGET = (
    ROOT / "opencc" / "eosphoros" / "eosphoros_emoji_extra_phrases_index.lua"
)
EMOJI_EXTRA_PHRASES_TARGET = (
    ROOT / "opencc" / "eosphoros" / "eosphoros_emoji_extra_phrases_0.lua"
)
TARGETS = (
    DANZI_TARGET,
    ICE_TARGET,
    *WANXIANG_TARGETS.values(),
    ENGLISH_TARGET,
    EMOJI_EXTRA_CHARS_TARGET,
    EMOJI_EXTRA_INDEX_TARGET,
    EMOJI_EXTRA_PHRASES_TARGET,
)

GENERATOR_DEPENDENCIES = (
    "tools/sync_upstream_dictionaries.py",
    "tools/clean_dictionary_quality.py",
    "tools/eosphoros_codes.py",
    "tools/upstream_sources.py",
)

LOCAL_WORD_DICTIONARIES = (
    "eosphoros.user.dict.yaml",
    "eosphoros.zzc.dict.yaml",
    "eosphoros.cizu.dict.yaml",
    "eosphoros.catholicism.dict.yaml",
    "eosphoros.protestantism.dict.yaml",
    "eosphoros.orthodoxy.dict.yaml",
    "eosphoros.oriental.dict.yaml",
    "eosphoros.assyrian.dict.yaml",
    "eosphoros.core.dict.yaml",
    "eosphoros.fjcy.dict.yaml",
)

# Curated specialty dictionaries must remain collision-free even when every
# legal suffix of a low-priority ICE row is occupied. In that situation the
# ICE row is omitted instead of sharing the specialty term's final six-key code.
STRICT_LOCAL_COLLISION_DICTIONARIES = (
    "eosphoros.protestantism.dict.yaml",
    "eosphoros.orthodoxy.dict.yaml",
    "eosphoros.oriental.dict.yaml",
    "eosphoros.assyrian.dict.yaml",
)

RIME_ICE_FILES = (
    ("base", "cn_dicts/base.dict.yaml"),
    ("ext", "cn_dicts/ext.dict.yaml"),
    ("others", "cn_dicts/others.dict.yaml"),
)

RIME_ICE_ENGLISH_FILES = (
    ("en", "en_dicts/en.dict.yaml"),
    ("en_ext", "en_dicts/en_ext.dict.yaml"),
)

RIME_ICE_EMOJI_FILE = ("emoji", "opencc/emoji.txt")

RIME_WANXIANG_FILES = tuple(
    (source_name, f"dicts/{source_name}.dict.yaml")
    for source_name in WANXIANG_SOURCE_NAMES
)


# Keep pathological template families from filling a candidate menu even when
# the aggregate collision budget has room. Existing local rows are never
# removed; this cap only controls additional Rime-Ice rows.
MAX_COMBINED_CANDIDATES_PER_CODE = 8

# Rime-Ice is a fallback vocabulary here, not the primary eosphoros lexicon. Keep
# short lexical items, but trim the long tail that is expensive to deploy and
# can still be entered naturally as shorter segments. The upstream ``ext``
# dictionary assigns every row the same weight, so length and template shape
# are the only stable signals available for that source.
ICE_BASE_LOW_WEIGHT_MAX = 10
ICE_BASE_LOW_WEIGHT_MIN_LENGTH = 4
ICE_EXT_MAX_LENGTH = 7
ICE_ABSOLUTE_MAX_LENGTH = 11
ICE_NUMERALS = frozenset("零〇一二三四五六七八九十百千万亿兆两壹贰叁肆伍陆柒捌玖拾佰仟")
ICE_NUMERIC_SUFFIXES = (
    "年",
    "年代",
    "年度",
    "月份",
    "月",
    "日",
    "号",
    "届",
    "级",
    "章",
    "条",
    "期",
    "册",
    "卷",
    "岁",
)
ICE_MEDICINE_DOSAGE_FORMS = (
    "片剂",
    "含片",
    "咀嚼片",
    "泡腾片",
    "分散片",
    "缓释片",
    "控释片",
    "肠溶片",
    "舌下片",
    "胶囊",
    "软胶囊",
    "硬胶囊",
    "胶丸",
    "颗粒",
    "颗粒剂",
    "冲剂",
    "滴丸",
    "散剂",
    "粉剂",
    "注射液",
    "注射剂",
    "粉针剂",
    "口服液",
    "口服溶液",
    "滴眼液",
    "滴耳液",
    "滴鼻液",
    "混悬液",
    "雾化液",
    "膏剂",
    "眼膏",
    "乳膏",
    "软膏",
    "凝胶",
    "凝胶剂",
    "栓",
    "栓剂",
    "糖浆",
    "糖浆剂",
    "合剂",
    "酊",
    "酊剂",
    "喷雾剂",
    "气雾剂",
    "吸入剂",
    "洗剂",
    "搽剂",
    "贴剂",
    "膜剂",
    "灌肠剂",
)
ICE_AMBIGUOUS_MEDICINE_FORMS = ("片", "丸", "散", "膏")
ICE_NON_MEDICINE_SUFFIXES = (
    "图片",
    "照片",
    "相片",
    "唱片",
    "影片",
    "宣传片",
    "纪录片",
    "切片",
    "碎片",
    "卡片",
    "名片",
    "芯片",
    "镜片",
    "叶片",
    "瓦片",
    "肉片",
    "鱼片",
    "鸡片",
    "肚片",
    "鳝片",
    "螺片",
    "萝卜片",
    "面片",
    "扩散",
    "离散",
    "聚散",
    "云散",
    "吹散",
    "走散",
    "失散",
    "疏散",
    "解散",
    "消散",
    "肉丸",
    "鱼丸",
    "弹丸",
    "睾丸",
)

# Syllables with no unambiguous monophonic anchor in pinyin_simp. Values are
# the corresponding Jiandao double-pinyin prefixes in 01.danzi.txt.
PINYIN_PREFIX_ALIASES = {
    "chua": "wq",
    "dei": "dw",
    "ei": "xw",
    "gei": "gw",
    "lia": "ls",
    "lo": "ll",
    "lve": "lh",
    "nve": "nh",
    "shei": "eb",
    "tei": "tw",
}

# Both variants are legal fly keys. Prefer the primary spellings used by this
# repository and explicitly confirmed for entries such as 召.
PINYIN_PREFIX_OVERRIDES = {
    "zhao": "fz",
    "zhe": "fe",
}


@dataclass(frozen=True, slots=True)
class SourceRow:
    word: str
    pinyin: tuple[str, ...]
    weight: int
    source: str
    source_priority: int
    order: int


@dataclass(frozen=True, slots=True)
class PendingRow:
    source_row: SourceRow
    candidates: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GeneratedRow:
    word: str
    code: str
    weight: int
    source_priority: int
    order: int
    is_medicine: bool = False


@dataclass(frozen=True)
class BuildResult:
    danzi_text: str
    ice_text: str
    wanxiang_texts: dict[str, str]
    english_text: str
    emoji_extra_chars_text: str
    emoji_extra_index_text: str
    emoji_extra_phrases_text: str
    stats: dict[str, int]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_generator_input_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def generator_input_sha256(root: Path, lock: dict[str, Any]) -> str:
    relative_paths = {
        *GENERATOR_DEPENDENCIES,
        "VERSION",
        "dicts/eosphoros/pinyin_simp.dict.yaml",
        *(f"dicts/eosphoros/{name}" for name in LOCAL_WORD_DICTIONARIES),
        "opencc/eosphoros/eosphoros_emoji_chars.lua",
        *(
            f"opencc/eosphoros/eosphoros_emoji_phrases_{suffix}.lua"
            for suffix in "0123456789abcdef"
        ),
    }
    descriptor = {
        "generated_on": lock["generated_on"],
        "sources": lock["sources"],
        "unicode_version": unicodedata.unidata_version,
    }
    digest = hashlib.sha256(
        json.dumps(
            descriptor,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    for relative in sorted(relative_paths):
        path = root / relative
        digest.update(b"\0" + relative.encode("utf-8") + b"\0")
        digest.update(
            canonical_generator_input_bytes(path) if path.is_file() else b"<missing>"
        )
    return digest.hexdigest()


def load_lock(path: Path = LOCK_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_danzi_rows(text: str) -> dict[str, tuple[str, ...]]:
    character_codes: dict[str, list[str]] = defaultdict(list)
    for line in text.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        character, code = fields[:2]
        if (
            len(character) == 1
            and len(code) >= 3
            and code.isascii()
            and code.islower()
        ):
            character_codes[character].append(code)
    return {character: tuple(codes) for character, codes in character_codes.items()}


def load_pinyin_readings(path: Path) -> dict[str, set[str]]:
    readings: dict[str, set[str]] = defaultdict(set)
    for text, code in iter_dictionary_rows(path):
        if len(text) == 1 and " " not in code:
            readings[text].add(code.replace("ü", "v"))
    return readings


def build_pinyin_prefixes(
    character_codes: dict[str, tuple[str, ...]],
    pinyin_readings: dict[str, set[str]],
) -> dict[str, str]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for character, readings in pinyin_readings.items():
        if len(readings) != 1:
            continue
        pinyin = next(iter(readings))
        for prefix in {code[:2] for code in character_codes.get(character, ())}:
            counts[pinyin][prefix] += 1

    prefixes: dict[str, str] = {}
    for pinyin, counter in counts.items():
        prefixes[pinyin] = sorted(
            counter.items(), key=lambda item: (-item[1], item[0])
        )[0][0]
    prefixes.update(PINYIN_PREFIX_ALIASES)
    prefixes.update(PINYIN_PREFIX_OVERRIDES)
    return prefixes


def normalize_pinyin_syllable(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower())
    output: list[str] = []
    for char in decomposed:
        if unicodedata.combining(char):
            if char == "\N{COMBINING DIAERESIS}" and output and output[-1] == "u":
                output[-1] = "v"
            continue
        output.append("v" if char == "ü" else char)
    return "".join(output)


def iter_rime_ice_rows(text: str, source: str, priority: int):
    in_data = False
    order = 0
    for line in text.splitlines():
        if line.strip() == "...":
            in_data = True
            continue
        if not in_data or not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 2 or not fields[0] or not fields[1]:
            continue
        weight = 0
        if len(fields) >= 3 and re.fullmatch(r"-?\d+", fields[2]):
            weight = int(fields[2])
        yield SourceRow(
            word=fields[0],
            pinyin=tuple(normalize_pinyin_syllable(item) for item in fields[1].split()),
            weight=weight,
            source=source,
            source_priority=priority,
            order=order,
        )
        order += 1


WANXIANG_HAN_RE = re.compile(r"^[\u3400-\u9fff\uf900-\ufaff]{2,12}$")
WANXIANG_INCOMPLETE_ENDINGS = (
    "的", "地", "得", "了", "着", "过", "吗", "呢", "吧", "啊", "呀",
    "氯化亚", "甲基己",
)
WANXIANG_CHEMISTRY_MARKERS = (
    "酸", "碱", "盐", "酯", "醇", "酚", "酮", "醚", "醛", "胺", "酰",
    "烷", "烯", "炔", "苯", "硫", "磷", "氯", "溴", "碘", "氟", "氧",
    "化物", "元素", "同位素", "聚合物", "矿物",
)
WANXIANG_PLACE_SUFFIXES = (
    "省", "市", "县", "区", "旗", "盟", "州", "乡", "镇", "村", "屯", "岛",
    "山", "岭", "峰", "河", "江", "湖", "海", "湾", "港", "洲", "路", "街",
    "巷", "寺", "关", "口", "站", "机场", "半岛", "群岛", "自治区",
)


def wanxiang_low_value_reason(row: SourceRow) -> str | None:
    """Return why an upstream Wanxiang row is unsuitable for eosphoros.

    Wanxiang's pinyin weights are selection signals only.  This conservative
    profile keeps specialist vocabulary and a very small high-frequency slice
    of the general dictionary; noisy name extraction and sentence association
    data are deliberately not imported.
    """
    word = row.word
    if not WANXIANG_HAN_RE.fullmatch(word):
        return "non_han_or_length"
    if word.endswith(WANXIANG_INCOMPLETE_ENDINGS):
        return "incomplete"
    if row.source in {"yaopin", "yixue"}:
        return None
    if row.source == "huaxue":
        return None if any(marker in word for marker in WANXIANG_CHEMISTRY_MARKERS) else "not_chemical"
    if row.source == "diming":
        if row.weight < 100 or not word.endswith(WANXIANG_PLACE_SUFFIXES):
            return "weak_place"
        return None
    if row.source == "mingren":
        return None if row.weight >= 100 else "rare_famous_name"
    if row.source == "taifeng":
        return None if word.startswith("台风") else "not_typhoon"
    if row.source == "jichu":
        return None if row.weight >= 10_000 and len(word) <= 6 else "general_long_tail"
    return "unsupported_source"


def is_likely_medicine_name(word: str) -> bool:
    """Recognize drug names by unambiguous administration/dosage wording."""
    if word.startswith("注射用") and len(word) > len("注射用"):
        return True
    if len(word) < 4 or word.endswith(ICE_NON_MEDICINE_SUFFIXES):
        return False
    return word.endswith(ICE_MEDICINE_DOSAGE_FORMS) or word.endswith(
        ICE_AMBIGUOUS_MEDICINE_FORMS
    )


def ice_low_value_reason(row: SourceRow) -> str | None:
    """Classify conservative long-tail rows excluded from the ICE fallback."""
    word = row.word
    if row.source == "ext":
        numeric_core = word
        for suffix in ICE_NUMERIC_SUFFIXES:
            if word.endswith(suffix):
                numeric_core = word[: -len(suffix)]
                break
        if len(numeric_core) >= 2 and all(char in ICE_NUMERALS for char in numeric_core):
            return "numeric_template"
    # Drug names are valuable specialist vocabulary even when upstream
    # frequency is low or the full generic name is unusually long.
    if is_likely_medicine_name(word):
        return None
    if len(word) > ICE_ABSOLUTE_MAX_LENGTH:
        return "overlong"
    if (
        row.source == "base"
        and len(word) >= ICE_BASE_LOW_WEIGHT_MIN_LENGTH
        and row.weight <= ICE_BASE_LOW_WEIGHT_MAX
    ):
        return "rare_base"
    if row.source == "ext" and len(word) > ICE_EXT_MAX_LENGTH:
        return "long_ext"
    return None


def select_full_codes(
    row: SourceRow,
    character_codes: dict[str, tuple[str, ...]],
    pinyin_prefixes: dict[str, str],
) -> list[str] | None:
    selected: list[str] = []
    for character, pinyin in zip(row.word, row.pinyin, strict=True):
        prefix = pinyin_prefixes.get(pinyin)
        if prefix is None:
            return None
        options = [
            code
            for code in character_codes.get(character, ())
            if code.startswith(prefix)
        ]
        if not options:
            return None
        selected.append(max(options, key=lambda code: (len(code), code)))
    return selected


def load_local_vocabulary(root: Path) -> tuple[set[str], dict[str, set[str]]]:
    words: set[str] = set()
    occupied: dict[str, set[str]] = defaultdict(set)
    for filename in LOCAL_WORD_DICTIONARIES:
        path = root / "dicts" / "eosphoros" / filename
        if not path.is_file():
            continue
        for word, code in iter_dictionary_rows(path):
            words.add(word)
            occupied[code].add(word)
    return words, occupied


def collision_row_count(counts: dict[str, int]) -> int:
    """Count rows whose code is shared by at least one other row."""
    return sum(count for count in counts.values() if count > 1)


def prune_ice_collisions(
    rows: list[GeneratedRow],
    local_occupied: dict[str, set[str]],
    max_candidates_per_code: int = MAX_COMBINED_CANDIDATES_PER_CODE,
) -> tuple[list[GeneratedRow], Counter[str]]:
    """Keep combined collisions at or below the existing local rate.

    ``rows`` is already ordered by source priority, frequency, and source
    order. The best row for every code unused locally is therefore retained
    first. Lower-priority rows compete for the collision budget; when a word
    can use a longer stroke-suffixed code it has already received that code in
    ``build_ice_rows`` and does not consume this budget.
    """
    stats: Counter[str] = Counter()
    local_counts = {code: len(words) for code, words in local_occupied.items()}
    local_rows = sum(local_counts.values())
    local_collision_rows = collision_row_count(local_counts)
    stats["local_rows"] = local_rows
    stats["local_collision_rows"] = local_collision_rows

    # Unit-test fixtures may have no local dictionary. There is no meaningful
    # baseline rate in that case, so leave their rows untouched.
    if local_rows == 0:
        stats["combined_rows"] = len(rows)
        ice_counts = Counter(row.code for row in rows)
        stats["combined_collision_rows"] = collision_row_count(dict(ice_counts))
        return rows, stats

    counts = dict(local_counts)
    selected: list[GeneratedRow] = []
    collision_candidates: list[GeneratedRow] = []

    # Unique anchors both preserve vocabulary breadth and create the budget
    # that permits a small number of useful same-code alternatives.
    for row in rows:
        if counts.get(row.code, 0) == 0:
            selected.append(row)
            counts[row.code] = 1
        else:
            collision_candidates.append(row)

    total_rows = local_rows + len(selected)
    combined_collision_rows = local_collision_rows

    # Medicine names are intentionally exempt from the slim filter. Give
    # them first claim on the existing collision budget without raising the
    # repository's collision-rate ceiling.
    collision_candidates.sort(key=lambda row: not row.is_medicine)
    for row in collision_candidates:
        current_count = counts[row.code]
        if current_count >= max_candidates_per_code:
            stats["skipped_candidate_cap"] += 1
            continue

        # Turning a unique code into a collision affects both rows. Once a
        # group already collides, every additional row increases the count by
        # only one.
        collision_delta = 2 if current_count == 1 else 1
        if (
            (combined_collision_rows + collision_delta) * local_rows
            > local_collision_rows * (total_rows + 1)
        ):
            stats["skipped_collision_budget"] += 1
            continue

        selected.append(row)
        counts[row.code] = current_count + 1
        total_rows += 1
        combined_collision_rows += collision_delta

    stats["combined_rows"] = total_rows
    stats["combined_collision_rows"] = combined_collision_rows
    ice_counts = Counter(row.code for row in selected)
    stats["ice_collision_rows"] = collision_row_count(dict(ice_counts))
    return selected, stats


def render_danzi(source_text: str, lock: dict[str, Any]) -> str:
    source = lock["sources"]["rime_jiandao"]
    rows = source_text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    header = (
        "# Rime dictionary\n"
        "# encoding: utf-8\n"
        "#\n"
        "# Generated from amorphobia/rime-jiandao; do not edit by hand.\n"
        f"# Source commit: {source['commit']}\n"
        "# Source file: dicts/01.danzi.txt\n"
        "# Header/concatenation behavior follows scripts/make_dicts.sh.\n"
        "---\n"
        "name: eosphoros.danzi\n"
        f"version: \"{lock['generated_on']}\"\n"
        "sort: original\n"
        "...\n\n"
    )
    return header + rows + "\n"


def normalize_english_code(code: str) -> str:
    """Convert upstream display-oriented English codes to reachable keys."""
    lowered = code.lower()
    aliases = {
        "c++": "cpp",
        "c#": "csharp",
        "f#": "fsharp",
        ".net": "dotnet",
    }
    if lowered in aliases:
        return aliases[lowered]
    return re.sub(r"[^a-z]", "", lowered)


def build_english_rows(
    source_texts: dict[str, str],
    occupied_codes: set[str] | None = None,
) -> tuple[list[tuple[str, str]], Counter[str]]:
    """Merge Rime-Ice English sources into the main-table ``i`` namespace."""
    stats: Counter[str] = Counter()
    rows: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    occupied_codes = occupied_codes or set()
    for source_name, _ in RIME_ICE_ENGLISH_FILES:
        for line in source_texts[source_name].splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
                continue
            fields = line.split("\t")
            if len(fields) < 2 or not fields[0] or not fields[1]:
                continue
            stats["english_source_rows"] += 1
            normalized = normalize_english_code(fields[1])
            if not normalized:
                stats["english_skipped_unreachable"] += 1
                continue
            key = (fields[0], "i" + normalized)
            if key[1] in occupied_codes:
                stats["english_skipped_local_code_collision"] += 1
                continue
            if key in seen:
                stats["english_deduplicated_upstream"] += 1
                continue
            seen.add(key)
            rows.append(key)
    stats["english_generated_rows"] = len(rows)
    return rows, stats


def render_english(
    rows: list[tuple[str, str]], stats: Counter[str], lock: dict[str, Any]
) -> str:
    source = lock["sources"]["rime_ice"]
    header = [
        "# Rime dictionary",
        "# encoding: utf-8",
        "#",
        "# Generated from iDvel/rime-ice; do not edit by hand.",
        f"# Source commit: {source['commit']}",
        "# Sources: en_dicts/en.dict.yaml, en_dicts/en_ext.dict.yaml",
        "# Codes are normalized to lowercase letters and prefixed with i.",
        "# Imported by the main eosphoros table; no auxiliary schema is needed.",
        f"# Source rows: {stats['english_source_rows']}",
        f"# Generated rows: {stats['english_generated_rows']}",
        f"# Deduplicated inside upstream: {stats['english_deduplicated_upstream']}",
        f"# Skipped unreachable rows: {stats['english_skipped_unreachable']}",
        f"# Skipped local code collisions: {stats['english_skipped_local_code_collision']}",
        "---",
        "name: eosphoros.en",
        f"version: \"{lock['generated_on']}\"",
        "sort: original",
        "...",
        "",
    ]
    return "\n".join(header + [f"{word}\t{code}" for word, code in rows]) + "\n"


LUA_MAPPING_KEY_RE = re.compile(r'^\s*\["((?:\\.|[^"\\])*)"\]\s*=')


def lua_unescape_key(value: str) -> str:
    return value.replace(r'\"', '"').replace(r"\\", "\\")


def lua_quote(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace('"', r'\"')
        .replace("\n", r"\n")
        .replace("\r", r"\r")
    )


def load_base_emoji_keys(root: Path) -> set[str]:
    emoji_root = root / "opencc" / "eosphoros"
    paths = [emoji_root / "eosphoros_emoji_chars.lua"]
    paths.extend(
        emoji_root / f"eosphoros_emoji_phrases_{suffix}.lua"
        for suffix in "0123456789abcdef"
    )
    keys: set[str] = set()
    for path in paths:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = LUA_MAPPING_KEY_RE.match(line)
            if match:
                keys.add(lua_unescape_key(match.group(1)))
    return keys


def build_emoji_extra(
    source_text: str, root: Path, lock: dict[str, Any]
) -> tuple[str, str, str, Counter[str]]:
    """Build a non-overwriting Rime-Ice Emoji overlay for the Lua filter."""
    stats: Counter[str] = Counter()
    base_keys = load_base_emoji_keys(root)
    rows: dict[str, str] = {}
    for line in source_text.splitlines():
        if not line or line.lstrip().startswith("#") or "\t" not in line:
            continue
        key, value = line.split("\t", 1)
        if not key or not value:
            continue
        stats["emoji_source_rows"] += 1
        if key in base_keys:
            stats["emoji_deduplicated_local"] += 1
            continue
        if key in rows:
            stats["emoji_deduplicated_upstream"] += 1
            continue
        rows[key] = value

    chars = {key: value for key, value in rows.items() if len(key) == 1}
    phrases = {key: value for key, value in rows.items() if len(key) > 1}
    index = {key[0]: "0" for key in phrases}
    stats["emoji_extra_char_rows"] = len(chars)
    stats["emoji_extra_index_rows"] = len(index)
    stats["emoji_extra_phrase_rows"] = len(phrases)
    stats["emoji_extra_rows"] = len(rows)

    source = lock["sources"]["rime_ice"]
    header = [
        "-- eosphoros Rime-Ice Emoji 增补数据",
        "-- Generated from iDvel/rime-ice; do not edit by hand.",
        f"-- Source commit: {source['commit']}",
        f"-- 更新：{lock['generated_on']}",
        "",
        "return {",
    ]

    def render_table(mapping: dict[str, str]) -> str:
        body = [
            f'  ["{lua_quote(key)}"] = "{lua_quote(mapping[key])}",'
            for key in sorted(mapping)
        ]
        return "\n".join(header + body + ["}", ""])

    return render_table(chars), render_table(index), render_table(phrases), stats


def build_ice_rows(
    source_texts: dict[str, str],
    character_codes: dict[str, tuple[str, ...]],
    pinyin_prefixes: dict[str, str],
    local_words: set[str],
    occupied: dict[str, set[str]],
    protected_local_codes: set[str] | None = None,
) -> tuple[list[GeneratedRow], Counter[str]]:
    stats: Counter[str] = Counter()
    protected_local_codes = protected_local_codes or set()
    local_occupied = {code: set(words) for code, words in occupied.items()}
    working_occupied: dict[str, set[str]] = defaultdict(set)
    working_occupied.update(
        {code: set(words) for code, words in local_occupied.items()}
    )
    seen_source_words: set[str] = set()
    pending: list[PendingRow] = []

    for priority, (source_name, _) in enumerate(RIME_ICE_FILES):
        for row in iter_rime_ice_rows(source_texts[source_name], source_name, priority):
            stats["source_rows"] += 1
            if row.word in seen_source_words:
                stats["deduplicated_upstream"] += 1
                continue
            seen_source_words.add(row.word)
            if row.word in local_words:
                stats["deduplicated_local"] += 1
                continue
            if len(row.word) < 2:
                stats["skipped_single_character"] += 1
                continue
            if len(row.word) != len(row.pinyin):
                stats["skipped_unaligned"] += 1
                continue
            if is_rejected(row.word, ""):
                stats["skipped_rejected"] += 1
                continue
            if is_likely_medicine_name(row.word):
                stats["recognized_medicine_names"] += 1
            low_value_reason = ice_low_value_reason(row)
            if low_value_reason is not None:
                stats[f"skipped_low_value_{low_value_reason}"] += 1
                continue
            full_codes = select_full_codes(row, character_codes, pinyin_prefixes)
            if full_codes is None:
                stats["skipped_unencodable"] += 1
                continue
            pending.append(
                PendingRow(row, tuple(code_candidates_from_full_codes(full_codes)))
            )

    generated: list[GeneratedRow] = []
    for item in sorted(
        pending,
        key=lambda item: (
            item.source_row.source_priority,
            len(item.source_row.word),
            -item.source_row.weight,
            item.source_row.order,
        ),
    ):
        row = item.source_row
        selected = None
        for candidate in item.candidates:
            if not working_occupied.get(candidate):
                selected = candidate
                break
        if selected is None:
            selected = item.candidates[-1]
            if selected in protected_local_codes:
                stats["skipped_protected_local_collision"] += 1
                continue
            stats["unavoidable_code_collisions"] += 1
        working_occupied[selected].add(row.word)
        generated.append(
            GeneratedRow(
                word=row.word,
                code=selected,
                weight=row.weight,
                source_priority=row.source_priority,
                order=row.order,
                is_medicine=is_likely_medicine_name(row.word),
            )
        )

    stats["generated_before_collision_pruning"] = len(generated)
    generated, pruning_stats = prune_ice_collisions(generated, local_occupied)
    stats.update(pruning_stats)
    stats["generated_medicine_names"] = sum(row.is_medicine for row in generated)
    generated.sort(
        key=lambda row: (
            row.code,
            -row.weight,
            row.source_priority,
            row.order,
            row.word,
        )
    )
    stats["generated_rows"] = len(generated)
    return generated, stats


def render_ice(
    rows: list[GeneratedRow], stats: Counter[str], lock: dict[str, Any]
) -> str:
    source = lock["sources"]["rime_ice"]
    header = [
        "# Rime dictionary",
        "# encoding: utf-8",
        "#",
        "# Generated from iDvel/rime-ice; do not edit by hand.",
        f"# Source commit: {source['commit']}",
        "# Sources: cn_dicts/base.dict.yaml, ext.dict.yaml, others.dict.yaml",
        "# Local dictionaries take precedence; duplicate text is excluded.",
        "# Priority: local > base > ext > others; higher source weight first.",
        "# Common homophones keep short codes; lower-priority ones add stroke keys.",
        "# Slim fallback profile: never directly filter 2-3 character words.",
        "# Unaligned, unencodable, rejected, and low-value entries are skipped.",
        f"# Source rows: {stats['source_rows']}",
        f"# Generated rows: {stats['generated_rows']}",
        f"# Rows before collision pruning: {stats['generated_before_collision_pruning']}",
        f"# Deduplicated against local dictionaries: {stats['deduplicated_local']}",
        f"# Deduplicated inside upstream: {stats['deduplicated_upstream']}",
        f"# Skipped unaligned: {stats['skipped_unaligned']}",
        f"# Skipped unencodable: {stats['skipped_unencodable']}",
        f"# Skipped rejected: {stats['skipped_rejected']}",
        f"# Recognized medicine names kept: {stats['recognized_medicine_names']}",
        f"# Generated medicine names: {stats['generated_medicine_names']}",
        f"# Skipped low-value numeric templates: {stats['skipped_low_value_numeric_template']}",
        f"# Skipped low-weight base entries: {stats['skipped_low_value_rare_base']}",
        f"# Skipped long ext entries: {stats['skipped_low_value_long_ext']}",
        f"# Skipped overlong entries: {stats['skipped_low_value_overlong']}",
        f"# Full-code collisions before pruning: {stats['unavoidable_code_collisions']}",
        f"# Skipped by collision-rate budget: {stats['skipped_collision_budget']}",
        f"# Skipped by per-code candidate cap: {stats['skipped_candidate_cap']}",
        "# Collision target: no higher than the existing local dictionaries.",
        f"# Local collision rows: {stats['local_collision_rows']} / {stats['local_rows']}",
        f"# Combined collision rows: {stats['combined_collision_rows']} / {stats['combined_rows']}",
        "---",
        "name: eosphoros.ice",
        f"version: \"{lock['generated_on']}\"",
        "sort: original",
        "...",
        "",
    ]
    body = [f"{row.word}\t{row.code}" for row in rows]
    return "\n".join(header + body) + "\n"


def build_wanxiang_rows(
    source_texts: dict[str, str],
    character_codes: dict[str, tuple[str, ...]],
    pinyin_prefixes: dict[str, str],
    higher_priority_words: set[str],
    occupied: dict[str, set[str]],
) -> tuple[list[GeneratedRow], Counter[str]]:
    """Build a collision-free, low-priority specialist Wanxiang supplement."""
    stats: Counter[str] = Counter()
    seen: set[str] = set()
    pending: list[PendingRow] = []
    for priority, (source_name, _) in enumerate(RIME_WANXIANG_FILES):
        for row in iter_rime_ice_rows(source_texts[source_name], source_name, priority):
            stats["wanxiang_source_rows"] += 1
            stats[f"wanxiang_source_{source_name}"] += 1
            if row.word in seen:
                stats["wanxiang_deduplicated_upstream"] += 1
                continue
            seen.add(row.word)
            if row.word in higher_priority_words:
                stats["wanxiang_deduplicated_local"] += 1
                continue
            reason = wanxiang_low_value_reason(row)
            if reason is not None:
                stats[f"wanxiang_skipped_low_value_{reason}"] += 1
                continue
            if len(row.word) != len(row.pinyin):
                stats["wanxiang_skipped_unaligned"] += 1
                continue
            if is_rejected(row.word, ""):
                stats["wanxiang_skipped_rejected"] += 1
                continue
            full_codes = select_full_codes(row, character_codes, pinyin_prefixes)
            if full_codes is None:
                stats["wanxiang_skipped_unencodable"] += 1
                continue
            pending.append(PendingRow(row, tuple(code_candidates_from_full_codes(full_codes))))

    working = {code: set(words) for code, words in occupied.items()}
    generated: list[GeneratedRow] = []
    for item in sorted(
        pending,
        key=lambda item: (
            item.source_row.source_priority,
            len(item.source_row.word),
            -item.source_row.weight,
            item.source_row.order,
        ),
    ):
        selected = next(
            (candidate for candidate in item.candidates if not working.get(candidate)),
            None,
        )
        if selected is None:
            stats["wanxiang_skipped_collision"] += 1
            continue
        row = item.source_row
        working.setdefault(selected, set()).add(row.word)
        generated.append(
            GeneratedRow(row.word, selected, row.weight, row.source_priority, row.order)
        )
        stats[f"wanxiang_generated_{row.source}"] += 1
    generated.sort(key=lambda row: (row.code, -row.weight, row.source_priority, row.order, row.word))
    stats["wanxiang_generated_rows"] = len(generated)
    return generated, stats


def render_wanxiang(
    source_name: str,
    rows: list[GeneratedRow],
    stats: Counter[str],
    lock: dict[str, Any],
) -> str:
    source = lock["sources"]["rime_wanxiang"]
    header = [
        "# Rime dictionary",
        "# encoding: utf-8",
        "#",
        "# Generated from amzxyz/rime-wanxiang; do not edit by hand.",
        f"# Source commit: {source['commit']}",
        f"# Selected source: dicts/{source_name}.dict.yaml.",
        "# Pinyin weights are used only for filtering/order; codes are regenerated as eosphoros.",
        "# Curated local vocabulary takes precedence; colliding rows are omitted.",
        "# Accepted codes are protected while the lower-priority Rime-Ice fallback is rebuilt.",
        f"# Source rows in category: {stats[f'wanxiang_source_{source_name}']}",
        f"# Generated rows in category: {stats[f'wanxiang_generated_{source_name}']}",
        "---",
        f"name: eosphoros.wanxiang.{source_name}",
        f"version: \"{lock['generated_on']}\"",
        "sort: original",
        "...",
        "",
    ]
    return "\n".join(header + [f"{row.word}\t{row.code}" for row in rows]) + "\n"


def build(
    root: Path,
    lock: dict[str, Any],
    jiandao_root: Path | None = None,
    rime_ice_root: Path | None = None,
    rime_wanxiang_root: Path | None = None,
) -> BuildResult:
    jiandao_source = lock["sources"]["rime_jiandao"]
    ice_source = lock["sources"]["rime_ice"]
    wanxiang_source = lock["sources"]["rime_wanxiang"]
    danzi_source_text = read_source(
        jiandao_source, "dicts/01.danzi.txt", jiandao_root
    )
    source_texts = {
        source_name: read_source(ice_source, relative_path, rime_ice_root)
        for source_name, relative_path in (
            RIME_ICE_FILES + RIME_ICE_ENGLISH_FILES + (RIME_ICE_EMOJI_FILE,)
        )
    }
    wanxiang_source_texts = {
        source_name: read_source(wanxiang_source, relative_path, rime_wanxiang_root)
        for source_name, relative_path in RIME_WANXIANG_FILES
    }

    character_codes = parse_danzi_rows(danzi_source_text)
    pinyin_readings = load_pinyin_readings(root / "dicts" / "eosphoros" / "pinyin_simp.dict.yaml")
    pinyin_prefixes = build_pinyin_prefixes(character_codes, pinyin_readings)
    local_words, occupied = load_local_vocabulary(root)
    protected_local_codes = {
        code
        for filename in STRICT_LOCAL_COLLISION_DICTIONARIES
        if (root / "dicts" / "eosphoros" / filename).is_file()
        for _, code in iter_dictionary_rows(root / "dicts" / "eosphoros" / filename)
    }
    wanxiang_rows, wanxiang_stats = build_wanxiang_rows(
        wanxiang_source_texts,
        character_codes,
        pinyin_prefixes,
        local_words,
        occupied,
    )
    augmented_words = set(local_words)
    augmented_occupied = {code: set(words) for code, words in occupied.items()}
    for row in wanxiang_rows:
        augmented_words.add(row.word)
        augmented_occupied.setdefault(row.code, set()).add(row.word)
    protected_local_codes.update(row.code for row in wanxiang_rows)
    ice_rows, stats = build_ice_rows(
        source_texts,
        character_codes,
        pinyin_prefixes,
        augmented_words,
        augmented_occupied,
        protected_local_codes,
    )
    stats.update(wanxiang_stats)
    english_occupied = set(occupied)
    english_occupied.update(row.code for row in ice_rows)
    english_occupied.update(row.code for row in wanxiang_rows)
    english_rows, english_stats = build_english_rows(source_texts, english_occupied)
    stats.update(english_stats)
    (
        emoji_extra_chars_text,
        emoji_extra_index_text,
        emoji_extra_phrases_text,
        emoji_stats,
    ) = build_emoji_extra(source_texts["emoji"], root, lock)
    stats.update(emoji_stats)
    return BuildResult(
        danzi_text=render_danzi(danzi_source_text, lock),
        ice_text=render_ice(ice_rows, stats, lock),
        wanxiang_texts={
            source_name: render_wanxiang(
                source_name,
                [row for row in wanxiang_rows if row.source_priority == priority],
                stats,
                lock,
            )
            for priority, (source_name, _) in enumerate(RIME_WANXIANG_FILES)
        },
        english_text=render_english(english_rows, stats, lock),
        emoji_extra_chars_text=emoji_extra_chars_text,
        emoji_extra_index_text=emoji_extra_index_text,
        emoji_extra_phrases_text=emoji_extra_phrases_text,
        stats=dict(stats),
    )


def update_generated_metadata(
    lock: dict[str, Any], result: BuildResult
) -> dict[str, Any]:
    lock = json.loads(json.dumps(lock))
    lock["generated"] = {
        DANZI_TARGET.relative_to(ROOT).as_posix(): {
            "sha256": sha256_text(result.danzi_text),
            "rows": result.danzi_text.count("\n") - 13,
        },
        ICE_TARGET.relative_to(ROOT).as_posix(): {
            "sha256": sha256_text(result.ice_text),
            "rows": result.stats["generated_rows"],
        },
        ENGLISH_TARGET.relative_to(ROOT).as_posix(): {
            "sha256": sha256_text(result.english_text),
            "rows": result.stats["english_generated_rows"],
        },
        "opencc/eosphoros/eosphoros_emoji_extra_chars.lua": {
            "sha256": sha256_text(result.emoji_extra_chars_text),
            "rows": result.stats["emoji_extra_char_rows"],
        },
        "opencc/eosphoros/eosphoros_emoji_extra_phrases_index.lua": {
            "sha256": sha256_text(result.emoji_extra_index_text),
            "rows": result.stats["emoji_extra_index_rows"],
        },
        "opencc/eosphoros/eosphoros_emoji_extra_phrases_0.lua": {
            "sha256": sha256_text(result.emoji_extra_phrases_text),
            "rows": result.stats["emoji_extra_phrase_rows"],
        },
    }
    for source_name, target in WANXIANG_TARGETS.items():
        lock["generated"][target.relative_to(ROOT).as_posix()] = {
            "sha256": sha256_text(result.wanxiang_texts[source_name]),
            "rows": result.stats[f"wanxiang_generated_{source_name}"],
        }
    lock["statistics"] = dict(sorted(result.stats.items()))
    lock["generator_input_sha256"] = generator_input_sha256(ROOT, lock)
    return lock


def verify_generated_hashes(root: Path = ROOT, lock_path: Path = LOCK_PATH) -> list[str]:
    lock = load_lock(lock_path)
    errors: list[str] = []
    for filename, metadata in lock.get("generated", {}).items():
        path = root / filename
        if not path.is_file():
            errors.append(f"missing generated dictionary {filename}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != metadata["sha256"]:
            errors.append(f"generated dictionary differs from lock: {filename}")
    return errors


def verify_generated_state(root: Path, lock: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_input = lock.get("generator_input_sha256")
    actual_input = generator_input_sha256(root, lock)
    if expected_input != actual_input:
        errors.append(
            "upstream generator inputs differ from lock; run "
            "tools/sync_upstream_dictionaries.py --check"
        )
    for filename, metadata in lock.get("generated", {}).items():
        path = root / filename
        if not path.is_file():
            errors.append(f"missing generated dictionary {filename}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != metadata["sha256"]:
            errors.append(f"generated dictionary differs from lock: {filename}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write dictionaries and lock")
    parser.add_argument("--check", action="store_true", help="fail when regeneration differs")
    parser.add_argument(
        "--quick-check",
        action="store_true",
        help="verify content-addressed generator inputs and committed output hashes",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="resolve configured branches to their latest commits before generation",
    )
    parser.add_argument(
        "--refresh-source",
        action="append",
        choices=tuple(sorted(("rime_jiandao", "rime_ice", "rime_wanxiang"))),
        default=[],
        help="refresh only one named source; may be repeated",
    )
    parser.add_argument("--jiandao-root", type=Path, help="use a local rime-jiandao checkout")
    parser.add_argument("--rime-ice-root", type=Path, help="use a local rime-ice checkout")
    parser.add_argument("--rime-wanxiang-root", type=Path, help="use a local rime-wanxiang checkout")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (args.refresh or args.refresh_source) and not args.write:
        raise SystemExit("--refresh and --refresh-source require --write")

    lock = load_lock()
    repository_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", repository_version):
        raise SystemExit("VERSION must use YYYY-MM-DD")
    # VERSION is the single date source. A plain --write after changing the
    # repository version must not restore an older generated_on from the lock.
    lock["generated_on"] = repository_version
    if args.quick_check:
        if args.check or args.write or args.refresh or args.refresh_source or any(
            (args.jiandao_root, args.rime_ice_root, args.rime_wanxiang_root)
        ):
            raise SystemExit(
                "--quick-check cannot be combined with full check, write, refresh, or local roots"
            )
        errors = verify_generated_state(ROOT, lock)
        if errors:
            for error in errors:
                print(error)
            return 1
        print("Upstream generator inputs and outputs match the content-addressed lock")
        return 0
    sources_to_refresh = (
        set(lock["sources"]) if args.refresh else set(args.refresh_source)
    )
    if sources_to_refresh:
        for source_name in sorted(sources_to_refresh):
            source = lock["sources"][source_name]
            source["commit"] = resolve_ref(source["repository"], source["branch"])

    result = build(
        ROOT, lock, args.jiandao_root, args.rime_ice_root, args.rime_wanxiang_root
    )
    expected = {
        DANZI_TARGET: result.danzi_text,
        ICE_TARGET: result.ice_text,
        ENGLISH_TARGET: result.english_text,
        EMOJI_EXTRA_CHARS_TARGET: result.emoji_extra_chars_text,
        EMOJI_EXTRA_INDEX_TARGET: result.emoji_extra_index_text,
        EMOJI_EXTRA_PHRASES_TARGET: result.emoji_extra_phrases_text,
    }
    expected.update(
        {
            WANXIANG_TARGETS[source_name]: text
            for source_name, text in result.wanxiang_texts.items()
        }
    )
    changed = [
        path
        for path, text in expected.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != text
    ]

    for key in sorted(result.stats):
        print(f"{key}={result.stats[key]}")
    for path in TARGETS:
        print(f"{path.name}: {'changed' if path in changed else 'clean'}")

    if args.write:
        for path, text in expected.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
        updated_lock = update_generated_metadata(lock, result)
        LOCK_PATH.write_text(
            json.dumps(updated_lock, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
