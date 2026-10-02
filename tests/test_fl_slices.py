"""Focused slices of the FL dataset (federatedlearning/fl_slices.py, make_slice_notebooks.py)."""
import contextlib
import io
import os
import sys
import unittest

from adept import PatternAnalysis

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
SPEC = os.path.join(FL_DIR, "FLsystem_split.json")
sys.path.insert(0, FL_DIR)

import fl_slices  # noqa: E402
import make_slice_notebooks  # noqa: E402

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

    def test_all_has_no_filter(self):
        self.assertIsNone(fl_slices.slice_filter("all"))

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


class TestFixedEdges(unittest.TestCase):
    def test_base_notebook_detects_edges_by_default(self):
        import json
        with open(make_slice_notebooks.BASE_NOTEBOOK) as f:
            cells = json.load(f)["cells"]
        params = "".join(next(c for c in cells if "parameters" in c["metadata"].get("tags", []))["source"])
        self.assertIn("TRADEOFF_EDGES = None", params)

    def test_generator_edges_reproduce_the_detected_regions(self):
        edges = make_slice_notebooks.full_dataset_edges(SPEC, OBJECTIVES)
        detected, fixed = load(), load(edges=edges)
        self.assertTrue(fixed.discrete_df.astype(str).equals(detected.discrete_df.astype(str)))

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


class TestGenerator(unittest.TestCase):
    def test_generated_notebook(self):
        nb = make_slice_notebooks.make_notebook("hdh", include_baseline=True)
        sources = ["".join(c["source"]) for c in nb["cells"]]
        params = next(s for c, s in zip(nb["cells"], sources) if "parameters" in c["metadata"].get("tags", []))
        self.assertIn("SLICE = 'hdh'", params)
        self.assertIn("INCLUDE_BASELINE = True", params)
        # The base notebook detects the edges; the focused one fixes those of the full dataset
        self.assertIn("TRADEOFF_EDGES = {", params)
        ns = {}
        exec(params, {}, ns)
        self.assertEqual(ns["TRADEOFF_EDGES"], make_slice_notebooks.full_dataset_edges(ns["SPEC"], ns["TRADEOFF_LABELS"]))
        self.assertIn("Focused analysis", sources[1])
        tagged = [s for c, s in zip(nb["cells"], sources)
                  if make_slice_notebooks.INTERPRETATION_TAG in c["metadata"].get("tags", [])]
        self.assertTrue(tagged)
        self.assertTrue(all("Interpretation to be written for this slice" in s for s in tagged))
        self.assertTrue(all(not c.get("outputs") for c in nb["cells"] if c["cell_type"] == "code"))
        self.assertEqual(make_slice_notebooks.output_name("hdh", True), "analysis-fl-hdh-vs-baseline.ipynb")


if __name__ == "__main__":
    unittest.main()
