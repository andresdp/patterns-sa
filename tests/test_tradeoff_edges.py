"""Fixed bin edges for discretization tradeoffs (DataProcessor._discretize(edges=...))."""
import contextlib
import io
import unittest

import pandas as pd

from adept.analysis.discretization import DataProcessor


class TestFixedEdges(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"acc": [0.1, 0.4, 0.5, 0.9], "time": [10.0, 20.0, 30.0, 40.0]})

    def test_edges_are_used_as_given(self):
        labeled, schemes = DataProcessor._discretize(
            self.df, all_labels={"acc": ["S", "L"]}, edges={"acc": [0.0, 0.45, 1.0]})
        self.assertEqual(list(labeled["acc"].astype(str)), ["S", "S", "L", "L"])
        acc = next(s for s in schemes if s.objective_name == "acc")
        self.assertEqual([(b.label, b.min_value, b.max_value) for b in acc.bins],
                         [("S", 0.0, 0.45), ("L", 0.45, 1.0)])
        # Objectives without edges keep the detected equal-width bins
        time = next(s for s in schemes if s.objective_name == "time")
        self.assertEqual(len(time.bins), 3)

    def test_lowest_edge_is_inclusive(self):
        labeled, _ = DataProcessor._discretize(self.df[["acc"]], edges={"acc": [0.1, 0.5, 0.9]})
        self.assertEqual(list(labeled["acc"].astype(str)), ["level_1", "level_1", "level_1", "level_2"])

    def test_values_outside_the_edges_are_reported(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            labeled, _ = DataProcessor._discretize(self.df[["acc"]], edges={"acc": [0.2, 0.6]})
        self.assertIn("2 run(s) of 'acc' fall outside the fixed edges", out.getvalue())
        self.assertEqual(int(labeled["acc"].isna().sum()), 2)

    def test_invalid_edges(self):
        with self.assertRaises(ValueError):
            DataProcessor._discretize(self.df[["acc"]], edges={"acc": [0.5, 0.2]})
        with self.assertRaises(ValueError):
            DataProcessor._discretize(self.df[["acc"]], all_labels={"acc": ["S", "M", "L"]},
                                      edges={"acc": [0.0, 1.0]})


if __name__ == "__main__":
    unittest.main()
