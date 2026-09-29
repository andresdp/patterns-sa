import os
import sys
import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from adept import PatternAnalysis
from adept.core.models import Box

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
sys.path.insert(0, FL_DIR)

from preprocess_fl_clients import preprocess_fl  # noqa: E402

# Optional categorical parameter: raw values are strings ('zlib', ...) or NaN
FLAG_PARAM = "Message Compressor Alg"


class TestBoxEncoding(unittest.TestCase):
    """Box limits on optional categorical parameters live in 0/1 presence-flag space."""

    @classmethod
    def setUpClass(cls):
        cls.session = PatternAnalysis(os.path.join(FL_DIR, "FLsystem_split.json"))
        cls.session.load(preprocessor=preprocess_fl)
        cls.session.create_tradeoffs(method="discretization", objectives=["best_val_f1", "avg_total_time"])
        cls.session.split_data(test_size=0.3, verbose=False)
        target = cls.session.get_tradeoffs(non_empty=True)[0].name
        cls.box = Box(
            limits={FLAG_PARAM: {"min": 0.5, "max": 1.0}, "Client Selector Value": {"min": 1.8, "max": 2.0}},
            target_tradeoff=target,
        )

    def test_encoding_matches_selected_rows(self):
        X = self.session.experiments_df
        encoded = self.session._encode_for_boxes(X)
        self.assertEqual(set(encoded[FLAG_PARAM].unique()), {0.0, 1.0})
        self.assertEqual((encoded[FLAG_PARAM] == 1.0).sum(), X[FLAG_PARAM].notna().sum())

    def test_box_diagnostics_accept_categorical_flag_limits(self):
        for subset in ("test", "all"):
            self.session.show_box_diagnostics(box=self.box, subset=subset, figsize=(8, 5))
            plt.close("all")

    def test_discovery_with_only_categorical_parameters(self):
        # Dataset bounds must be computed on the encoded flags, not fail on string columns
        boxes = self.session.discover_scenarios(
            self.box.target_tradeoff, method="prim", standardize=True, parameters=[FLAG_PARAM]
        )
        for box in boxes:
            self.assertEqual(box.dataset_bounds.get(FLAG_PARAM), {"min": 0.0, "max": 1.0})

    def test_box_matrices_accept_categorical_flag_limits(self):
        impact = self.session.get_tradeoff_impact_matrix([self.box], subset="test")
        coverage = self.session.get_tradeoff_coverage_matrix([self.box], subset="test")
        self.assertEqual(list(impact.index), [self.box.target_tradeoff])
        self.assertEqual(list(coverage.index), [self.box.target_tradeoff])


if __name__ == "__main__":
    unittest.main()
