from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tools.release_catalog import render_download_table
except ModuleNotFoundError:
    from release_catalog import render_download_table


def build_release_notes(
    repository_url: str,
    release_tag: str,
    run_url: str,
    run_label: str,
    changelog: str,
) -> str:
    repository_url = repository_url.rstrip("/")
    download_base = f"{repository_url}/releases/download/{release_tag}"
    table = render_download_table(
        repository_url,
        download_base,
        compact_headers=True,
    )
    changelog = changelog.strip() or "- 本次构建没有可列出的提交。"
    return (
        "## Release Notes\n"
        f"- [如何使用]({repository_url}#如何使用)\n"
        f"- 构建：[{run_label}]({run_url})\n\n"
        "## 平台与词库版本\n\n"
        f"{table}\n\n"
        "## Changelog\n"
        f"{changelog}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-url", required=True)
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--run-url", required=True)
    parser.add_argument("--run-label", required=True)
    parser.add_argument("--changelog-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("release-notes.md"))
    args = parser.parse_args()
    notes = build_release_notes(
        args.repository_url,
        args.release_tag,
        args.run_url,
        args.run_label,
        args.changelog_file.read_text(encoding="utf-8"),
    )
    args.output.write_text(notes, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
