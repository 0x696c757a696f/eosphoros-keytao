#!/usr/bin/env python3
"""Combine Yong's maintained UI assets with Eosphoros colors and icons."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def prepare(base_skin: Path, destination: Path) -> None:
    if not (base_skin / "skin.ini").is_file():
        raise FileNotFoundError(f"Yong base skin is incomplete: {base_skin}")
    shared = [
        path
        for path in base_skin.iterdir()
        if path.is_file() and path.name not in {"skin.ini", "skin0.ini", "skin1.ini", "skin2.ini"}
    ]
    if not shared:
        raise FileNotFoundError(f"Yong base skin has no shared UI assets: {base_skin}")

    destination.mkdir(parents=True, exist_ok=True)
    for source_theme in sorted((ROOT / "packaging" / "yong" / "skins").iterdir()):
        if not source_theme.is_dir():
            continue
        target = destination / source_theme.name
        target.mkdir(parents=True, exist_ok=True)
        for source in shared:
            shutil.copy2(source, target / source.name)
        shutil.copy2(source_theme / "skin.ini", target / "skin.ini")
        shutil.copy2(ROOT / "assets" / "eosphoros-tray-active.ico", target / "tray1.ico")
        shutil.copy2(ROOT / "assets" / "eosphoros-tray-inactive.ico", target / "tray2.ico")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-skin", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    prepare(args.base_skin.resolve(), args.destination.resolve())
    print(f"Prepared Yong desktop skins: {args.destination.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
