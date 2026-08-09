from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class TxjxAdapterTests(unittest.TestCase):
    def make_upstream_fixture(
        self,
        *,
        source_path: str,
        base_text: str,
        upstream_text: str,
        mapping: dict[str, object] | None,
    ) -> tuple[Path, str, str]:
        temp = tempfile.TemporaryDirectory(prefix="xmjd6-txjx-adapter-test-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(
            ["git", "-C", str(root), "config", "user.name", "test"], check=True
        )
        subprocess.run(
            ["git", "-C", str(root), "config", "user.email", "test@example.invalid"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(root), "config", "core.autocrlf", "false"],
            check=True,
        )
        source = root / source_path
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(base_text, encoding="utf-8", newline="\n")
        subprocess.run(["git", "-C", str(root), "add", source_path], check=True)
        subprocess.run(
            ["git", "-C", str(root), "commit", "-q", "-m", "base"], check=True
        )
        base = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()
        source.write_text(upstream_text, encoding="utf-8", newline="\n")
        subprocess.run(["git", "-C", str(root), "add", source_path], check=True)
        subprocess.run(
            ["git", "-C", str(root), "commit", "-q", "-m", "upstream"],
            check=True,
        )
        target = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()

        (root / "tools").mkdir(exist_ok=True)
        lock = {
            "updated": "2026-08-08",
            "upstreams": {
                "rime-txjx": {
                    "repository": str(root),
                    "ref": "HEAD",
                    "commit": base,
                }
            },
        }
        (root / "tools" / "upstream_code.lock.json").write_text(
            json.dumps(lock), encoding="utf-8"
        )
        (root / "tools" / "txjx_adaptation_manifest.json").write_text(
            json.dumps({"schema": 1, "mappings": [mapping] if mapping else []}),
            encoding="utf-8",
        )
        (root / "THIRD_PARTY.md").write_text(
            f"- Integrated commit: `{base}`\n", encoding="utf-8"
        )
        return root, base, target

    def test_manifest_has_unique_existing_local_targets(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads(
            (root / "tools" / "txjx_adaptation_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        sources = [item["source"] for item in manifest["mappings"]]
        targets = [item["target"] for item in manifest["mappings"]]

        self.assertEqual(len(sources), len(set(sources)))
        self.assertEqual(len(targets), len(set(targets)))
        for target in targets:
            self.assertTrue((root / target).is_file(), target)

    def test_lua_namespace_transform_uses_xmjd6_modules(self) -> None:
        from tools.adapt_txjx_upstream import adapt_lua_text

        upstream = '''-- 天行键
local core = require("zzc.txjx_zzc_core")
local config = require("common.txjx_config")
local ext = require("txjx_ext_core")
return { core = core, config = config, ext = ext, id = "txjx" }
'''
        adapted = adapt_lua_text(upstream)

        self.assertIn('require("xmjd6.zzc.xmjd6_zzc_core")', adapted)
        self.assertIn('require("xmjd6.common.xmjd6_config")', adapted)
        self.assertIn('require("xmjd6.xmjd6_ext_core")', adapted)
        self.assertIn('id = "xmjd6"', adapted)
        self.assertIn("星猫键道", adapted)
        self.assertNotIn("txjx", adapted.lower())

    def test_project_transform_preserves_local_xmjd6_naming(self) -> None:
        from tools.adapt_txjx_upstream import (
            adapt_project_text,
            has_upstream_namespace_residue,
        )

        adapted = adapt_project_text(
            'SCHEMA = "txjx"\nPATH = "lua/txjx"\nTITLE = "天行键"\n'
            '# source: wzxmer/rime-txjx\n'
        )

        self.assertEqual(
            adapted,
            'SCHEMA = "xmjd6"\nPATH = "lua/xmjd6"\nTITLE = "星猫键道"\n'
            '# source: wzxmer/rime-txjx\n',
        )
        self.assertFalse(has_upstream_namespace_residue(adapted))
        self.assertTrue(has_upstream_namespace_residue('SCHEMA = "txjx"\n'))

    def test_three_way_merge_keeps_local_features_and_upstream_fix(self) -> None:
        from tools.adapt_txjx_upstream import merge_adapted_text

        middle = "\n".join(f"local keep_{index} = {index}" for index in range(8))
        base = f'local behavior = "old"\n{middle}\nreturn behavior\n'
        upstream = f'local behavior = "fixed"\n{middle}\nreturn behavior\n'
        local = (
            f'local behavior = "old"\n{middle}\n'
            "local xmjd6_only = true\nreturn behavior\n"
        )

        result = merge_adapted_text(local, base, upstream)

        self.assertFalse(result.conflicted)
        self.assertIn('local behavior = "fixed"', result.text)
        self.assertIn("local xmjd6_only = true", result.text)

    def test_three_way_merge_stops_on_overlapping_changes(self) -> None:
        from tools.adapt_txjx_upstream import merge_adapted_text

        result = merge_adapted_text(
            'local behavior = "xmjd6"\n',
            'local behavior = "old"\n',
            'local behavior = "upstream"\n',
        )

        self.assertTrue(result.conflicted)
        self.assertIn("<<<<<<<", result.text)

    def test_repository_adapter_merges_and_advances_lock_atomically(self) -> None:
        from tools.adapt_txjx_upstream import adapt_repository

        root, _, target = self.make_upstream_fixture(
            source_path="lua/txjx_core.lua",
            base_text='local behavior = "old"\nlocal gap = true\nreturn behavior\n',
            upstream_text='local behavior = "fixed"\nlocal gap = true\nreturn behavior\n',
            mapping={
                "source": "lua/txjx_core.lua",
                "target": "lua/xmjd6/xmjd6_core.lua",
                "transform": "lua_namespace",
            },
        )
        local = root / "lua" / "xmjd6" / "xmjd6_core.lua"
        local.parent.mkdir(parents=True)
        local.write_text(
            'local behavior = "old"\nlocal gap = true\nlocal xmjd6_only = true\nreturn behavior\n',
            encoding="utf-8",
        )

        report = adapt_repository(
            root, target=target, write=True, update_lock=True
        )

        self.assertFalse(report["blocked"])
        self.assertIn('local behavior = "fixed"', local.read_text(encoding="utf-8"))
        self.assertIn("local xmjd6_only = true", local.read_text(encoding="utf-8"))
        lock = json.loads(
            (root / "tools" / "upstream_code.lock.json").read_text(encoding="utf-8")
        )
        self.assertEqual(lock["upstreams"]["rime-txjx"]["commit"], target)

    def test_unknown_source_blocks_without_advancing_lock(self) -> None:
        from tools.adapt_txjx_upstream import adapt_repository

        root, base, target = self.make_upstream_fixture(
            source_path="lua/new_upstream_module.lua",
            base_text="return false\n",
            upstream_text="return true\n",
            mapping=None,
        )

        report = adapt_repository(
            root, target=target, write=True, update_lock=True
        )

        self.assertTrue(report["blocked"])
        self.assertFalse(report["written"])
        self.assertFalse(report["lock_updated"])
        lock = json.loads(
            (root / "tools" / "upstream_code.lock.json").read_text(encoding="utf-8")
        )
        self.assertEqual(lock["upstreams"]["rime-txjx"]["commit"], base)


if __name__ == "__main__":
    unittest.main()
