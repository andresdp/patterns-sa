"""Pattern stress, client-count/task/environment filters and the all-configurations spec
(federatedlearning/pattern_stress.py, fl_slices.py, compact/FLsystem_compact_all.json)."""
import contextlib
import io
import os
import sys
import tempfile
import unittest

import pandas as pd

from adept import PatternAnalysis
from adept.core.loader import GenericDataLoader

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
ALL_SPEC = os.path.join(FL_DIR, "compact", "FLsystem_compact_all.json")
sys.path.insert(0, FL_DIR)

import fl_slices  # noqa: E402
import make_slice_notebooks  # noqa: E402
import pattern_stress  # noqa: E402

LABELS = {"final_val_accuracy": ["S", "M", "L"], "avg_total_time": ["S", "M", "L"]}


def load(**filters):
    session = PatternAnalysis(ALL_SPEC)
    with contextlib.redirect_stdout(io.StringIO()):
        session.load(preprocessor=fl_slices.slice_filter(**filters))
    return session


def run(config, n_clients, usage, distribution):
    """One synthetic run with per-client usage (None = not recorded) and distributions."""
    row = {"config_id": config, "Total Clients": n_clients}
    for i, (u, d) in enumerate(zip(usage, distribution), start=1):
        row[f"Client {i} CPU Usage Avg"] = u
        row[f"Client {i} Data Distribution"] = d
    return row


class TestPatternStress(unittest.TestCase):
    def test_types_and_instances(self):
        df = pd.DataFrame([
            # 4 clients, all participate, clients 3-4 non-IID
            run("OFF,OFF,OFF", 4, [1, 1, 1, 1], ["IID", "IID", "non-IID", "non-IID"]),
            run("OFF,ON,ON", 4, [1, 1, 1, 1], ["IID", "IID", "non-IID", "non-IID"]),
            # selector ON: client 4 (non-IID) excluded, so one HDH instance less
            run("ON,ON,ON", 4, [1, 1, 1, None], ["IID", "IID", "non-IID", "non-IID"]),
            # client 4 does not exist in a 3-client run, whatever its columns say
            run("OFF,ON,OFF", 3, [1, 1, 1, 1], ["IID", "IID", "IID", "IID"]),
        ])
        out = pattern_stress.add_pattern_stress(df)
        self.assertEqual(list(out["Pattern Types Active"]), [0, 2, 3, 1])
        self.assertEqual(list(out["Client Selector Instances"]), [0, 0, 1, 0])
        self.assertEqual(list(out["Message Compressor Instances"]), [0, 4, 3, 3])
        self.assertEqual(list(out["HDH Instances"]), [0, 2, 1, 0])
        self.assertEqual(list(out["Pattern Instances"]), [0, 6, 5, 3])
        self.assertEqual(list(out["Participating Clients"]), [4, 4, 3, 3])

    def test_participation_assumption_holds_on_the_compact_data(self):
        # A4: with the selector ON, participants are exactly the clients that are not low-spec
        raw = load().raw_df
        selector_on = raw["config_id"].str.startswith("ON")
        cpu = pd.DataFrame({i: raw[f"Client {i} CPU"] for i in range(1, 11)})
        exists = pd.DataFrame({i: raw["Total Clients"] >= i for i in range(1, 11)})
        low_spec = ((cpu < cpu.max().max()) & exists).sum(axis=1)
        expected = raw["Total Clients"] - low_spec.where(selector_on, 0)
        self.assertTrue((raw["Participating Clients"] == expected).all())
        # A5: HDH instances never exceed the non-IID clients
        self.assertTrue((raw["HDH Instances"] <= raw["non_iid_clients"]).all())


