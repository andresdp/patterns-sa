"""Focused slices of the FL dataset (federatedlearning/fl_slices.py, make_slice_notebooks.py)."""
import contextlib
import io
import os
import sys
import unittest

import pandas as pd

from adept import PatternAnalysis

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
SPEC = os.path.join(FL_DIR, "naive", "FLsystem_split.json")
sys.path.insert(0, FL_DIR)

import fl_slices  # noqa: E402

OBJECTIVES = {"final_val_accuracy": ["S", "M", "L"], "avg_total_time": ["S", "M", "L"]}


# Bin edges detected on the full dataset, as fixed in analysis-fl.ipynb (TRADEOFF_EDGES)
EDGES = {"final_val_accuracy": [0.21230, 0.33613, 0.45997, 0.58380],
         "avg_total_time": [17.261, 195.682, 374.104, 552.525]}


def load(slice_name="all", include_baseline=False, edges=None):
    session = PatternAnalysis(SPEC)
    with contextlib.redirect_stdout(io.StringIO()):
        session.load(preprocessor=fl_slices.slice_filter(slice_name, include_baseline))
        session.create_tradeoffs(method="discretization", labels=OBJECTIVES, edges=edges)
    return session


def bin_edges(session):
    return {sc.objective_name: [(b.label, b.min_value, b.max_value) for b in sc.bins] for sc in session.schemes}


class TestSliceFilter(unittest.TestCase):
    def test_config_ids(self):
        self.assertEqual(fl_slices.config_id(), "OFF,OFF,OFF")
        self.assertEqual(fl_slices.config_id(["hdh"]), "OFF,OFF,ON")
        self.assertEqual(fl_slices.config_id(["client_selector"]), "ON,OFF,OFF")
        with self.assertRaises(ValueError):
            fl_slices.config_id(["unknown"])

    def test_all_keeps_every_run(self):
        self.assertEqual(len(load("all").raw_df), 32)

    def test_slices_keep_only_their_configurations(self):
        expected = {"baseline": {"OFF,OFF,OFF"}, "client_selector": {"ON,OFF,OFF"},
                    "message_compressor": {"OFF,ON,OFF"}, "hdh": {"OFF,OFF,ON"}}
        for name, configs in expected.items():
            with self.subTest(slice=name):
                session = load(name)
                self.assertEqual(set(session.raw_df["config_id"]), configs)

    def test_include_baseline(self):
        session = load("hdh", include_baseline=True)
        self.assertEqual(set(session.raw_df["config_id"]), {"OFF,OFF,OFF", "OFF,OFF,ON"})

    def test_unknown_slice(self):
        with self.assertRaises(ValueError):
            fl_slices.slice_filter("nope")

    def test_target_stress_keeps_every_enabled_pattern_at_requested_level(self):
        rows = pd.DataFrame([
            {"config_id": "ON,OFF,OFF", "pattern_stress": "CS=50%", "low_spec_percentage": 50, "partition_seed": 1},
            {"config_id": "OFF,ON,OFF", "pattern_stress": "MC=50%", "delay_percentage": 50, "partition_seed": 1},
            {"config_id": "OFF,OFF,ON", "pattern_stress": "HDH=50%", "non_iid_percentage": 50, "partition_seed": 1},
            {"config_id": "ON,ON,OFF", "pattern_stress": "CS=50%; MC=50%", "low_spec_percentage": 50, "delay_percentage": 50, "partition_seed": 1},
            {"config_id": "ON,OFF,ON", "pattern_stress": "CS=50%; HDH=25%", "low_spec_percentage": 50, "non_iid_percentage": 25, "partition_seed": 1},
            {"config_id": "OFF,OFF,OFF", "pattern_stress": "none", "partition_seed": 1},
        ])

        with contextlib.redirect_stdout(io.StringIO()):
            selected = fl_slices.slice_filter(target_stress=50)(rows)
        self.assertEqual(
            set(selected["config_id"]),
            {"ON,OFF,OFF", "OFF,ON,OFF", "OFF,OFF,ON", "ON,ON,OFF"},
        )

    def test_target_stress_validates_range_and_parsed_fields(self):
        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            fl_slices.slice_filter(target_stress=101)
        rows = pd.DataFrame({"config_id": ["ON,OFF,OFF"]})
        with self.assertRaisesRegex(ValueError, "parsed feature"):
            fl_slices.slice_filter(target_stress=50)(rows)

    def test_pattern_combination_support_includes_absent_combinations(self):
        rows = pd.DataFrame({
            "config_id": ["ON,OFF,OFF", "ON,ON,OFF", "ON,ON,OFF"],
            "partition_seed": [1, 1, 2],
        })
        support = fl_slices.pattern_combination_support(rows)
        self.assertEqual(len(support), 7)
        self.assertEqual(support.loc[support["config_id"].eq("ON,ON,OFF"), "Rows"].item(), 2)
        self.assertEqual(support.loc[support["config_id"].eq("ON,ON,ON"), "Rows"].item(), 0)


class TestFixedEdges(unittest.TestCase):
    def test_edges_need_labels(self):
        session = PatternAnalysis(SPEC)
        with contextlib.redirect_stdout(io.StringIO()):
            session.load()
            with self.assertRaises(ValueError):
                session.create_tradeoffs(method="discretization", edges=EDGES)

    def test_fixed_edges_reproduce_the_detected_regions(self):
        detected, fixed = load(), load(edges=EDGES)
        self.assertTrue((fixed.discrete_df.astype(str) == detected.discrete_df.astype(str)).all().all())

    def test_slices_share_the_regions_of_the_full_dataset(self):
        full = load(edges=EDGES)
        for name in ("baseline", "client_selector", "message_compressor", "hdh"):
            with self.subTest(slice=name):
                sliced = load(name, edges=EDGES)
                self.assertEqual(bin_edges(sliced), bin_edges(full))
                # Each run keeps the label it has in the full dataset
                keys = ["config_id", "Model", "final_val_accuracy", "avg_total_time"]
                full_labels = full.discrete_df.astype(str).agg("-".join, axis=1)
                sliced_labels = sliced.discrete_df.astype(str).agg("-".join, axis=1)
                full_map = dict(zip(map(tuple, full.raw_df[keys].values), full_labels))
                for key, label in zip(map(tuple, sliced.raw_df[keys].values), sliced_labels):
                    self.assertEqual(label, full_map[key])
        # Detected edges would differ per slice
        self.assertNotEqual(bin_edges(load("hdh")), bin_edges(full))


if __name__ == "__main__":
    unittest.main()
