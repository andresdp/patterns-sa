"""Per-instance column aggregation (adept/utils/aggregation.py) and its dataspace declaration."""
import contextlib
import io
import os
import sys
import unittest

import numpy as np
import pandas as pd

from adept import PatternAnalysis
from adept.utils.aggregation import aggregate_instance_columns

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
sys.path.insert(0, FL_DIR)

from preprocess_fl_clients import preprocess_fl  # noqa: E402


class TestAggregateInstanceColumns(unittest.TestCase):
    def setUp(self):
        # Three nodes (not "clients"), with a field that is NaN for one node
        self.df = pd.DataFrame({
            "Node 1 Load": [1.0, 4.0], "Node 2 Load": [3.0, 4.0], "Node 3 Load": [5.0, np.nan],
            "Node 1 Zone": ["a", "a"], "Node 2 Zone": ["b", "a"], "Node 3 Zone": ["b", "a"],
            "Other": [7, 8],
        })
        self.pattern = r"^Node (\d+) (.+)$"

    def test_numeric_statistics_skip_nan(self):
        out = aggregate_instance_columns(self.df, self.pattern, numeric=["mean", "std", "min", "max"])
        self.assertEqual(list(out["Load Mean"]), [3.0, 4.0])
        self.assertEqual(list(out["Load Min"]), [1.0, 4.0])
        self.assertEqual(list(out["Load Max"]), [5.0, 4.0])
        self.assertAlmostEqual(out["Load Std"].iloc[0], 2.0)
        self.assertEqual(out["Load Std"].iloc[1], 0.0)

    def test_categorical_diversity_and_originals_kept(self):
        out = aggregate_instance_columns(self.df, self.pattern)
        self.assertEqual(list(out["Zone Diversity"]), [2, 1])
        self.assertTrue(set(self.df.columns) <= set(out.columns))

    def test_fields_filter_and_no_match(self):
        out = aggregate_instance_columns(self.df, self.pattern, fields=["Zone"])
        self.assertNotIn("Load Mean", out.columns)
        self.assertIs(aggregate_instance_columns(self.df, r"^Client (\d+) (.+)$"), self.df)

    def test_unknown_statistic_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown aggregation statistics"):
            aggregate_instance_columns(self.df, self.pattern, numeric=["variance"])


class TestDeclaredAggregation(unittest.TestCase):
    """FL's spec declares its client aggregation, so no preprocessor is needed."""

    def test_declared_aggregation_matches_the_fl_preprocessor(self):
        json_path = os.path.join(FL_DIR, "FLsystem_split.json")
        with contextlib.redirect_stdout(io.StringIO()):
            declared = PatternAnalysis(json_path)
            declared.load()
            hooked = PatternAnalysis(json_path)
            hooked.load(preprocessor=preprocess_fl)
        pd.testing.assert_frame_equal(declared.experiments_df, hooked.experiments_df)
        pd.testing.assert_frame_equal(declared.outcomes_df, hooked.outcomes_df)
        self.assertIn("CPU Mean", declared.experiments_df.columns)
        self.assertIn("CPU Usage Avg Mean", declared.outcomes_df.columns)


if __name__ == "__main__":
    unittest.main()
