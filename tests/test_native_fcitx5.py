from __future__ import annotations

import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "native" / "fcitx5-eosphoros"


def read_u32(data: bytes, offset: int) -> tuple[int, int]:
    return struct.unpack_from("<I", data, offset)[0], offset + 4


def read_string(data: bytes, offset: int) -> tuple[str, int]:
    size, offset = read_u32(data, offset)
    return data[offset : offset + size].decode("ascii"), offset + size


class NativeFcitx5Tests(unittest.TestCase):
    def test_native_runtime_boundary_and_fcitx_metadata(self) -> None:
        source_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((NATIVE / "src").glob("*"))
            if path.is_file()
        )
        cmake = (NATIVE / "CMakeLists.txt").read_text(encoding="utf-8")
        runtime = (source_text + cmake).lower()
        for forbidden in ("fcitx5-rime", "librime", "rime/schema", "opencc"):
            self.assertNotIn(forbidden, runtime)
        self.assertIn("public fcitx::InputMethodEngineV2", source_text)
        self.assertIn("EosphorosEngine", source_text)
        self.assertIn("EosphorosContext", source_text)
        self.assertIn("FactoryFor<State>", source_text)

        input_method = (NATIVE / "data/eosphoros-native.conf.in").read_text(
            encoding="utf-8"
        )
        addon = (NATIVE / "data/eosphoros-native-addon.conf.in").read_text(
            encoding="utf-8"
        )
        self.assertIn("Name=晨星键道（原生）", input_method)
        self.assertIn("Addon=eosphoros-native", input_method)
        self.assertIn("Library=libeosphoros-native", addon)

    def test_release_and_rime_packages_exclude_native_sources(self) -> None:
        from tools.build_platform_packages import package_files

        for archive, paths in package_files(ROOT).items():
            relative = {path.relative_to(ROOT).as_posix() for path in paths}
            self.assertFalse(
                any(path.startswith("native/") for path in relative), archive
            )
        master = (ROOT / ".github/workflows/package-master.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("!native/**", master)

    def test_dictionary_compiler_embeds_schema_topup_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "native.dict"
            result = subprocess.run(
                [
                    sys.executable,
                    str(NATIVE / "tools/build_dictionary.py"),
                    "--schema",
                    str(ROOT / "eosphoros.schema.yaml"),
                    "--input",
                    str(NATIVE / "tests/fixtures/minimal.dict.yaml"),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = output.read_bytes()

        self.assertEqual(data[:8], b"EOSDICT2")
        version, offset = read_u32(data, 8)
        self.assertEqual(version, 2)
        topup_this, offset = read_string(data, offset)
        topup_with, offset = read_string(data, offset)
        min_length, offset = read_u32(data, offset)
        max_length, offset = read_u32(data, offset)
        auto_clear, offset = read_u32(data, offset)
        topup_command, offset = read_u32(data, offset)
        page_size, offset = read_u32(data, offset)
        count, _ = read_u32(data, offset)
        self.assertEqual(topup_this, "bcdefghjklmnpqrstwxyz")
        self.assertEqual(topup_with, "avuio;")
        self.assertEqual((min_length, max_length), (4, 6))
        self.assertEqual((auto_clear, topup_command), (1, 0))
        self.assertEqual(page_size, 5)
        self.assertEqual(count, 24)


if __name__ == "__main__":
    unittest.main()
