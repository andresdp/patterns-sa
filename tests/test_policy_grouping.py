"""Policy grouping for robustness analysis (see docs/robustness_policy_grouping.md).

Gateway Offloading (single decision): every grouping must describe the same rows.
Federated Learning (three ON/OFF decisions): configurations, qualified decision policies
and single-decision breakdowns must stay distinct, and plain 'ON'/'OFF' must be rejected
as ambiguous instead of silently matching the first decision.
"""
import contextlib
import io
import os
import sys
import unittest

import pandas as pd

from adept import PatternAnalysis
from adept.core.models import Box

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
GO_DIR = os.path.join(REPO_ROOT, "patterns", "Gateway_Offloading")
sys.path.insert(0, FL_DIR)

from preprocess_fl_clients import preprocess_fl  # noqa: E402

FL_CONFIGS = ["OFF,OFF,OFF", "OFF,OFF,ON", "OFF,ON,OFF", "ON,OFF,OFF"]
FL_DECISION_LABELS = [
    "client_selector_pattern:OFF", "client_selector_pattern:ON",
    "message_compressor_pattern:OFF", "message_compressor_pattern:ON",
    "hdh_pattern:OFF", "hdh_pattern:ON",
]
GO_POLICIES = ["long-services-offloaded", "no-offloading", "short-services-offloaded"]


def preprocess_gateway_offloading(df):
    """Mirror of the preprocessor in patterns/Gateway_Offloading/analysis-go.ipynb."""
    configurations = {0: 'no-offloading', 5: 'short-services-offloaded', 10: 'long-services-offloaded'}
    inputs = ['N_A', 'N_B', 'r_Z_A', 'r_Z_B', 'r_gw', 'r_A_s1', 'r_B_s2', 'r_B_s3']
    outputs = ['response_time', 'utilization']
    df = df.rename(columns={'R0': 'response_time', 'Ugw': 'utilization'})
    df['S_gw'] = df['r_gw'].apply(lambda x: 0.0 if x > 1e10 else (1.0 / x if x != 0 else 0.0))
    parts = []
    for s in df['S_gw'].unique():
        if int(s) in configurations:
            part = df[df['S_gw'] == s][inputs + outputs].copy()
            part['policy'] = pd.Series(configurations[int(s)], index=part.index).astype('category')
            part['S_gw'] = s
            parts.append(part)
    out = pd.concat(parts).rename_axis('scenario').reset_index()
    out['model'] = 'gateway_offloading'
    return out.sort_values(by=['N_A', 'S_gw']).reset_index(drop=True)


def load_session(json_path, preprocessor, objectives, test_size):
    with contextlib.redirect_stdout(io.StringIO()):
        session = PatternAnalysis(json_path)
        session.load(preprocessor=preprocessor)
        session.create_tradeoffs(method="discretization", objectives=objectives)
        session.split_data(test_size=test_size, verbose=False)
    return session


class TestSingleDecisionGrouping(unittest.TestCase):
    """Gateway Offloading: configurations and policies coincide, so all groupings agree."""

    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        os.chdir(GO_DIR)  # the system JSON references its CSV relatively
        try:
            cls.session = load_session("Gateway_Offloading.json", preprocess_gateway_offloading,
                                       ["response_time", "utilization"], test_size=0.4)
        finally:
            os.chdir(cwd)

    def test_groupings_have_the_same_labels(self):
        s = self.session
        self.assertEqual(s._policy_labels("configuration"), GO_POLICIES)
        self.assertEqual(sorted(s._policy_labels("offloading_strategy")), GO_POLICIES)
        self.assertEqual([l.split(":")[-1] for l in s._policy_labels("decision")], GO_POLICIES)

    def test_report_is_independent_of_grouping(self):
        s = self.session
        by_config = s.get_robustness_report(subset="test")
        by_decision_key = s.get_robustness_report(decision_key="offloading_strategy", subset="test")
        pd.testing.assert_frame_equal(by_config, by_decision_key.loc[by_config.index])

    def test_plain_policy_names_still_resolve(self):
        t = self.session.get_tradeoffs(non_empty=True)[0].name
        value = self.session.compute_robustness("no-offloading", t, subset="test")["value"]
        by_key = self.session.compute_robustness("no-offloading", t, subset="test", by="offloading_strategy")["value"]
        self.assertEqual(value, by_key)


