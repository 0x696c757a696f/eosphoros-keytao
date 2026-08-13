#!/usr/bin/env python3
"""Build Fcitx5 built-in Table packages without Rime or a custom addon."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "packaging" / "fcitx5" / "table" / "production-dictionaries.tsv"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
NORMAL_PREFIXES = {""}
KEY_CODE = "abcdefghijklmnopqrstuvwxyz;"
MAX_CODE_LENGTH = 6


@dataclass(frozen=True)
class Entry:
    text: str
    code: str
    weight: int
    source_order: int


def parse_weight(value: str) -> int:
    value = value.strip().rstrip("%")
    if not value:
        return 0
    try:
        return int(float(value))
    except ValueError:
        return 0


def read_manifest(root: Path = ROOT) -> list[Path]:
    result: list[Path] = []
    for line_number, raw in enumerate(
        (root / MANIFEST.relative_to(ROOT)).read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) == 1:
            prefix, relative = "", fields[0]
        elif len(fields) == 2:
            prefix, relative = fields
        else:
            raise ValueError(f"manifest line {line_number}: expected [prefix TAB] path")
        # Built-in Table is intentionally the normal KeyTao table. Rime-only
        # namespaces (English and reverse lookup) would change normal topup.
        if prefix not in NORMAL_PREFIXES:
            continue
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        result.append(path)
    return result


def read_rime_dictionary(path: Path, start_order: int) -> tuple[list[Entry], int]:
    entries: list[Entry] = []
    in_body = False
    sort_mode = "original"
    order = start_order
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        for line_number, raw in enumerate(source, 1):
            line = raw.rstrip("\r\n")
            if not in_body:
                if line.strip().startswith("sort:"):
                    sort_mode = line.split(":", 1)[1].split("#", 1)[0].strip()
                if line.strip() == "...":
                    in_body = True
                continue
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) < 2:
                continue
            text, code = fields[0].strip(), fields[1].strip()
            if not text or not code:
                continue
            if any(char not in KEY_CODE for char in code):
                raise ValueError(f"{path}:{line_number}: unsupported Fcitx5 table code {code!r}")
            if len(code) > MAX_CODE_LENGTH:
                raise ValueError(f"{path}:{line_number}: code exceeds {MAX_CODE_LENGTH} keys")
            weight = parse_weight(fields[2]) if len(fields) > 2 else 0
            entries.append(Entry(text, code, weight, order))
            order += 1
    if not in_body:
        raise ValueError(f"{path}: missing dictionary body marker (...)")
    if sort_mode == "by_weight":
        entries.sort(key=lambda entry: (-entry.weight, entry.source_order))
    return entries, order


def collect_entries(root: Path = ROOT) -> list[Entry]:
    result: list[Entry] = []
    seen: set[tuple[str, str]] = set()
    order = 0
    for path in read_manifest(root):
        entries, order = read_rime_dictionary(path, order)
        for entry in entries:
            key = (entry.code, entry.text)
            if key in seen:
                continue
            seen.add(key)
            result.append(entry)
    return result


def render_table(entries: list[Entry]) -> str:
    lines = [
        f"KeyCode={KEY_CODE}",
        f"Length={MAX_CODE_LENGTH}",
        "[Data]",
    ]
    lines.extend(f"{entry.code}\t{entry.text}" for entry in entries)
    return "\n".join(lines) + "\n"


def render_config() -> str:
    return """[InputMethod]
Name=Eosphoros KeyTao
Name[zh_CN]=晨星键道
Name[zh_TW]=晨星鍵道
Icon=input-keyboard
Label=晨
LangCode=zh_CN
Addon=table
Configurable=True

[Table]
File=table/eosphoros.main.dict
AutoSelect=True
AutoSelectLength=-1
NoMatchAutoSelectLength=1
CommitAfterSelect=True
CommitWhenDeactivate=True
CommitInvalidSegment=False
FirstCandidateAsPreedit=False
IgnorePunc=False
NoSortInputLength=6
SortByCodeLength=False
OrderPolicy=No
UseSystemLanguageModel=False
UseContextRelatedOrder=False
AutoPhraseLength=0
Learning=True
Hint=False
UseFullWidth=True
CandidateLayoutHint=Vertical

