#!/usr/bin/env python3
"""Safely adapt reviewed rime-txjx changes onto the local xmjd6 namespace."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "tools" / "upstream_code.lock.json"
MANIFEST_PATH = ROOT / "tools" / "txjx_adaptation_manifest.json"
THIRD_PARTY_PATH = ROOT / "THIRD_PARTY.md"
BLOCKED_EXIT = 20


@dataclass(frozen=True)
class MergeResult:
    text: str
    conflicted: bool


def adapt_lua_text(text: str) -> str:
    """Translate upstream Lua identifiers without changing xmjd6 behavior."""
    adapted = adapt_project_text(text)
    adapted = re.sub(
        r'require\((["\'])common\.', r'require(\1xmjd6.common.', adapted
    )
    adapted = re.sub(
        r'require\((["\'])input\.', r'require(\1xmjd6.input.', adapted
    )
    adapted = re.sub(
        r'require\((["\'])zzc\.', r'require(\1xmjd6.zzc.', adapted
    )
    for module in (
        "typing_stats",
        "typing_stats_processor",
        "typing_stats_translator",
    ):
        adapted = adapted.replace(
            f'require("xmjd6_{module}")', f'require("xmjd6.{module}")'
        ).replace(f"require('xmjd6_{module}')", f"require('xmjd6.{module}')")
    adapted = re.sub(
        r'require\((["\'])xmjd6_(?!typing_stats)',
        r'require(\1xmjd6.xmjd6_',
        adapted,
    )
    return adapted


def adapt_project_text(text: str) -> str:
    """Translate upstream project names in non-Lua source files."""
    attribution_marker = "__UPSTREAM_PROJECT_ATTRIBUTION__"
    adapted = text.replace("rime-txjx", attribution_marker)
    adapted = adapted.replace("天行键", "星猫键道")
    adapted = adapted.replace("TXJX", "xmjd6").replace("Txjx", "xmjd6")
    return adapted.replace("txjx", "xmjd6").replace(
        attribution_marker, "rime-txjx"
    )


def has_upstream_namespace_residue(text: str) -> bool:
    """Allow source attribution while rejecting live txjx identifiers."""
    without_attribution = re.sub(r"(?i)rime-txjx", "", text)
    return "txjx" in without_attribution.lower()


def merge_adapted_text(local: str, base: str, upstream: str) -> MergeResult:
    """Three-way merge adapted text, reporting overlap instead of overwriting it."""
    with tempfile.TemporaryDirectory(prefix="xmjd6-txjx-merge-") as temp_dir:
        root = Path(temp_dir)
        local_path = root / "local"
        base_path = root / "base"
        upstream_path = root / "upstream"
        local_path.write_text(local, encoding="utf-8", newline="\n")
        base_path.write_text(base, encoding="utf-8", newline="\n")
        upstream_path.write_text(upstream, encoding="utf-8", newline="\n")
        result = subprocess.run(
            [
                "git",
                "merge-file",
                "-p",
                str(local_path),
                str(base_path),
                str(upstream_path),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            check=False,
        )
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or "git merge-file failed")
    return MergeResult(text=result.stdout, conflicted=result.returncode == 1)


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=check,
    )


def _remote_commit(repository: str, ref: str) -> str:
    result = subprocess.run(
        ["git", "ls-remote", repository, ref],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=True,
    )
    rows = [line.split() for line in result.stdout.splitlines() if line.strip()]
    if len(rows) != 1:
        raise RuntimeError(f"cannot resolve {ref} from {repository}")
    return rows[0][0]


def _ensure_commit(root: Path, repository: str, commit: str) -> None:
    found = _git(root, "cat-file", "-e", f"{commit}^{{commit}}", check=False)
    if found.returncode == 0:
        return
    _git(root, "fetch", "--no-tags", "--depth=1", repository, commit)


def _try_show_text(root: Path, commit: str, path: str) -> str | None:
    result = _git(root, "show", f"{commit}:{path}", check=False)
    return result.stdout if result.returncode == 0 else None


def _changed_paths(root: Path, base: str, target: str) -> list[str]:
    result = _git(root, "diff", "--name-only", base, target, "--")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _transform(text: str, name: str) -> str:
    if name == "lua_namespace":
        return adapt_lua_text(text)
    if name == "project_namespace":
        return adapt_project_text(text)
    if name == "identity":
        return text
    raise ValueError(f"unknown transform: {name}")


def _is_critical_unmapped(path: str) -> bool:
    if path.startswith("lua/") and path.endswith(".lua"):
        return True
    if not path.startswith("zzc/"):
        return False
    name = Path(path).name
    return path.endswith(".py") or name.startswith(("Linux_", "Mac_", "iOS_"))


def _update_metadata(root: Path, lock: dict[str, Any], target: str) -> None:
    source = lock["upstreams"]["rime-txjx"]
    source["commit"] = target
    lock["updated"] = date.today().isoformat()
    (root / LOCK_PATH.relative_to(ROOT)).write_text(
        json.dumps(lock, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    third_party_path = root / THIRD_PARTY_PATH.relative_to(ROOT)
    third_party = third_party_path.read_text(encoding="utf-8")
    third_party, count = re.subn(
        r"(?m)^- Integrated commit: `[0-9a-f]{40}`$",
        f"- Integrated commit: `{target}`",
        third_party,
    )
    if count != 1:
        raise RuntimeError("cannot update rime-txjx commit in THIRD_PARTY.md")
    third_party_path.write_text(third_party, encoding="utf-8", newline="\n")


def adapt_repository(
    root: Path = ROOT,
    *,
    target: str | None = None,
    write: bool = False,
    update_lock: bool = False,
) -> dict[str, Any]:
    lock_path = root / LOCK_PATH.relative_to(ROOT)
    manifest_path = root / MANIFEST_PATH.relative_to(ROOT)
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source = lock["upstreams"]["rime-txjx"]
    repository = source["repository"]
    base = source["commit"]
    target = target or _remote_commit(repository, source["ref"])

    report: dict[str, Any] = {
        "base_commit": base,
        "target_commit": target,
        "update_available": base != target,
        "changed_upstream_paths": [],
        "adapted_targets": [],
        "unchanged_targets": [],
        "conflicts": [],
        "unmapped_paths": [],
        "critical_unmapped_paths": [],
        "windows_exe_rebuild_required": False,
        "written": False,
        "lock_updated": False,
        "blocked": False,
    }
    if base == target:
        return report

    _ensure_commit(root, repository, base)
    _ensure_commit(root, repository, target)
    ancestry = _git(root, "merge-base", "--is-ancestor", base, target, check=False)
    if ancestry.returncode != 0:
        report["conflicts"].append(
            {
                "source": "<upstream-history>",
                "target": "<commit-lock>",
                "reason": "upstream_history_is_not_a_descendant_of_locked_commit",
            }
        )
        report["blocked"] = True
        return report
    changed_paths = _changed_paths(root, base, target)
    report["changed_upstream_paths"] = changed_paths
    mappings = {item["source"]: item for item in manifest["mappings"]}
    report["unmapped_paths"] = [path for path in changed_paths if path not in mappings]
    report["critical_unmapped_paths"] = [
        path for path in report["unmapped_paths"] if _is_critical_unmapped(path)
    ]

    pending: dict[Path, str] = {}
    for upstream_path in changed_paths:
        mapping = mappings.get(upstream_path)
        if not mapping:
            continue
        target_path = root / mapping["target"]
        if not target_path.is_file():
            report["conflicts"].append(
                {"source": upstream_path, "target": mapping["target"], "reason": "missing_local_target"}
            )
            continue
        base_source = _try_show_text(root, base, upstream_path)
        upstream_source = _try_show_text(root, target, upstream_path)
        if base_source is None or upstream_source is None:
            report["conflicts"].append(
                {
                    "source": upstream_path,
                    "target": mapping["target"],
                    "reason": (
                        "mapped_source_added"
                        if base_source is None
                        else "mapped_source_deleted"
                    ),
                }
            )
            continue
        transform = mapping["transform"]
        base_text = _transform(base_source, transform)
        upstream_text = _transform(upstream_source, transform)
        local_text = target_path.read_text(encoding="utf-8")
        merged = merge_adapted_text(local_text, base_text, upstream_text)
        if merged.conflicted:
            report["conflicts"].append(
                {"source": upstream_path, "target": mapping["target"], "reason": "overlapping_changes"}
            )
            continue
        if has_upstream_namespace_residue(merged.text):
            report["conflicts"].append(
                {"source": upstream_path, "target": mapping["target"], "reason": "upstream_namespace_residue"}
            )
            continue
        if merged.text == local_text:
            report["unchanged_targets"].append(mapping["target"])
            continue
        pending[target_path] = merged.text
        report["adapted_targets"].append(mapping["target"])
        if mapping.get("rebuild_windows_exe"):
            report["windows_exe_rebuild_required"] = True
            report["conflicts"].append(
                {
                    "source": upstream_path,
                    "target": mapping["target"],
                    "reason": "release_only_windows_executable_rebuild",
                }
            )

    blocked = bool(report["conflicts"] or report["critical_unmapped_paths"])
    report["blocked"] = blocked
    if write and not blocked:
        for path, content in pending.items():
            path.write_text(content, encoding="utf-8", newline="\n")
        report["written"] = bool(pending)
        if update_lock:
            _update_metadata(root, lock, target)
            report["lock_updated"] = True
    return report


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", help="upstream commit; defaults to the locked ref HEAD")
    parser.add_argument("--write", action="store_true", help="write conflict-free adaptations")
    parser.add_argument(
        "--update-lock",
        action="store_true",
        help="update the lock and THIRD_PARTY.md; requires --write",
    )
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.update_lock and not args.write:
        print("--update-lock requires --write", file=sys.stderr)
        return 2
    try:
        report = adapt_repository(
            target=args.target,
            write=args.write,
            update_lock=args.update_lock,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"rime-txjx adaptation failed: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"rime-txjx: {report['base_commit']} -> {report['target_commit']}")
        print(f"adapted targets: {len(report['adapted_targets'])}")
        print(f"conflicts: {len(report['conflicts'])}")
        print(f"critical unmapped paths: {len(report['critical_unmapped_paths'])}")
    return BLOCKED_EXIT if report.get("blocked") else 0


if __name__ == "__main__":
    raise SystemExit(main())
