#!/usr/bin/env python3
"""Build Fcitx5 Linux and macOS themes from the desktop Rime palettes."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "fcitx5"


def rime_color(value: int, fallback: str = "#000000FF") -> str:
    """Convert Rime AABBGGRR/BGR integers to Fcitx RRGGBBAA."""
    if not isinstance(value, int):
        return fallback
    if value <= 0xFFFFFF:
        alpha = 0xFF
        blue = (value >> 16) & 0xFF
        green = (value >> 8) & 0xFF
        red = value & 0xFF
    else:
        alpha = (value >> 24) & 0xFF
        blue = (value >> 16) & 0xFF
        green = (value >> 8) & 0xFF
        red = value & 0xFF
    return f"#{red:02X}{green:02X}{blue:02X}{alpha:02X}"


def first_color(scheme: dict[str, Any], *keys: str, default: str) -> str:
    for key in keys:
        value = scheme.get(key)
        if isinstance(value, int):
            return rime_color(value)
    return default


def palette(scheme: dict[str, Any]) -> dict[str, str]:
    text = first_color(scheme, "candidate_text_color", "text_color", default="#000000FF")
    background = first_color(scheme, "candidate_back_color", "back_color", default="#FFFFFFFF")
    highlighted_text = first_color(
        scheme,
        "hilited_candidate_text_color",
        "hilited_text_color",
        default=text,
    )
    highlighted_background = first_color(
        scheme,
        "hilited_candidate_back_color",
        "hilited_back_color",
        default=background,
    )
    return {
        "background": background,
        "border": first_color(scheme, "border_color", default=background),
        "text": text,
        "preedit": first_color(scheme, "hilited_text_color", "text_color", default=text),
        "highlight_text": highlighted_text,
        "highlight_background": highlighted_background,
        "label": first_color(scheme, "label_color", default=text),
        "highlight_label": first_color(
            scheme, "hilited_label_color", default=highlighted_text
        ),
        "comment": first_color(scheme, "comment_text_color", default=text),
        "highlight_comment": first_color(
            scheme, "hilited_comment_text_color", default=highlighted_text
        ),
    }


def desktop_schemes() -> list[dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    origin: dict[str, list[str]] = {}
    # Squirrel is preferred for shared IDs because its current format is the
    # closest desktop counterpart to both Fcitx frontends. Weasel contributes
    # every Windows-only palette.
    for source_name in ("squirrel", "weasel"):
        document = yaml.safe_load(
            (ROOT / f"{source_name}.yaml").read_text(encoding="utf-8-sig")
        )
        for scheme_id, scheme in document["preset_color_schemes"].items():
            if not isinstance(scheme, dict):
                continue
            origin.setdefault(scheme_id, []).append(source_name)
            if scheme_id not in sources or source_name == "squirrel":
                sources[scheme_id] = scheme

    return [
        {
            "id": scheme_id,
            "name": str(scheme.get("name", scheme_id)),
            "author": str(scheme.get("author", "xmjd6 desktop theme collection")),
            "sources": origin[scheme_id],
            "colors": palette(scheme),
        }
        for scheme_id, scheme in sources.items()
    ]


def linux_theme(item: dict[str, Any]) -> str:
    c = item["colors"]
    sources = ", ".join(item["sources"])
    return f"""[Metadata]
Name={item['name']}
Version=1
Author={item['author']}
Description=xmjd6 desktop palette replica ({sources})
ScaleWithDPI=True

[InputPanel]
NormalColor={c['text']}
HighlightColor={c['preedit']}
HighlightBackgroundColor={c['highlight_background']}
HighlightCandidateColor={c['highlight_text']}
CandidateLabelColor={c['label']}
HighlightCandidateLabelColor={c['highlight_label']}
CandidateCommentColor={c['comment']}
HighlightCandidateCommentColor={c['highlight_comment']}
PageButtonAlignment=Last Candidate

[InputPanel/TextMargin]
Left=5
Right=5
Top=5
Bottom=5

[InputPanel/ContentMargin]
Left=2
Right=2
Top=2
Bottom=2

[InputPanel/Background]
Color={c['background']}
BorderColor={c['border']}
BorderWidth=1

