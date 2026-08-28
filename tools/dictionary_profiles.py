from __future__ import annotations

from pathlib import Path


PROFILES = ("full", "standard", "lite")
PROFILE_LABELS = {
    "full": "完整版",
    "standard": "标准版",
    "lite": "精简版",
}

STANDARD_EXCLUDED_DICTIONARIES = (
    "dicts/eosphoros/eosphoros.fjcy.dict.yaml",
)
LITE_EXCLUDED_DICTIONARIES = STANDARD_EXCLUDED_DICTIONARIES + (
    "dicts/eosphoros/eosphoros.ice.dict.yaml",
    "dicts/eosphoros/eosphoros.catholicism.dict.yaml",
    "dicts/eosphoros/eosphoros.protestantism.dict.yaml",
    "dicts/eosphoros/eosphoros.orthodoxy.dict.yaml",
    "dicts/eosphoros/eosphoros.oriental.dict.yaml",
    "dicts/eosphoros/eosphoros.assyrian.dict.yaml",
    "dicts/eosphoros/eosphoros.wanxiang.yaopin.dict.yaml",
    "dicts/eosphoros/eosphoros.wanxiang.yixue.dict.yaml",
    "dicts/eosphoros/eosphoros.wanxiang.huaxue.dict.yaml",
    "dicts/eosphoros/eosphoros.wanxiang.diming.dict.yaml",
    "dicts/eosphoros/eosphoros.wanxiang.mingren.dict.yaml",
    "dicts/eosphoros/eosphoros.wanxiang.taifeng.dict.yaml",
    "dicts/eosphoros/eosphoros.wanxiang.jichu.dict.yaml",
)
PROFILE_EXCLUDED_DICTIONARIES = {
    "full": (),
    "standard": STANDARD_EXCLUDED_DICTIONARIES,
    "lite": LITE_EXCLUDED_DICTIONARIES,
}
PROFILE_INDEX_FILENAMES = tuple(f"eosphoros.{profile}.dict.yaml" for profile in PROFILES)


def validate_profile(profile: str) -> str:
    if profile not in PROFILES:
        raise ValueError(f"unsupported dictionary profile: {profile}")
    return profile


def excluded_dictionaries(profile: str) -> tuple[str, ...]:
    return PROFILE_EXCLUDED_DICTIONARIES[validate_profile(profile)]


def profile_dictionary_name(profile: str) -> str:
    return f"eosphoros.{validate_profile(profile)}"


def profiled_custom_config(path: Path, profile: str) -> bytes:
    dictionary = profile_dictionary_name(profile)
    text = path.read_text(encoding="utf-8-sig")
    marker = "patch:\n"
    if marker not in text:
        raise ValueError(f"custom config has no patch node: {path}")
    return text.replace(
        marker,
        f"{marker}  translator/dictionary: {dictionary}\n",
        1,
    ).encode("utf-8")


def includes_dictionary(relative: str | Path, profile: str) -> bool:
    normalized = Path(relative).as_posix()
    return normalized not in excluded_dictionaries(profile)


def archive_name(base_name: str, profile: str) -> str:
    validate_profile(profile)
    stem = base_name.removesuffix(".zip")
    return f"{stem}-{profile}.zip"


def profiled_dictionary_index(path: Path, profile: str) -> bytes:
    excluded_imports = {
        relative.removesuffix(".dict.yaml")
        for relative in excluded_dictionaries(profile)
    }
    lines = [
        line
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip().removeprefix("- ") not in excluded_imports
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")
