"""Numeric encoding of categorical and optional parameters (adept/utils/feature_encoding.py)."""
import contextlib
import io
import os
import sys
import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from adept import PatternAnalysis
from adept.core.models import Box, Parameter
from adept.utils.feature_encoding import FeatureEncoder

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
sys.path.insert(0, FL_DIR)

from preprocess_fl_clients import preprocess_fl  # noqa: E402


def param(name, optional=False):
    return Parameter(name=name, level="system", type="lever", optional=optional)


class TestFeatureEncoder(unittest.TestCase):
    def setUp(self):
        self.train = pd.DataFrame({
            "model": ["squeezenet", "cnn", "cnn", "squeezenet"],   # categorical, always present
            "alg": ["zlib", None, "lz4", None],                      # categorical, optional
            "rate": [0.5, np.nan, 0.7, np.nan],                      # numeric, optional
            "n": [1.0, 2.0, 3.0, 4.0],                               # numeric, required
            "policy": ["a", "b", "a", "b"],                          # not a declared parameter
        })
        self.params = [param("model"), param("alg", optional=True), param("rate", optional=True), param("n")]
        self.encoder = FeatureEncoder.fit(self.train, self.params)

    def test_categories_become_sorted_codes_with_zero_for_not_selected(self):
        out = self.encoder.transform(self.train)
        self.assertEqual(list(out["model"]), [2.0, 1.0, 1.0, 2.0])
        self.assertEqual(list(out["alg"]), [2.0, 0.0, 1.0, 0.0])

    def test_numeric_optional_nan_becomes_sentinel_below_minimum(self):
        out = self.encoder.transform(self.train)
        sentinel = self.encoder.sentinels["rate"]
        self.assertLess(sentinel, 0.5)
        self.assertEqual(list(out["rate"]), [0.5, sentinel, 0.7, sentinel])

    def test_required_numeric_and_undeclared_columns_are_untouched(self):
        out = self.encoder.transform(self.train)
        pd.testing.assert_series_equal(out["n"], self.train["n"])
        pd.testing.assert_series_equal(out["policy"], self.train["policy"])

    def test_unseen_category_is_encoded_as_not_selected(self):
        out = self.encoder.transform(pd.DataFrame({"model": ["resnet"], "alg": ["gzip"]}))
        self.assertEqual(list(out["model"]), [0.0])
        self.assertEqual(list(out["alg"]), [0.0])

    def test_interpreting_encoded_limits(self):
        self.assertEqual(self.encoder.decode_categories("model", {"min": 1.5, "max": 2.0}), ["squeezenet"])
        self.assertTrue(self.encoder.includes_not_selected("alg", {"min": -np.inf, "max": 0.5}))
        self.assertFalse(self.encoder.includes_not_selected("alg", {"min": 0.5, "max": 2.0}))
        self.assertFalse(self.encoder.includes_not_selected("model", {"min": -np.inf, "max": 2.0}))  # not optional
        sentinel = self.encoder.sentinels["rate"]
        self.assertTrue(self.encoder.includes_not_selected("rate", {"min": sentinel, "max": 0.6}))


class TestReadableLimits(unittest.TestCase):
    def test_categorical_limits_become_category_sets(self):
        box = Box(
            limits={"Model": {"min": 1.5, "max": 2.0}, "rate": {"min": -np.inf, "max": 0.6}},
            categorical_levels={"Model": ["CNN 16k", "squeezenet1_1"]},
            includes_na={"rate": True},
        )
        self.assertEqual(box.readable_limits(), {
            "Model": {"in": ["squeezenet1_1"]},
            "rate": {"min": -np.inf, "max": 0.6, "includes_na": True},
        })

    def test_not_selected_is_listed_for_categorical_limits(self):
        box = Box(limits={"alg": {"min": -np.inf, "max": 0.5}},
                  categorical_levels={"alg": ["zlib"]}, includes_na={"alg": True})
        self.assertEqual(box.readable_limits(), {"alg": {"in": ["(not selected)"], "includes_na": True}})

    def test_describe_limits_uses_original_values(self):
        box = Box(
            limits={
                "Model": {"min": 1.5, "max": 2.0},
                "alg": {"min": -np.inf, "max": 1.0},
                "rate": {"min": 0.35, "max": 0.6},
                "n": {"min": 2.0, "max": np.inf},
                "m": {"min": 1.0, "max": 3.0},
            },
            categorical_levels={"Model": ["CNN 16k", "squeezenet1_1"], "alg": ["zlib"]},
            includes_na={"alg": True, "rate": True},
        )
        self.assertEqual(box.describe_limits(), {
            "Model": "{squeezenet1_1}",
            "alg": "{(not selected), zlib}",
            "rate": "(not selected) or <= 0.60",
            "n": ">= 2.00",
            "m": "[1.00, 3.00]",
        })


