#!/usr/bin/env python3
"""Apply an original Eosphoros palette to a user-supplied Yong Android skin."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THEMES = ROOT / "packaging" / "yong" / "android" / "themes"
START = "/* eosphoros-theme:start */"
END = "/* eosphoros-theme:end */"
REQUIRED = ("keyboard.html", "keyboard.css")


def safe_extract(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as source:
        for item in source.infolist():
            target = (destination / item.filename).resolve()
            if destination.resolve() not in (target, *target.parents):
                raise ValueError(f"unsafe ZIP member: {item.filename}")
        source.extractall(destination)


def find_skin_root(root: Path) -> Path:
    candidates = [root, *(path for path in root.iterdir() if path.is_dir())]
    matches = [path for path in candidates if all((path / name).is_file() for name in REQUIRED)]
    if len(matches) != 1:
        raise ValueError("base skin must contain keyboard.html and keyboard.css at one root")
    return matches[0]


def replace_theme(css: str, theme: str) -> str:
    block = f"{START}\n{theme.rstrip()}\n{END}"
    if START in css or END in css:
        if css.count(START) != 1 or css.count(END) != 1:
            raise ValueError("damaged existing Eosphoros theme block")
        before, rest = css.split(START, 1)
        _, after = rest.split(END, 1)
        return f"{before.rstrip()}\n\n{block}{after}"
    return f"{css.rstrip()}\n\n{block}\n"


def write_zip(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source).as_posix())


def build(base: Path, theme_name: str, output: Path) -> None:
    theme_path = THEMES / f"{theme_name}.css"
    if not theme_path.is_file():
        choices = ", ".join(path.stem for path in sorted(THEMES.glob("*.css")))
        raise ValueError(f"unknown theme {theme_name!r}; choose: {choices}")

    with tempfile.TemporaryDirectory() as temp:
        extracted = Path(temp) / "base"
        extracted.mkdir()
        if base.is_dir():
            shutil.copytree(base, extracted, dirs_exist_ok=True)
        elif zipfile.is_zipfile(base):
            safe_extract(base, extracted)
        else:
            raise ValueError("base skin must be a directory or ZIP archive")

        skin_root = find_skin_root(extracted)
        css_path = skin_root / "keyboard.css"
        css = css_path.read_text(encoding="utf-8-sig")
        theme = theme_path.read_text(encoding="utf-8")
        css_path.write_text(replace_theme(css, theme), encoding="utf-8", newline="\n")
        write_zip(skin_root, output)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply a compact Eosphoros palette to a Yong Android skin ZIP/directory."
    )
    parser.add_argument("base", type=Path, help="current compatible Yong Android skin")
    parser.add_argument("--theme", choices=("dawn", "night"), default="dawn")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.base, args.theme, args.output)
    print(f"Built {args.output} with Eosphoros {args.theme} palette")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
