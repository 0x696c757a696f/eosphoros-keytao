from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class YongTableTests(unittest.TestCase):
    def test_builds_complete_static_namespaced_table_and_dazhu(self) -> None:
        from tools.build_yong_table import build

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            table = output / "eosphoros.txt"
            dazhu = output / "dazhu.txt"
            count = build(ROOT, table, dazhu)

            self.assertGreater(count, 1_300_000)
            text = table.read_text(encoding="gb18030")
            self.assertIn("len=63\n", text)
            self.assertIn("nsort=1\n", text)
            self.assertIn("\nihello hello\n", text)
            self.assertIn("\nuhao 好\n", text)
            self.assertIn("\nvhr 一\n", text)
            self.assertIn("\nohz 好\n", text)
            self.assertIn("ihello\thello", dazhu.read_text(encoding="utf-8"))

    def test_desktop_yong_configuration_loads_large_static_table_off_ui_thread(self) -> None:
        for relative in ("packaging/yong/yong.ini", "packaging/yong/android/yong.ini"):
            config = (ROOT / relative).read_text(encoding="utf-8-sig")
            self.assertIn("thread=1", config)
            self.assertIn("auto_move=0", config)
            self.assertIn("auto_add=0", config)


if __name__ == "__main__":
    unittest.main()
