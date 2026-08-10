#!/usr/bin/env python3
"""Build the packaged core with a real rime_deployer and verify artifacts."""

from __future__ import annotations

import argparse
import os
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
    "eosphoros.schema.yaml",
    "eosphoros.extended.table.bin",
    "eosphoros.extended.prism.bin",
)
DEFAULT_SHARED_DATA_DIR = Path("/usr/share/rime-data")


def stage_runtime(source_root: Path, destination: Path) -> None:
    for source in common_runtime_files(source_root):
        relative = source.relative_to(source_root)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def validate_outputs(user_dir: Path) -> list[str]:
    build_dir = user_dir / "build"
    return [name for name in REQUIRED_BUILD_OUTPUTS if not (build_dir / name).is_file()]


def deployer_command(
    deployer: str, user_dir: Path, shared_data_dir: Path | None
) -> list[str]:
    command = [
        deployer,
        "--compile",
        str(user_dir / "eosphoros.schema.yaml"),
        str(user_dir),
    ]
    if shared_data_dir is not None:
        command.append(str(shared_data_dir))
    return command


def smoke_test(
    deployer: str,
    source_root: Path = ROOT,
    shared_data_dir: Path | None = None,
) -> None:
    if shared_data_dir is not None and not shared_data_dir.is_dir():
        raise FileNotFoundError(f"Rime shared data directory is missing: {shared_data_dir}")
    with tempfile.TemporaryDirectory(prefix="eosphoros-rime-") as temporary:
        user_dir = Path(temporary) / "user"
        user_dir.mkdir()
        stage_runtime(source_root, user_dir)
        (user_dir / "build").mkdir()
        environment = os.environ.copy()
        environment["GLOG_logtostderr"] = "1"
        result = subprocess.run(
            deployer_command(deployer, user_dir, shared_data_dir),
            cwd=user_dir,
            env=environment,
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
            available = sorted(
                path.relative_to(user_dir / "build").as_posix()
                for path in (user_dir / "build").rglob("*")
                if path.is_file()
            )
            raise RuntimeError(
                "rime_deployer omitted: "
                + ", ".join(missing)
                + "; available: "
                + ", ".join(available)
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deployer", default=shutil.which("rime_deployer"))
    parser.add_argument(
        "--shared-data-dir",
        type=Path,
        default=DEFAULT_SHARED_DATA_DIR if DEFAULT_SHARED_DATA_DIR.is_dir() else None,
        help="Rime prelude/shared-data directory (for example /usr/share/rime-data)",
    )
    args = parser.parse_args()
    if not args.deployer:
        parser.error("rime_deployer was not found; install librime-bin")
    try:
        smoke_test(args.deployer, shared_data_dir=args.shared_data_dir)
    except Exception as exc:
        # GitHub exposes workflow annotations even when the full log requires
        # authentication, so retain the actionable deployer output there.
        annotation = (
            str(exc).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        )
        print(f"::error title=Rime deployment failed::{annotation}", file=sys.stderr)
        raise
    print("Real librime deployment smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
