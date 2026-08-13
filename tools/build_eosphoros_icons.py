#!/usr/bin/env python3
"""Derive Yong state icons without changing the canonical Eosphoros icon."""

from __future__ import annotations

import argparse
import io
from pathlib import Path

from PIL import Image, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SIZES = (16, 20, 24, 32, 40, 48, 64, 128, 256)


def inactive_icon(source: Path) -> bytes:
    """Keep the original star silhouette and only dim its monochrome values."""

    with Image.open(source) as canonical:
        base = canonical.convert("RGBA")
    frames: list[Image.Image] = []
    for size in SIZES:
        frame = base.resize((size, size), Image.Resampling.LANCZOS)
        alpha = frame.getchannel("A")
        gray = ImageEnhance.Contrast(frame.convert("L")).enhance(0.70)
        gray = ImageEnhance.Brightness(gray).enhance(0.72)
        dimmed = Image.merge("RGBA", (gray, gray, gray, alpha))
        frames.append(dimmed)
    output = io.BytesIO()
    frames[-1].save(
        output,
        format="ICO",
        sizes=[(size, size) for size in SIZES],
    )
    return output.getvalue()


def outputs() -> dict[Path, bytes]:
    # This tracked file is the canonical, original elongated morning-star icon.
    # Never regenerate or restyle it here.
    active = (ROOT / "eosphoros.ico").read_bytes()
    return {
        ROOT / "assets" / "eosphoros-tray-active.ico": active,
        ROOT / "eosphoros-ascii.ico": inactive_icon(ROOT / "eosphoros.ico"),
        ROOT / "assets" / "eosphoros-tray-inactive.ico": inactive_icon(
            ROOT / "eosphoros.ico"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale: list[Path] = []
    for path, content in outputs().items():
        if args.check:
            if not path.is_file() or path.read_bytes() != content:
                stale.append(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if stale:
        print("Stale Eosphoros icons: " + ", ".join(str(path) for path in stale))
        return 1
    print("Eosphoros desktop icons are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