[Table/PrevPage]
0=Up
1=minus

[Table/NextPage]
0=Down
1=equal

[Table/PrevCandidate]
0=Left

[Table/NextCandidate]
0=Right
"""


def _zip_write(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data, compresslevel=9)


def _theme_files(root: Path, platform: str) -> list[tuple[str, Path]]:
    if platform == "linux":
        base = root / "fcitx5/linux/themes"
        return [(f"themes/{p.relative_to(base).as_posix()}", p) for p in sorted(base.rglob("*")) if p.is_file()]
    if platform == "macos":
        base = root / "fcitx5/macos/themes"
        return [(f"themes/{p.name}", p) for p in sorted(base.glob("*.conf"))]
    base = root / "mobile_themes/fcitx5-android"
    return [(f"themes/{p.name}", p) for p in sorted(base.glob("*.zip"))]


def build_packages(
    root: Path,
    output_dir: Path,
    compiler: str | None = None,
    compiled_dictionary: bytes | None = None,
) -> list[Path]:
    entries = collect_entries(root)
    table = render_table(entries).encode("utf-8")
    config = render_config().encode("utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    binary = compiled_dictionary
    if compiler:
        resolved_compiler = shutil.which(compiler) or (
            compiler if Path(compiler).is_file() else None
        )
        if resolved_compiler is None:
            raise FileNotFoundError(f"libime_tabledict not found: {compiler}")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "eosphoros.txt"
            destination = temp / "eosphoros.main.dict"
            source.write_bytes(table)
            subprocess.run([resolved_compiler, str(source), str(destination)], check=True)
            binary = destination.read_bytes()

    archives: list[Path] = []
    for platform in ("linux", "macos", "android"):
        if platform == "linux" and binary is None:
            raise ValueError("Linux package requires --compiler (libime_tabledict)")
        destination = output_dir / f"eosphoros-fcitx5-{platform}.zip"
        with zipfile.ZipFile(destination, "w") as archive:
            if platform == "linux":
                _zip_write(archive, "inputmethod/eosphoros.conf", config)
                _zip_write(archive, "table/eosphoros.main.dict", binary or b"")
            else:
                # Both official import UIs accept a .conf plus a libime text
                # dictionary and compile it inside the application.
                _zip_write(archive, "eosphoros.conf", config)
                _zip_write(archive, "eosphoros.txt", table)
            # Android's custom-table ZIP importer expects only the table
            # configuration and dictionary. Themes are published separately.
            if platform != "android":
                for name, path in _theme_files(root, platform):
                    _zip_write(archive, name, path.read_bytes())
        archives.append(destination)
    print(f"Fcitx5 Table: {len(entries)} unique rows")
    return archives


def check(root: Path = ROOT) -> None:
    entries = collect_entries(root)
    if len(entries) < 1_000_000:
        raise ValueError("Fcitx5 Table dictionary is unexpectedly incomplete")
    expected = {
        ("jxjdoo", "晨星键道"),
        ("hyefa", "婚姻圣召"),
        ("zqquo", "赞主曲"),
    }
    actual = {(entry.code, entry.text) for entry in entries}
    missing = sorted(expected - actual)
    if missing:
        raise ValueError(f"Fcitx5 Table is missing smoke rows: {missing}")
    config = render_config()
    for required in ("Addon=table", "NoMatchAutoSelectLength=1", "Length=6"):
        haystack = config if required != "Length=6" else render_table(entries[:1])
        if required not in haystack:
            raise ValueError(f"missing Fcitx5 Table setting: {required}")
    print(f"Fcitx5 Table check passed: {len(entries)} unique rows")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument("--compiler", default=shutil.which("libime_tabledict"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check(ROOT)
        return 0
    for archive in build_packages(ROOT, args.output_dir.resolve(), args.compiler):
        print(archive)
    return 0


if __name__ == "__main__":
    sys.exit(main())