class TestMultiDecisionGrouping(unittest.TestCase):
    """Federated Learning: three decisions sharing the policy names ON/OFF."""

    @classmethod
    def setUpClass(cls):
        cls.session = load_session(os.path.join(FL_DIR, "FLsystem_split.json"), preprocess_fl,
                                   ["best_val_f1", "avg_total_time"], test_size=0.3)
        target = cls.session.get_tradeoffs(non_empty=True)[0].name
        cls.target = target
        cls.box = Box(limits={"Client Selector Value": {"min": 1.8, "max": 2.0}}, target_tradeoff=target)

    def test_labels_per_grouping(self):
        s = self.session
        self.assertEqual(s._policy_labels("configuration"), FL_CONFIGS)
        self.assertEqual(sorted(s._policy_labels("decision")), sorted(FL_DECISION_LABELS))
        self.assertEqual(sorted(s._policy_labels("hdh_pattern")), ["OFF", "ON"])

    def test_decision_policy_rows_follow_configurations(self):
        s = self.session
        config = s.experiments_df[s.sys_def.dataspace.configuration_identification.column]
        hdh_on = s._policy_mask("hdh_pattern:ON")
        self.assertEqual(list(hdh_on), list(config == "OFF,OFF,ON"))
        self.assertTrue((s._policy_mask("OFF", by="hdh_pattern") == ~hdh_on).all())

    def test_plain_shared_policy_name_is_ambiguous(self):
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            self.session.compute_robustness("ON", self.target)

    def test_qualified_label_matches_decision_breakdown(self):
        s = self.session
        qualified = s.compute_robustness("hdh_pattern:ON", self.target, subset="test")["value"]
        by_decision = s.compute_robustness("ON", self.target, subset="test", by="hdh_pattern")["value"]
        self.assertEqual(qualified, by_decision)

    def test_report_rows_per_grouping(self):
        s = self.session
        self.assertEqual(list(s.get_robustness_report(subset="test").index), FL_CONFIGS)
        self.assertEqual(sorted(s.get_robustness_report(subset="test", by="decision").index), sorted(FL_DECISION_LABELS))
        by_key = s.get_robustness_report(subset="test", by="hdh_pattern")
        pd.testing.assert_frame_equal(by_key, s.get_robustness_report(subset="test", decision_key="hdh_pattern"))

    def test_robustness_results_for_every_grouping(self):
        s = self.session
        for by, labels in (("configuration", FL_CONFIGS), ("decision", FL_DECISION_LABELS), ("hdh_pattern", ["OFF", "ON"])):
            with contextlib.redirect_stdout(io.StringIO()) as out:
                results = s.get_robustness_results([self.box], [self.box], by=by)
            self.assertNotIn("do not match", out.getvalue(), by)
            self.assertTrue(set(results["policy"]) <= set(labels), by)
            baseline_rows = results[results["method"] == "test set"]["policy"]
            self.assertTrue(set(baseline_rows) <= set(labels), by)

    def test_mismatched_baseline_warns(self):
        s = self.session
        per_decision = s.get_robustness_report(subset="test", by="hdh_pattern")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            s.get_robustness_results([self.box], [self.box], baseline=per_decision)
        self.assertIn("do not match", out.getvalue())

    def test_improvement_matrix_and_uplift_rows(self):
        s = self.session
        aligned = s.align_boxes_to_tradeoffs([self.box])
        self.assertEqual(sorted(s.get_policy_robustness_improvement_matrix(aligned, subset="test", by="decision").index),
                         sorted(FL_DECISION_LABELS))
        uplift = s.analyze_robustness_uplift(self.box, self.target, subset="test", by="decision")
        self.assertEqual(list(uplift.index).count("GLOBAL"), 1)
        self.assertTrue(set(uplift.index) - {"GLOBAL"} <= set(FL_DECISION_LABELS))


if __name__ == "__main__":
    unittest.main()
