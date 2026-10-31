#!/usr/bin/env python3
"""Build the Bible names and Christian terminology supplement.

The manifest lists 和合本 and 思高本 forms of Bible names, book titles, church
terms, popes, saints and orders. Every word that no repository dictionary
already contains is written with a legal JianDao 6 code that no fixed local
dictionary uses. Words whose legal codes are all taken are skipped, so the
dictionary adds no code collisions.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build_catholicism_expansion import (
    PREFERRED_PHONETIC_PREFIXES as CATHOLIC_PREFERRED_PREFIXES,
    load_manifest,
)
from tools.eosphoros_codes import (
    choose_code,
    iter_dictionary_rows,
    load_character_code_options,
    load_character_codes,
)


ROOT = Path(__file__).resolve().parents[1]
DICT_DIR = ROOT / "dicts" / "eosphoros"
TARGET_NAME = "eosphoros.bible.dict.yaml"
DICTIONARY_NAME = "eosphoros.bible"
MANIFEST_NAME = "tools/bible_terms_2026.txt"

# Readings that differ from the character's most common reading in existing
# two-character words. Everything else ambiguous uses that most common reading,
# or the character's default code when existing words give no clear answer.
NAME_READING_PREFIXES = {
    "曾": "zr",  # zēng（乌曾舍厄辣、厄曾）
}


@dataclass(frozen=True)
class Entry:
    category: str
    word: str
    code: str


@dataclass(frozen=True)
class BuildResult:
    entries: tuple[Entry, ...]
    skipped_existing: tuple[str, ...]
    skipped_no_free_code: tuple[str, ...]


def coding_word(word: str) -> str:
    """Remove display punctuation that does not participate in JianDao codes."""
    return word.replace("·", "")


def repository_version(root: Path = ROOT) -> str:
    version = (root / "VERSION").read_text(encoding="utf-8-sig").strip()
    if not version:
        raise ValueError(f"{root / 'VERSION'} is empty")
    return version


def source_dictionaries(root: Path) -> list[Path]:
    return [path for path in sorted((root / "dicts" / "eosphoros").glob("*.dict.yaml")) if path.name != TARGET_NAME]


def relevant_positions(word: str) -> range | tuple[int, ...]:
    return range(len(word)) if len(word) <= 3 else (0, 1, 2, len(word) - 1)


def infer_preferred_prefixes(
    words: list[str],
    code_options: dict[str, tuple[str, ...]],
    dictionary_paths: list[Path],
) -> dict[str, str]:
    """Pick a reading for every ambiguous character the manifest needs.

    The reading is the two-key prefix the character uses most often in
    existing two-character words. Characters without a clear winner are left
    out and fall back to their default code.
    """
    ambiguous: set[str] = set()
    for word in words:
        coded = coding_word(word)
        for position in relevant_positions(coded):
            character = coded[position]
            prefixes = {code[:2] for code in code_options.get(character, ())}
            relevant = prefixes if len(coded) == 2 else {prefix[0] for prefix in prefixes}
            if len(relevant) > 1:
                ambiguous.add(character)

    usage: dict[str, Counter[str]] = defaultdict(Counter)
    for path in dictionary_paths:
        for word, code in iter_dictionary_rows(path):
            if len(word) != 2 or len(code) < 4:
                continue
            for character, prefix in ((word[0], code[:2]), (word[1], code[2:4])):
                if character in ambiguous:
                    usage[character][prefix] += 1

    preferred = {**CATHOLIC_PREFERRED_PREFIXES, **NAME_READING_PREFIXES}
    for character in sorted(ambiguous - set(preferred)):
        options = {code[:2] for code in code_options[character]}
        ranked = [(count, prefix) for prefix, count in usage[character].items() if prefix in options]
        ranked.sort(reverse=True)
        if ranked and (len(ranked) == 1 or ranked[0][0] > ranked[1][0]):
            preferred[character] = ranked[0][1]
    return preferred


def build_entries(root: Path = ROOT) -> BuildResult:
    dictionary_paths = source_dictionaries(root)
    manifest_rows = load_manifest(root / MANIFEST_NAME)
    danzi = root / "dicts" / "eosphoros" / "eosphoros.danzi.dict.yaml"
    code_options = load_character_code_options(danzi)

    # Every dictionary counts for "already included"; only fixed local
    # dictionaries reserve codes, since ICE and 万象 are rebuilt around them.
    # Words that differ only by the display separator are the same word.
    existing_words: set[str] = set()
    occupied: dict[str, set[str]] = defaultdict(set)
    for path in dictionary_paths:
        reserves_codes = path.name != "eosphoros.ice.dict.yaml" and ".wanxiang." not in path.name
        for word, code in iter_dictionary_rows(path):
            existing_words.add(coding_word(word))
            if reserves_codes:
                occupied[code].add(coding_word(word))

    new_rows: list[tuple[str, str]] = []
    skipped_existing: list[str] = []
    seen: set[str] = set()
    for category, word in manifest_rows:
        if coding_word(word) in existing_words:
            skipped_existing.append(word)
        elif coding_word(word) not in seen:
            new_rows.append((category, word))
        seen.add(coding_word(word))
    preferred = infer_preferred_prefixes([word for _, word in new_rows], code_options, dictionary_paths)
    character_codes = load_character_codes(danzi, preferred)

    entries: list[Entry] = []
    skipped_no_free_code: list[str] = []
    for category, word in new_rows:
        coded = coding_word(word)
        code = choose_code(coded, character_codes, occupied)
        if code is None:
            skipped_no_free_code.append(word)
            continue
        entries.append(Entry(category, word, code))
        occupied[code].add(coded)

    return BuildResult(
        entries=tuple(entries),
        skipped_existing=tuple(skipped_existing),
        skipped_no_free_code=tuple(skipped_no_free_code),
    )


def render_dictionary(result: BuildResult, version: str) -> str:
    lines = [
        "# Rime dictionary",
        "# encoding: utf-8",
        "#",
        "# 圣经人名地名、经书名、教会术语、教宗与圣人",
        "# 同时收录《和合本》与《思高本》译名，分节存放；只收其他词库尚未收录的词。",
        "---",
        f"name: {DICTIONARY_NAME}",
        f'version: "{version}"',
        "sort: original",
        "use_preset_vocabulary: false",
        "columns:",
        "  - text",
        "  - code",
        "...",
        "",
        "# 编码由 tools/build_bible_terms.py 按键道六码规则生成，逐码避开固定本地词典，不新增重码；",
        "# 所有合法码都被占用的词不收录。",
        "# 多音字取该字在现有双字词中最常用的读音，人名特殊读音单独指定。",
        "# 审核清单：tools/bible_terms_2026.txt",
    ]
    current_category: str | None = None
    for entry in result.entries:
        if entry.category != current_category:
            lines.extend(("", f"# -------------------- {entry.category} --------------------"))
            current_category = entry.category
        lines.append(f"{entry.word}\t{entry.code}")
    return "\n".join(lines) + "\n"


def expected_dictionary_text(root: Path = ROOT) -> tuple[str, BuildResult]:
    result = build_entries(root)
    return render_dictionary(result, repository_version(root)), result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true", help="write the dictionary")
    action.add_argument("--check", action="store_true", help="check that the dictionary is current")
    parser.add_argument("--verbose", action="store_true", help="list skipped words")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    expected, result = expected_dictionary_text(ROOT)
    target = DICT_DIR / TARGET_NAME
    if args.check:
        actual = target.read_text(encoding="utf-8-sig").replace("\r\n", "\n") if target.exists() else ""
        if actual != expected:
            print(f"{TARGET_NAME} is stale; run with --write.", file=sys.stderr)
            return 1
    else:
        target.write_text(expected, encoding="utf-8", newline="\n")

    print(
        f"Bible terms: {len(result.entries)} added, "
        f"{len(result.skipped_existing)} existing, "
        f"{len(result.skipped_no_free_code)} without a free code."
    )
    if args.verbose:
        print("no free code:", " ".join(result.skipped_no_free_code))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
