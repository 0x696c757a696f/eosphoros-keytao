from __future__ import annotations

from dataclasses import dataclass

try:
    from tools.dictionary_profiles import PROFILES, archive_name
except ModuleNotFoundError:
    from dictionary_profiles import PROFILES, archive_name


PROFILE_TITLES = {
    "full": "完整版 Full",
    "standard": "标准版 Standard",
    "lite": "精简版 Lite",
}
PROFILE_LINK_LABELS = {
    "full": "Full",
    "standard": "Standard",
    "lite": "Lite",
}
STANDALONE_ASSETS = (
    "eosphoros-fcitx5-android-themes.zip",
    "eosphoros-yong-desktop-skins.zip",
)


@dataclass(frozen=True)
class ReleasePackage:
    platform: str
    engine: str
    base_archive: str
    theme_label: str
    theme_target: str
    theme_is_archive: bool = True


PACKAGES = (
    ReleasePackage(
        "通用",
        "Rime",
        "eosphoros-rime.zip",
        "按所用前端选择",
        "#-各平台皮肤与样式",
        False,
    ),
    ReleasePackage(
        "Windows",
        "小狼毫 Weasel",
        "eosphoros-weasel-windows-rime.zip",
        "包内提供",
        "eosphoros-weasel-windows-rime-full.zip",
    ),
    ReleasePackage(
        "Windows",
        "玉兔毫 Rabbit",
        "eosphoros-rabbit-windows-rime.zip",
        "包内提供",
        "eosphoros-rabbit-windows-rime-full.zip",
    ),
    ReleasePackage(
        "Windows",
        "小小输入法 Yong",
        "eosphoros-yong-windows.zip",
        "包内提供；单独下载",
        "eosphoros-yong-desktop-skins.zip",
    ),
    ReleasePackage(
        "macOS",
        "鼠须管 Squirrel",
        "eosphoros-squirrel-macos-rime.zip",
        "包内提供",
        "eosphoros-squirrel-macos-rime-full.zip",
    ),
    ReleasePackage(
        "macOS",
        "Fcitx5 + Rime",
        "eosphoros-fcitx5-macos-rime.zip",
        "包内提供",
        "eosphoros-fcitx5-macos-rime-full.zip",
    ),
    ReleasePackage(
        "macOS",
        "Fcitx5 原生 Table",
        "eosphoros-fcitx5-macos.zip",
        "包内提供",
        "eosphoros-fcitx5-macos-full.zip",
    ),
    ReleasePackage(
        "Android",
        "同文 Trime",
        "eosphoros-trime-android.zip",
        "包内提供",
        "eosphoros-trime-android-full.zip",
    ),
    ReleasePackage(
        "Android",
        "Fcitx5 + Rime",
        "eosphoros-fcitx5-android-rime.zip",
        "独立主题包",
        "eosphoros-fcitx5-android-themes.zip",
    ),
    ReleasePackage(
        "Android",
        "Fcitx5 原生 Table",
        "eosphoros-fcitx5-android.zip",
        "独立主题包",
        "eosphoros-fcitx5-android-themes.zip",
    ),
    ReleasePackage(
        "Android",
        "小小输入法 Yong",
        "eosphoros-yong-android.zip",
        "包内提供",
        "eosphoros-yong-android-full.zip",
    ),
    ReleasePackage(
        "iOS",
        "元书输入法",
        "eosphoros-yuanshu-ios-rime.zip",
        ".cskin 包内提供",
        "eosphoros-yuanshu-ios-rime-full.zip",
    ),
    ReleasePackage(
        "iOS",
        "仓输入法 Hamster",
        "eosphoros-hamster-ios-rime.zip",
        ".hskin 包内提供",
        "eosphoros-hamster-ios-rime-full.zip",
    ),
    ReleasePackage(
        "Linux",
        "Fcitx5 + Rime",
        "eosphoros-fcitx5-linux-rime.zip",
        "包内提供",
        "eosphoros-fcitx5-linux-rime-full.zip",
    ),
    ReleasePackage(
        "Linux",
        "Fcitx5 原生 Table",
        "eosphoros-fcitx5-linux.zip",
        "包内提供",
        "eosphoros-fcitx5-linux-full.zip",
    ),
    ReleasePackage(
        "Linux",
        "小小输入法 Yong",
        "eosphoros-yong-linux.zip",
        "包内提供；单独下载",
        "eosphoros-yong-desktop-skins.zip",
    ),
)


def profile_assets() -> tuple[str, ...]:
    return tuple(
        archive_name(package.base_archive, profile)
        for package in PACKAGES
        for profile in PROFILES
    )


def _link(label: str, target: str) -> str:
    return f"[{label}]({target})"


def render_download_table(
    repository_url: str,
    download_base: str,
    *,
    compact_headers: bool,
) -> str:
    repository_url = repository_url.rstrip("/")
    download_base = download_base.rstrip("/")
    profile_headers = [
        PROFILE_TITLES[profile].split()[0]
        if compact_headers
        else PROFILE_TITLES[profile]
        for profile in PROFILES
    ]
    lines = [
        "| 平台 | 输入法 / 引擎 | "
        + " | ".join(profile_headers)
        + " | 主题 / 皮肤 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for package in PACKAGES:
        profile_links = [
            _link(
                PROFILE_LINK_LABELS[profile] if compact_headers else "下载",
                f"{download_base}/{archive_name(package.base_archive, profile)}",
            )
            for profile in PROFILES
        ]
        theme_target = (
            f"{download_base}/{package.theme_target}"
            if package.theme_is_archive
            else f"{repository_url}{package.theme_target}"
        )
        if package.theme_label == "包内提供；单独下载":
            embedded_target = (
                f"{download_base}/{archive_name(package.base_archive, 'full')}"
            )
            theme = (
                f"{_link('包内提供', embedded_target)}；"
                f"{_link('单独下载', theme_target)}"
            )
        else:
            theme = _link(package.theme_label, theme_target)
        lines.append(
            f"| {package.platform} | {package.engine} | "
            + " | ".join(profile_links)
            + f" | {theme} |"
        )
    return "\n".join(lines)
