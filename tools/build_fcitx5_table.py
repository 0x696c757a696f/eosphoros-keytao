#!/usr/bin/env python3
"""Build Fcitx5 built-in Table packages without Rime or a custom addon."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

try:
    from tools.dictionary_profiles import PROFILES, archive_name, includes_dictionary
except ModuleNotFoundError:
    from dictionary_profiles import PROFILES, archive_name, includes_dictionary


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "packaging" / "fcitx5" / "table" / "production-dictionaries.tsv"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
KEY_CODE = "abcdefghijklmnopqrstuvwxyz;"
NAMESPACE_PREFIXES = frozenset("iuov")
MAX_CODE_LENGTH = 63


@dataclass(frozen=True)
class DictionarySource:
    namespace: str
    path: Path


@dataclass(frozen=True)
class Entry:
    text: str
    code: str
    weight: int
    source_order: int
    namespace: str = ""


def parse_weight(value: str) -> int:
    value = value.strip().rstrip("%")
    if not value:
        return 0
    try:
        return int(float(value))
    except ValueError:
        return 0


def read_manifest(root: Path = ROOT, profile: str = "full") -> list[DictionarySource]:
    result: list[DictionarySource] = []
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
        if prefix not in ({""} | NAMESPACE_PREFIXES):
            raise ValueError(f"manifest line {line_number}: unsupported namespace {prefix!r}")
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        if not includes_dictionary(relative, profile):
            continue
        result.append(DictionarySource(prefix, path))
    return result


def _namespace_code(namespace: str, code: str) -> str:
    code = code.lower().replace(" ", "").replace("'", "")
    # The synchronized English dictionary is already stored with its i prefix.
    # The other source dictionaries contain bare codes, so a leading u/v/o is
    # data and must not be mistaken for an existing namespace marker.
    if namespace and not (namespace == "i" and code.startswith("i")):
        code = namespace + code
    return code


def read_rime_dictionary(
    path: Path, start_order: int, namespace: str = ""
) -> tuple[list[Entry], int]:
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
            text, code = fields[0].strip(), _namespace_code(namespace, fields[1].strip())
            if not text or not code:
                continue
            if any(char not in KEY_CODE for char in code):
                raise ValueError(f"{path}:{line_number}: unsupported Fcitx5 table code {code!r}")
            if len(code) > MAX_CODE_LENGTH:
                raise ValueError(f"{path}:{line_number}: code exceeds {MAX_CODE_LENGTH} keys")
            weight = parse_weight(fields[2]) if len(fields) > 2 else 0
            entries.append(Entry(text, code, weight, order, namespace))
            order += 1
    if not in_body:
        raise ValueError(f"{path}: missing dictionary body marker (...)")
    if sort_mode == "by_weight":
        entries.sort(key=lambda entry: (-entry.weight, entry.source_order))
    return entries, order


@lru_cache(maxsize=None)
def _read_source_cached(source: DictionarySource, fingerprint: bytes) -> tuple[Entry, ...]:
    entries, _ = read_rime_dictionary(source.path, 0, source.namespace)
    return tuple(entries)


@lru_cache(maxsize=None)
def _collect_entries_cached(
    sources: tuple[DictionarySource, ...],
    fingerprint: tuple[bytes, ...],
) -> tuple[Entry, ...]:
    result: list[Entry] = []
    seen: set[tuple[str, str]] = set()
    order = 0
    for source, digest in zip(sources, fingerprint, strict=True):
        for cached in _read_source_cached(source, digest):
            entry = Entry(
                cached.text,
                cached.code,
                cached.weight,
                order,
                cached.namespace,
            )
            order += 1
            key = (entry.code, entry.text)
            if key in seen:
                continue
            seen.add(key)
            result.append(entry)
    return tuple(result)


def _sha256_file(path: Path) -> bytes:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").digest()


def collect_entries(root: Path = ROOT, profile: str = "full") -> list[Entry]:
    sources = tuple(read_manifest(root.resolve(), profile))
    fingerprint = tuple(_sha256_file(source.path) for source in sources)
    return list(_collect_entries_cached(sources, fingerprint))


def prefix_fanout(
    entries: Iterable[Entry],
    lengths: Iterable[int] = range(1, 7),
) -> dict[int, int]:
    """Return the largest subtree size at each prefix length."""
    counters = {length: Counter() for length in lengths}
    for entry in entries:
        for length in counters:
            if len(entry.code) >= length:
                counters[length][entry.code[:length]] += 1
    return {
        length: max(counter.values(), default=0)
        for length, counter in counters.items()
    }


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
SaveAutoPhraseAfter=-1
Learning=False
ExactMatch=False
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


def _zip_write(
    archive: zipfile.ZipFile,
    name: str,
    data: bytes,
    compresslevel: int = 9,
) -> None:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data, compresslevel=compresslevel)


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
    entries: list[Entry] | None = None,
    compresslevel: int = 6,
) -> list[Path]:
    entries_by_profile = {
        profile: entries if entries is not None else collect_entries(root, profile)
        for profile in PROFILES
    }
    tables = {
        profile: render_table(profile_entries).encode("utf-8")
        for profile, profile_entries in entries_by_profile.items()
    }
    config = render_config().encode("utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    binaries = {profile: compiled_dictionary for profile in PROFILES}
    if compiler:
        resolved_compiler = shutil.which(compiler) or (
            compiler if Path(compiler).is_file() else None
        )
        if resolved_compiler is None:
            raise FileNotFoundError(f"libime_tabledict not found: {compiler}")
        def compile_profile(profile: str) -> tuple[str, bytes]:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp = Path(temp_dir)
                source = temp / "eosphoros.txt"
                destination = temp / "eosphoros.main.dict"
                source.write_bytes(tables[profile])
                subprocess.run([resolved_compiler, str(source), str(destination)], check=True)
                return profile, destination.read_bytes()

        with ThreadPoolExecutor(max_workers=len(PROFILES)) as executor:
            binaries.update(executor.map(compile_profile, PROFILES))

    archives: list[Path] = []
    for profile in PROFILES:
        for platform in ("linux", "macos", "android"):
            if platform == "linux" and binaries[profile] is None:
                raise ValueError("Linux package requires --compiler (libime_tabledict)")
            destination = output_dir / archive_name(f"eosphoros-fcitx5-{platform}.zip", profile)
            with zipfile.ZipFile(destination, "w") as archive:
                if platform == "linux":
                    _zip_write(archive, "inputmethod/eosphoros.conf", config, compresslevel)
                    _zip_write(
                        archive,
                        "table/eosphoros.main.dict",
                        binaries[profile] or b"",
                        compresslevel,
                    )
                else:
                    _zip_write(archive, "eosphoros.conf", config, compresslevel)
                    _zip_write(archive, "eosphoros.txt", tables[profile], compresslevel)
                if platform != "android":
                    for name, path in _theme_files(root, platform):
                        _zip_write(archive, name, path.read_bytes(), compresslevel)
            archives.append(destination)
    print(
        "Fcitx5 Table: "
        + ", ".join(
            f"{profile}={len(profile_entries)}"
            for profile, profile_entries in entries_by_profile.items()
        )
    )
    return archives


def check(root: Path = ROOT) -> None:
    entries = collect_entries(root)
    if len(entries) < 1_300_000:
        raise ValueError("Fcitx5 Table dictionary is unexpectedly incomplete")
    expected = {
        ("jxjdoo", "晨星键道"),
        ("hyefa", "婚姻圣召"),
        ("zqquo", "赞主曲"),
        ("ihello", "hello"),
        ("uhao", "好"),
        ("vhr", "一"),
        ("ohz", "好"),
    }
    actual = {(entry.code, entry.text) for entry in entries}
    missing = sorted(expected - actual)
    if missing:
        raise ValueError(f"Fcitx5 Table is missing smoke rows: {missing}")
    limits = {1: 100_000, 2: 8_000, 3: 600}
    normal_fanout = prefix_fanout(
        (entry for entry in entries if entry.namespace == ""),
        limits,
    )
    oversized = {
        length: normal_fanout[length]
        for length, limit in limits.items()
        if normal_fanout[length] > limit
    }
    if oversized:
        raise ValueError(f"normal KeyTao prefix fanout regressed: {oversized}")
    config = render_config()
    for required in (
        "Addon=table",
        "NoMatchAutoSelectLength=1",
        "Learning=False",
        "SaveAutoPhraseAfter=-1",
        "Length=63",
    ):
        haystack = config if required != "Length=63" else render_table(entries[:1])
        if required not in haystack:
            raise ValueError(f"missing Fcitx5 Table setting: {required}")
    print(
        f"Fcitx5 Table check passed: {len(entries)} unique rows; "
        f"normal max fanout 1/2/3={normal_fanout[1]}/"
        f"{normal_fanout[2]}/{normal_fanout[3]}"
    )


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
