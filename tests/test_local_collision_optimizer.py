from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path

from tools.optimize_local_collisions import collision_metrics, plan_moves


ROOT = Path(__file__).resolve().parents[1]


class LocalCollisionOptimizerTests(unittest.TestCase):
    def test_local_dictionaries_have_no_safe_pending_moves(self) -> None:
        rows, moves = plan_moves(ROOT)
        self.assertEqual(moves, ())

        before, after = collision_metrics(rows, moves)
        self.assertEqual(before, after)
        self.assertLess(before / len(rows), 0.049)

    def test_optimizer_does_not_touch_user_or_specialty_dictionaries(self) -> None:
        _, moves = plan_moves(ROOT)
        touched = Counter(move.row.filename for move in moves)
        self.assertEqual(touched, Counter())


if __name__ == "__main__":
    unittest.main()
