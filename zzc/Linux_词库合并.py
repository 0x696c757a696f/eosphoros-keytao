#!/usr/bin/env python3
"""Legacy Linux entry point for the shared eosphoros ZZZC merge core."""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("eosphoros_词库合并.py")), run_name="__main__")
