from __future__ import annotations

import unittest

from tools.run_test_shard import shard_index


class TestShardingTests(unittest.TestCase):
    def test_partition_is_stable_and_complete(self) -> None:
        test_ids = [f"tests.sample.SampleTests.test_{index}" for index in range(100)]
        first = [shard_index(test_id, 3) for test_id in test_ids]
        second = [shard_index(test_id, 3) for test_id in test_ids]

        self.assertEqual(first, second)
        self.assertEqual(set(first), {0, 1, 2})
        self.assertTrue(all(0 <= index < 3 for index in first))


if __name__ == "__main__":
    unittest.main()
