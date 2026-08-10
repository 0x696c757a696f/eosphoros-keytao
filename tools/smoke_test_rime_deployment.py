#!/usr/bin/env python3
"""Build the packaged core with a real rime_deployer and verify artifacts."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build_platform_packages import common_runtime_files


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_BUILD_OUTPUTS = (
    "default.yaml",
    "eosphoros.schema.yaml",
    "eosphoros.prism.bin",
    "eosphoros.extended.table.bin",
)


def stage_runtime(source_root: Path, destination: Path) -> None:
    for source in common_runtime_files(source_root):
        relative = source.relative_to(source_root)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def validate_outputs(user_dir: Path) -> list[str]:
    build_dir = user_dir / "build"
    return [name for name in REQUIRED_BUILD_OUTPUTS if not (build_dir / name).is_file()]


def smoke_test(deployer: str, source_root: Path = ROOT) -> None:
    with tempfile.TemporaryDirectory(prefix="eosphoros-rime-") as temporary:
        user_dir = Path(temporary) / "user"
        user_dir.mkdir()
        stage_runtime(source_root, user_dir)
        result = subprocess.run(
            [deployer, "--build", str(user_dir)],
            cwd=user_dir,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        if result.returncode:
            raise RuntimeError(
                "rime_deployer failed\n"
                + (result.stdout or "")
                + (result.stderr or "")
            )
        missing = validate_outputs(user_dir)
        if missing:
            raise RuntimeError("rime_deployer omitted: " + ", ".join(missing))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deployer", default=shutil.which("rime_deployer"))
    args = parser.parse_args()
    if not args.deployer:
        parser.error("rime_deployer was not found; install librime-bin")
    smoke_test(args.deployer)
    print("Real librime deployment smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
