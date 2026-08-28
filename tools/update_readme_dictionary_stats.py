#!/usr/bin/env python3
"""Update README dictionary counts and collision statistics."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

try:
    from tools.dictionary_profiles import PROFILES, profile_dictionary_name
    from tools.eosphoros_codes import iter_dictionary_rows
except ModuleNotFoundError:
    from dictionary_profiles import PROFILES, profile_dictionary_name
    from eosphoros_codes import iter_dictionary_rows


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PROFILE_MARKERS = ("<!-- dictionary-profile-stats:start -->", "<!-- dictionary-profile-stats:end -->")
DICTIONARY_MARKERS = ("<!-- dictionary-file-stats:start -->", "<!-- dictionary-file-stats:end -->")

DICTIONARIES = (
    ("eosphoros.danzi.dict.yaml", "上游键道单字表"),
    ("eosphoros.cizu.dict.yaml", "本地基础词组"),
    ("eosphoros.catholicism.dict.yaml", "天主教、礼仪、神学与东方礼词汇"),
    ("eosphoros.protestantism.dict.yaml", "传统新教宗派、信条、人物、日常教会用语及《和合本》词汇"),
    ("eosphoros.orthodoxy.dict.yaml", "东正教礼仪、圣像、灵修与教会制度专有词汇"),
    ("eosphoros.oriental.dict.yaml", "东方正统教会、合性论传统与成员教会专有词汇"),
    ("eosphoros.assyrian.dict.yaml", "东方亚述教会、东叙利亚礼与景教史专有词汇"),
    ("eosphoros.core.dict.yaml", "630 规则、快符和核心候选"),
    ("eosphoros.fjcy.dict.yaml", "附加扩展词组"),
    ("eosphoros.ice.dict.yaml", "Rime-Ice 中文精简补充词库"),
    ("eosphoros.en.dict.yaml", "Rime-Ice 英文词库"),
)


def imported_paths(profile: str) -> list[Path]:
    index = ROOT / f"{profile_dictionary_name(profile)}.dict.yaml"
    return [
        ROOT / f"{line.strip().removeprefix('- ')}.dict.yaml"
        for line in index.read_text(encoding="utf-8-sig").splitlines()
        if line.strip().startswith("- dicts/eosphoros/")
    ]


def profile_stats(profile: str) -> tuple[int, int]:
    codes = [code for path in imported_paths(profile) for _, code in iter_dictionary_rows(path)]
    counts = Counter(codes)
    return len(codes), sum(count for count in counts.values() if count > 1)


def row_count(path: Path) -> int:
    return sum(1 for _ in iter_dictionary_rows(path))


def render_profiles() -> str:
    compositions = {
        "full": "Lite + 宗派专题 + ICE + 万象专业 + `fjcy`",
        "standard": "Lite + 宗派专题 + ICE + 万象专业",
        "lite": "用户词库 + 单字 + 基础词组 + 核心码 + `i` 英文",
    }
    lines = [
        PROFILE_MARKERS[0],
        "| 档位 | 当前记录数 | 同码记录数 | 同码记录率 | 实际组成 |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for profile in PROFILES:
        total, collisions = profile_stats(profile)
        lines.append(
            f"| {profile.capitalize()} | {total:,} | {collisions:,} | "
            f"{collisions / total:.3%} | {compositions[profile]} |"
        )
    lines.extend(
        (
            "",
            "同码记录率是“最终编码与其他不同词条共用”的静态记录数占本档位总记录数的比例。"
            "上表为当前词库快照，不计入用户后续添加的动态词和客户端词频调整；该指标适合比较"
            "本项目的三个档位，不建议与统计口径不同的其他方案直接对比。",
            PROFILE_MARKERS[1],
        )
    )
    return "\n".join(lines)


def render_dictionaries() -> str:
    dictionary_dir = ROOT / "dicts" / "eosphoros"
    lines = [
        DICTIONARY_MARKERS[0],
        "| 词库 | 记录数 | 用途 |",
        "| --- | ---: | --- |",
    ]
    for filename, purpose in DICTIONARIES[:-1]:
        lines.append(
            f"| `dicts/eosphoros/{filename}` | {row_count(dictionary_dir / filename):,} | {purpose} |"
        )
        if filename == "eosphoros.ice.dict.yaml":
            wanxiang = sum(row_count(path) for path in dictionary_dir.glob("eosphoros.wanxiang.*.dict.yaml"))
            lines.append(
                f"| `dicts/eosphoros/eosphoros.wanxiang.*.dict.yaml` | {wanxiang:,} | 七个万象分类补充词库 |"
            )
    filename, purpose = DICTIONARIES[-1]
    lines.append(
        f"| `dicts/eosphoros/{filename}` | {row_count(dictionary_dir / filename):,} | {purpose} |"
    )
    total, _ = profile_stats("full")
    lines.extend(
        (
            f"| **合计** | **{total:,}** | 不含动态自造词和个人词库 |",
            DICTIONARY_MARKERS[1],
        )
    )
    return "\n".join(lines)


def replace_block(text: str, markers: tuple[str, str], replacement: str) -> str:
    start, end = markers
    if start not in text or end not in text:
        raise ValueError(f"README markers missing: {start}, {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + replacement + after


def expected_readme() -> str:
    text = README.read_text(encoding="utf-8-sig")
    text = replace_block(text, PROFILE_MARKERS, render_profiles())
    return replace_block(text, DICTIONARY_MARKERS, render_dictionaries())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()

    current = README.read_text(encoding="utf-8-sig")
    expected = expected_readme()
    if args.check:
        if current != expected:
            print("README dictionary statistics are stale")
            return 1
        return 0
    README.write_text(expected, encoding="utf-8", newline="\n")
    print("Updated README dictionary statistics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