class TestCategoricalParametersInAnalysis(unittest.TestCase):
    """FL: `Model` (categorical, always present) and optional pattern parameters."""

    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            cls.session = PatternAnalysis(os.path.join(FL_DIR, "FLsystem_split.json"))
            cls.session.load(preprocessor=preprocess_fl)
            cls.session.create_tradeoffs(method="discretization", objectives=["best_val_f1", "avg_total_time"])
            cls.session.split_data(test_size=0.3, verbose=False)
            cls.cart = [b for b in cls.session.discover_scenarios(
                method="cart", standardize=True, parameters=["Model", "Client Selector Value"]) if not b.is_empty()]

    def test_model_is_scored(self):
        with contextlib.redirect_stdout(io.StringIO()):
            scores = self.session.compute_feature_scores(include_constraints=True, subset="train")
        self.assertIn("Model", scores.index)
        self.assertEqual(scores["best_val_f1"].idxmax(), "Model")

    def test_boxes_decode_categories(self):
        self.assertTrue(self.cart)
        for box in self.cart:
            self.assertEqual(box.categorical_levels["Model"], ["CNN 16k", "squeezenet1_1"])
            self.assertTrue(set(box.readable_limits()["Model"]["in"]) <= {"CNN 16k", "squeezenet1_1"})

    def test_includes_na_matches_the_encoded_not_selected_value(self):
        encoder = self.session._fit_box_encoder()
        flags = []
        for box in self.cart:
            expected = encoder.includes_not_selected("Client Selector Value", box.limits["Client Selector Value"])
            self.assertEqual(box.includes_na.get("Client Selector Value", False), expected)
            flags.append(expected)
        self.assertIn(True, flags)  # client selector OFF regions exist in this data

    def test_diagnostics_hatch_not_selected_region(self):
        box = next(b for b in self.cart if b.includes_na.get("Client Selector Value"))
        fig = self.session.show_box_diagnostics(box=box, subset="all", figsize=(8, 5))
        hatches = [c.get_hatch() for ax in fig.axes for c in ax.collections + ax.patches]
        plt.close(fig)
        self.assertIn("///", hatches)

    @staticmethod
    def _figure_texts(fig):
        texts = [t.get_text() for ax in fig.axes for t in ax.texts]
        for ax in fig.axes:
            texts += [t.get_text() for t in ax.get_xticklabels() + ax.get_yticklabels()]
        return texts

    def test_diagnostics_show_original_values(self):
        box = next(b for b in self.cart if b.includes_na.get("Client Selector Value"))
        fig = self.session.show_box_diagnostics(box=box, subset="all", figsize=(8, 5))
        fig.canvas.draw()
        texts = self._figure_texts(fig)
        plt.close(fig)
        self.assertTrue(any("CNN 16k" in t or "squeezenet1_1" in t for t in texts), texts)
        self.assertTrue(any("(not selected)" in t or t == "N/A" for t in texts), texts)

    def test_diagnostics_can_show_codes(self):
        box = next(b for b in self.cart if b.includes_na.get("Client Selector Value"))
        fig = self.session.show_box_diagnostics(box=box, subset="all", figsize=(8, 5),
                                                show_original_values=False)
        fig.canvas.draw()
        texts = self._figure_texts(fig)
        plt.close(fig)
        self.assertFalse(any("squeezenet1_1" in t or "CNN 16k" in t or t == "N/A" for t in texts), texts)

    def test_impact_summary_shows_original_values(self):
        box = self.cart[0]
        fig = self.session.show_box_impact_objective_space(
            box=box, x_metric="best_val_f1", y_metric="avg_total_time", show_box_summary=True)
        texts = [t.get_text() for ax in fig.axes for t in ax.texts] + [t.get_text() for t in fig.texts]
        plt.close(fig)
        summary = next(t for t in texts if "Constraints:" in t)
        self.assertIn("Model: {", summary)


if __name__ == "__main__":
    unittest.main()