class TestCompactFilters(unittest.TestCase):
    def test_all_configurations_from_both_csvs(self):
        raw = load().raw_df
        self.assertEqual(len(raw), 2340)
        self.assertEqual(raw["config_id"].nunique(), 8)
        self.assertIn("Pattern Types Active", load().experiments_df.columns)

    def test_clients_and_task(self):
        raw = load(clients=8, task="text").raw_df
        self.assertEqual(set(raw["Total Clients"]), {8})
        self.assertEqual(set(zip(raw["Dataset"], raw["Model"])), {("AG_NEWS", "MLP")})
        self.assertEqual(raw["config_id"].nunique(), 8)

    def test_common_environment_is_a_balanced_factorial(self):
        raw = load(clients=4, task="image", environment="common").raw_df
        self.assertEqual(set(raw["config_id"].value_counts()), {10})
        self.assertEqual(raw[list(fl_slices.ENVIRONMENT_COLUMNS)].drop_duplicates().shape[0], 1)

    def test_unknown_task(self):
        with self.assertRaises(ValueError):
            fl_slices.slice_filter(task="audio")


class TestColumnGrouping(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = load(clients=8, task="image", environment="common")
        with contextlib.redirect_stdout(io.StringIO()):
            cls.session.create_tradeoffs(method="discretization", labels=LABELS)

    def test_robustness_by_a_column(self):
        matrix = self.session.get_robustness_report(metric="starr", subset="all", by="Pattern Types Active")
        self.assertEqual(list(matrix.index), [f"Pattern Types Active={i}" for i in range(4)])
        # Each level's runs fall in exactly one region
        self.assertTrue(((matrix.sum(axis=1) - 1).abs() < 1e-9).all())

    def test_decisions_take_precedence_over_columns(self):
        matrix = self.session.get_robustness_report(metric="starr", subset="all", by="hdh_pattern")
        self.assertEqual(sorted(matrix.index), ["OFF", "ON"])

    def test_unknown_grouping(self):
        with self.assertRaises(ValueError):
            self.session.get_robustness_report(metric="starr", subset="all", by="no such column")


class TestSourceFileList(unittest.TestCase):
    def test_files_are_concatenated(self):
        with tempfile.TemporaryDirectory() as tmp:
            pd.DataFrame({"policy": ["a"], "x": [1.0], "y": [2.0]}).to_csv(os.path.join(tmp, "one.csv"), index=False)
            pd.DataFrame({"y": [4.0], "x": [3.0], "policy": ["b"]}).to_csv(os.path.join(tmp, "two.csv"), index=False)
            spec = os.path.join(tmp, "spec.json")
            with open(spec, "w") as f:
                f.write('{"system": {"name": "S", "components": {"c": {"name": "C", "parameters": '
                        '{"x": {"level": "system", "type": "lever"}}}}}, "dataspace": {"source_file": '
                        '["one.csv", "two.csv"], "configuration_identification": {"from": "column", '
                        '"column": "policy", "configurations": {}}, "quality_objectives": [{"name": "y"}]}}')
            with contextlib.redirect_stdout(io.StringIO()):
                raw, _, _ = GenericDataLoader().load_data(spec, validate_integrity=False)
        self.assertEqual(list(raw["policy"]), ["a", "b"])
        self.assertEqual(list(raw["x"]), [1.0, 3.0])


class TestStressNotebooks(unittest.TestCase):
    def test_generated_parameters(self):
        nb = make_slice_notebooks.make_stress_notebook(8, "image")
        params = next("".join(c["source"]) for c in nb["cells"] if "parameters" in c["metadata"].get("tags", []))
        ns = {}
        exec(params, {}, ns)
        self.assertEqual((ns["CLIENTS"], ns["TASK"], ns["ENVIRONMENT"], ns["SLICE"]), (8, "image", "common", "all"))
        self.assertEqual(ns["SPEC"], make_slice_notebooks.STRESS_SPEC)
        self.assertIsNone(ns["TRADEOFF_EDGES"])  # each stress notebook detects its own edges
        self.assertEqual(make_slice_notebooks.stress_output_name(8, "image"), "analysis-fl-stress-c8-image.ipynb")


if __name__ == "__main__":
    unittest.main()
