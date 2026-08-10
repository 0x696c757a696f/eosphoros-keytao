#!/usr/bin/env python3
"""Report sentence-like long rows across every non-single-character dictionary."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.clean_dictionary_quality import is_rejected, is_rejected_cizu_row


ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "tools" / "long_entry_allowlist.txt"
MIN_LENGTH = 10
SENTENCE_PUNCTUATION = frozenset("，。！？；：、,.!?;:")
PROTECTED_FILE_MARKERS = (".yaopin.", ".yixue.", ".huaxue.")
EXCLUDED_NAMES = {
    "eosphoros.danzi.dict.yaml",
    "eosphoros.en.dict.yaml",
    "pinyin_simp.dict.yaml",
    "liangfen.dict.yaml",
}
INLINE_NOTE_RE = re.compile(r"[\u3400-\u9fff].*[A-Za-z].*[（(]")


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    text: str
    code: str
    length: int
    reason: str


def load_allowlist(path: Path = ALLOWLIST) -> set[tuple[str, str]]:
    allowed: set[tuple[str, str]] = set()
    if not path.is_file():
        return allowed
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 2:
            raise ValueError(f"{path}:{number}: expected file<TAB>text")
        allowed.add((fields[0], fields[1]))
    return allowed


def suspicious_reason(filename: str, text: str, code: str) -> str | None:
    normalized = text.replace("·", "")
    if len(normalized) < MIN_LENGTH:
        return None
    if any(marker in filename for marker in PROTECTED_FILE_MARKERS):
        return None
    if is_rejected(text, code):
        return "known_rejected_sentence"
    if filename == "eosphoros.cizu.dict.yaml" and is_rejected_cizu_row(text, code):
        return "local_nonlexical_row"
    if any(mark in text for mark in SENTENCE_PUNCTUATION):
        return "sentence_punctuation"
    if any(char.isspace() for char in text):
        return "embedded_whitespace"
    if INLINE_NOTE_RE.search(text):
        return "inline_reading_note"
    if len(set(text)) == 1:
        return "repeated_character"
    return None


def audit(root: Path = ROOT, allowlist_path: Path = ALLOWLIST) -> tuple[list[Finding], int]:
    allowed = load_allowlist(allowlist_path)
    findings: list[Finding] = []
    long_rows = 0
    paths = sorted((root / "dicts" / "eosphoros").glob("*.dict.yaml"))
    paths.extend(sorted(root.glob("*.dict.yaml")))
    for path in paths:
        if path.name in EXCLUDED_NAMES:
            continue
        relative = path.relative_to(root).as_posix()
        for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            if not line or line.startswith("#") or "\t" not in line:
                continue
            text, code, *_ = line.split("\t")
            length = len(text.replace("·", ""))
            if length < MIN_LENGTH:
                continue
            long_rows += 1
            reason = suspicious_reason(path.name, text, code)
            if reason and (relative, text) not in allowed:
                findings.append(Finding(relative, number, text, code, length, reason))
    return findings, long_rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on unreviewed findings")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()
    findings, long_rows = audit()
    if args.json:
        print(json.dumps({"long_rows": long_rows, "findings": [asdict(x) for x in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Reviewed long rows: {long_rows}; suspicious: {len(findings)}")
        for item in findings:
            print(f"{item.file}:{item.line}: {item.reason}: {item.text}\t{item.code}")
    return 1 if args.check and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