[InputPanel/Background/Margin]
Left=2
Right=2
Top=2
Bottom=2

[InputPanel/Highlight]
Color={c['highlight_background']}

[InputPanel/Highlight/Margin]
Left=5
Right=5
Top=5
Bottom=5

[Menu]
NormalColor={c['text']}
HighlightCandidateColor={c['highlight_text']}

[Menu/Background]
Color={c['background']}
BorderColor={c['border']}
BorderWidth=1

[Menu/Highlight]
Color={c['highlight_background']}

[Menu/Separator]
Color={c['border']}
"""


def macos_mode(c: dict[str, str], *, same_as_light: bool | None) -> str:
    same_line = (
        "" if same_as_light is None else f"SameWithLightMode={'True' if same_as_light else 'False'}\n"
    )
    return f"""OverrideDefault=True
{same_line}HighlightColor={c['highlight_background']}
HighlightHoverColor={c['highlight_background']}
HighlightTextColor={c['highlight_text']}
HighlightTextPressColor={c['highlight_text']}
HighlightLabelColor={c['highlight_label']}
HighlightCommentColor={c['highlight_comment']}
HighlightMarkColor={c['highlight_text']}
PanelColor={c['background']}
TextColor={c['text']}
LabelColor={c['label']}
CommentColor={c['comment']}
PagingButtonColor={c['text']}
DisabledPagingButtonColor={c['comment']}
AuxColor={c['preedit']}
PreeditColorPreCaret={c['preedit']}
PreeditColorCaret={c['highlight_text']}
PreeditColorPostCaret={c['preedit']}
BorderColor={c['border']}
DividerColor={c['border']}
"""


def macos_theme(light: dict[str, str], dark: dict[str, str] | None = None) -> str:
    dark_colors = dark or light
    return f"""[LightMode]
{macos_mode(light, same_as_light=None)}
[DarkMode]
{macos_mode(dark_colors, same_as_light=dark is None)}
[Typography]
Layout=Vertical
WritingMode=Horizontal top-bottom
TypographyAwarenessForIM=True

[Background]
KeepPanelColorWhenHasImage=True
Blur=System
Shadow=True

[Size]
OverrideDefault=True
BorderWidth=1
BorderRadius=8
Margin=0
HighlightRadius=6
TopPadding=5
RightPadding=7
BottomPadding=5
LeftPadding=7
LabelTextGap=6
VerticalMinWidth=200
HorizontalDividerWidth=1
"""


def write_tree(destination: Path) -> None:
    schemes = desktop_schemes()
    linux_root = destination / "linux" / "themes"
    macos_root = destination / "macos" / "themes"
    linux_root.mkdir(parents=True, exist_ok=True)
    macos_root.mkdir(parents=True, exist_ok=True)

    for item in schemes:
        linux_dir = linux_root / f"xmjd6-{item['id']}"
        linux_dir.mkdir()
        (linux_dir / "theme.conf").write_text(linux_theme(item), encoding="utf-8")
        (macos_root / f"xmjd6-{item['id']}.conf").write_text(
            macos_theme(item["colors"]), encoding="utf-8"
        )

    by_id = {item["id"]: item for item in schemes}
    (macos_root / "xmjd6-auto.conf").write_text(
        macos_theme(by_id["CatLight"]["colors"], by_id["CatDark"]["colors"]),
        encoding="utf-8",
    )
    manifest = {
        "generated": "2026-08-09",
        "desktop_precedence": ["squirrel", "weasel"],
        "themes": [
            {key: item[key] for key in ("id", "name", "author", "sources")}
            for item in schemes
        ],
    }
    (destination / "themes.yaml").write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def files(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as temp_dir:
        generated = Path(temp_dir) / "fcitx5"
        write_tree(generated)
        if args.check:
            if files(generated) != files(OUTPUT):
                print("Fcitx5 themes are stale; run tools/build_fcitx5_themes.py")
                return 1
            print(f"Fcitx5 themes are current ({len(desktop_schemes())} palettes)")
            return 0

        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)
        shutil.copytree(generated, OUTPUT)
    print(f"Built {len(desktop_schemes())} Fcitx5 palettes for Linux and macOS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
