#!/usr/bin/env python3
"""Clean high-confidence corruption and abusive junk from non-danzi dictionaries."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.eosphoros_codes import load_character_code_options


ROOT = Path(__file__).resolve().parents[1]
TARGET_NAMES = (
    "eosphoros.core.dict.yaml",
    "eosphoros.cizu.dict.yaml",
    "eosphoros.fjcy.dict.yaml",
    "eosphoros.ice.dict.yaml",
    "pinyin_simp.dict.yaml",
)

ROW_REPLACEMENTS = {
    "eosphoros.cizu.dict.yaml": {
        "不成其为\tbjqwvvv": "不成其为\tbjqwvv",
        "布甲鞋\tbjxvviv": "布甲鞋\tbjxviv",
        "钡盐\tbwyfivv": "钡盐\tbwyfiv",
        "都招\tddfzu2": "都招\tddfzu",
        "搭着\tdsfeio ": "搭着\tdsfeio",
        "这根\tfegnosss": "这根\tfegn",
        "中间调\tfjdiooo": "中间调\tfjdioo",
        "出阁\tjjgeaoa": "出阁\tjjgeao",
        "速听\tsjtgV": "速听\tsjtgv",
        "淡啦\ttflsa.碳蜡\ttflsv": "淡啦\tdflsa\n碳蜡\ttflsv",
        "养恩\typxn~": "养恩\typxn",
        "于死地\tysdvvvv": "于死地\tysdvvv",
        "还不认账\tbhrq": "还不认账\thbrq",
        "不会冷\tbhrvio": "不会冷\tbhlvio",
        "板蓝根颗粒\tblgnv": "板蓝根颗粒\tblglv",
        "脾胃虚弱\tbwxr": "脾胃虚弱\tpwxr",
        "不用挣扎\tbyffv": "不用挣扎\tbyqfv",
    },
    "eosphoros.fjcy.dict.yaml": {
        "基莲\tjklmvii": "基莲\tjklmvi",
    },
    "pinyin_simp.dict.yaml": {
        "袮\tni\t51": "袮\tmi\t51",
        "胊\txu\t1": "胊\tqu\t1",
    },
}

ROW_REMOVALS = {
    "eosphoros.core.dict.yaml": {
        "富强 民主 文明 和谐 自由 平等 公正 法治 爱国 敬业 诚信 友善\tfmwh",
    },
    "eosphoros.cizu.dict.yaml": {
        "不必这样\tbbfq",
        "练但三等分\tlmdx",
        # Keep the standard JianDao 6 code jdng; this duplicate mnemonic code
        # is neither a legal word code nor useful as a second candidate.
        "京都念慈庵蜜炼川贝枇杷膏\tkesd",
    },
    "pinyin_simp.dict.yaml": {
        "汩\tmi\t12",
        "不\tdun\t3",
        "沐\tshu\t21",
    },
}

# These patterns are unambiguously abusive, obscene, or discriminatory in a
# general-purpose input dictionary. Clinical and legal terms are deliberately
# not included.
REJECTED_SUBSTRINGS = (
    "肏",
    "操你妈",
    "操你大爷",
    "草尼玛",
    "傻逼",
    "煞笔",
    "妈逼",
    "妈屄",
    "鸡巴",
    "几把",
    "妈卖批",
    "你妈的胎盘",
    "支那",
    "黑鬼",
    "日本鬼子",
    "小日本",
    "洋鬼子",
)

REJECTED_EXACT_WORDS = {
    "沙比",
    # Sentence fragments and quotations imported from upstream dictionaries.
    # Their component words remain available, so keeping the whole sentence
    # only adds collisions and artificial candidates.
    "仁义不施而攻守之势异也",
    "亦使后人而复哀后人也",
    "曾不如早索我于枯鱼之肆",
    "是骡子是马拉出来遛遛",
    "好的开端是成功的一半",
    "良好的开端是成功的一半",
    "鳏寡孤独废疾者皆有所养",
    "夫妻在婚姻关系存续期间",
    "军人以服从命令为天职",
    "节约时间就是延长生命",
    "非法占用耕地改作他用",
    "主动交代违法违纪行为",
    "其行为已经构成诈骗罪",
    "司法为民做群众满意法官",
    "调解优先促社会稳定和谐",
    "天雨虽宽不润无根之草",
    "用本民族语言进行诉讼",
    "愿天下眷属皆是有情人",
    "最新商务文书写作全编",
}

# Myitkyina is a valid place name, not the slur caught by the substring rule.
ALLOWLIST = {
    "密支那",
}

# The word dictionary once accumulated whole quotations, chat replies, typing
# notes, and search prompts.  They are shortcuts or explanations rather than
# lexical entries and make ordinary codes needlessly crowded.  Proper names,
# official titles, medicines, and other fixed long terms are intentionally not
# rejected merely because they are long.
INLINE_READING_NOTE_RE = re.compile(
    r"[\u3400-\u9fff].*[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]+.*[（(]"
)
PARENTHETICAL_CODE_RE = re.compile(r"[（(][a-z|]{2,}[）)]")
LONG_SENTENCE_PUNCTUATION = frozenset("，。！？；：、,.!?;:")
LONG_SHORTCUT_CODE_PREFIXES = (
    "ercwu",  # numbered aphorism paragraphs
    "hheha",  # conversation-advice paragraphs
    "jebai",  # full paragraphs from 出师表
    "msrn",   # stock insult/chat replies
)
LONG_NONLEXICAL_EXACT_WORDS = {
    "卑鄙是卑鄙者的通行证",
    "不知道从什么时候开始",
    "不出意外就会出意外啦",
    "不出意外的话就会出意外",
    "不出意外的话肯定出意外",
    "不要让孩子输在起跑线上",
    "这事情不是你做得了的",
    "这是个两全期美的办法",
    "本不富裕的家庭雪上加霜",
    "多种所有制经济共同发展",
    "世界一流大学和一流学科",
    "喝了这杯奶→忘了那个仔",
    "建设中国特色社会主义",
    "建设有中国特色社会主义",
    "科学技术是第一生产力",
    "你拨打的电话不在服务区",
    "抛开事实不谈[旺柴]",
    "枸杞红枣桂圆五味子桑葚",
    "以其人之道还治其人之身",
    "针灸中药方剂辩证分型",
    "微雕绣式光离子包皮整形",
    "娇兰花草水语安妮莎贝拉",
    "娇兰花草水语之华贵牡丹",
    "泰尼莫格勒天使星光偶像",
    "放到乡下你都算是个痴批",
    "你可真是个绝种好男人",
    "要不要看看你在说什么",
    "你要不要看看你在说什么",
    "对不起·抱歉·打扰了",
    "操操操操操操操操操操",
    "不是驴不走就是磨不转",
    "麻烦您再看下核对下地址",
    "本店暂不支持指定快递",
    "嫁出去的女儿泼出去的水",
    "宁可无了有不可有了无",
    "一个君子待了十个小人",
    "不记前仇俏媳妇戴凤冠",
    "打灯笼走亲戚一明去明来",
    "点燃的蜡烛一长命不了",
    "脚踩西瓜皮手里抓把泥",
    "明看不成器丢又舍不得",
    "哪一壶不开单提哪一壶",
    "你吃鸡鸭肉我啃窝窝头",
    "骑马时间少擦镫时间多",
    "天上的老鹰不吃脏东西",
    "宰个鸽鸽也要请屠夫提刀",
    "知道你是哪块地里有呢",
    "鼠牛虎兔龙蛇马羊猴鸡狗猪",
    "枸杞大枣桂圆西洋参菊花冰糖",
    "搜不到力工梭哈就搜力工嗦啥",
    "你拨打的电话暂时无人接听",
    "你知道这五年我是怎么过的吗",
    "阿姆斯特朗回旋加速喷气式阿姆斯特朗炮",
    "马查贝利王子艾维安斯夜间麝香",
    "泰尼莫格勒天使纯情夏日露水",
    "如需指定快递请提前告知或备注",
    "百斤重担能上肩一两笔杆提不动",
    "一官二吏三僧四道五工六农七匠八娼九儒十丐",
    "底层男性为结婚把命和钱全押上赌一个家",
}


@dataclass(frozen=True)
class Result:
    path: Path
    replacements: int
    removals: int
    changed: bool


def valid_word_codes(word: str, options: dict[str, tuple[str, ...]]) -> set[str]:
    """Return every standard 3-6 key code supported by the single-char table."""
    if len(word) < 2 or any(character not in options for character in word):
        return set()

    valid: set[str] = set()
    for full_codes in product(*(options[character] for character in word)):
        if len(word) == 2:
            base = full_codes[0][:2] + full_codes[1][:2]
            auxiliary = (full_codes[0][2], full_codes[1][2])
        elif len(word) == 3:
            base = "".join(code[0] for code in full_codes)
            auxiliary = tuple(code[2] for code in full_codes)
        else:
            base = "".join(code[0] for code in full_codes[:3]) + full_codes[-1][0]
            auxiliary = (full_codes[0][2], full_codes[1][2])
        valid.add(base)
        for length in range(1, min(len(auxiliary), 6 - len(base)) + 1):
            valid.add(base + "".join(auxiliary[:length]))
    return valid


def validate_replacements(root: Path = ROOT) -> None:
    options = load_character_code_options(root / "dicts" / "eosphoros" / "eosphoros.danzi.dict.yaml")
    errors: list[str] = []
    for filename, replacements in ROW_REPLACEMENTS.items():
        for old_row, new_rows in replacements.items():
            for new_row in new_rows.splitlines():
                word, code, *_ = new_row.split("\t")
                if filename == "pinyin_simp.dict.yaml":
                    if len(word) != len(code.split()):
                        errors.append(
                            f"{filename}: {old_row!r} -> {new_row!r} has mismatched syllables"
                        )
                    continue
                valid = valid_word_codes(word, options)
                if code not in valid:
                    errors.append(
                        f"{filename}: {old_row!r} -> {new_row!r} is not a standard code; "
                        f"candidates={sorted(valid)!r}"
                    )
    if errors:
        raise ValueError("\n".join(errors))


def is_rejected(text: str, code: str) -> bool:
    if text in ALLOWLIST:
        return False
    if text in REJECTED_EXACT_WORDS:
        return True
    if any(pattern in text for pattern in REJECTED_SUBSTRINGS):
        return True

    # Remove obvious pasted meme/abuse paragraphs while preserving intentional
    # classical-text shortcuts such as the existing 出师表 entries.
    if len(text) >= 20 and code == "nmsl":
        return True
    if text.startswith("每日一问：今天超越了吗"):
        return True
    if len(text) >= 20 and "🤙" in text:
        return True
    return False


def is_rejected_cizu_row(text: str, code: str) -> bool:
    """Reject high-confidence non-lexical rows from the local word dictionary."""
    if is_rejected(text, code):
        return True
    if INLINE_READING_NOTE_RE.search(text):
        return True
    if PARENTHETICAL_CODE_RE.search(text):
        return True
    if text.startswith(("最新读音规范", "读作")):
        return True
    if "规范读" in text and any(char.isascii() and char.isalpha() for char in text):
        return True
    if text in LONG_NONLEXICAL_EXACT_WORDS:
        return True
    if len(text) < 10:
        return False
    if code.startswith(LONG_SHORTCUT_CODE_PREFIXES):
        return True
    if len(text) >= 10 and any(mark in text for mark in LONG_SENTENCE_PUNCTUATION):
        return True
    if len(text) >= 12 and any("\u3400" <= char <= "\u9fff" for char in text) and any(
        char.isascii() and char.isalpha() for char in text
    ):
        return True
    if len(text) >= 10 and any(ord(char) > 0xFFFF for char in text):
        return True
    return False


def clean_text(path: Path, source: str) -> tuple[str, int, int]:
    replacements = ROW_REPLACEMENTS.get(path.name, {})
    row_removals = ROW_REMOVALS.get(path.name, set())
    output: list[str] = []
    replacement_count = 0
    removal_count = 0

    for line in source.splitlines():
        if line in row_removals:
            removal_count += 1
            continue
        replacement = replacements.get(line)
        if replacement is not None:
            output.extend(replacement.splitlines())
            replacement_count += 1
            continue

        fields = line.split("\t")
        if len(fields) >= 2:
            rejected = is_rejected(fields[0], fields[1])
            if path.name == "eosphoros.cizu.dict.yaml":
                rejected = is_rejected_cizu_row(fields[0], fields[1])
            if rejected:
                removal_count += 1
                continue
        output.append(line)

    trailing_newline = "\n" if source.endswith("\n") else ""
    return "\n".join(output) + trailing_newline, replacement_count, removal_count


def process(root: Path = ROOT, write: bool = False) -> list[Result]:
    results: list[Result] = []
    for name in TARGET_NAMES:
        path = root / "dicts" / "eosphoros" / name
        source = path.read_text(encoding="utf-8")
        cleaned, replacements, removals = clean_text(path, source)
        changed = cleaned != source
        if write and changed:
            path.write_text(cleaned, encoding="utf-8", newline="\n")
        results.append(Result(path, replacements, removals, changed))
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="apply the cleanup")
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if a cleanup would still change any target",
    )
    parser.add_argument(
        "--list-rejections",
        action="store_true",
        help="print every row selected by the content filter",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validate_replacements()
    if args.list_rejections:
        for name in TARGET_NAMES:
            path = ROOT / "dicts" / "eosphoros" / name
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                fields = line.split("\t")
                if len(fields) < 2:
                    continue
                rejected = is_rejected(fields[0], fields[1])
                if name == "eosphoros.cizu.dict.yaml":
                    rejected = is_rejected_cizu_row(fields[0], fields[1])
                if rejected:
                    print(f"{name}:{number}: {line}")
        return 0
    results = process(write=args.write)
    for result in results:
        state = "changed" if result.changed else "clean"
        print(
            f"{result.path.name}: {state}; "
            f"replacements={result.replacements}, removals={result.removals}"
        )
    if args.check and any(result.changed for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
